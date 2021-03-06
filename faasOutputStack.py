import inspect;
from .faasOutputSourceCode import faasOutputSourceCode;
from .fasGetSourceCode import fasGetSourceCode;
from .mColors import *;

def faasOutputStack(oStack, oException = None, bAddHeader = True):
  aasOutputLines = [];
  if bAddHeader:
    aasOutputLines += [
      [
        guStackHeaderColor, "Stack for thread ", guStackHeaderHighlightColor, "0x%X/%d" % (oStack.uThreadId, oStack.uThreadId),
        guStackHeaderColor, " (", guStackHeaderHighlightColor, oStack.sThreadName or "<unnamed>", guStackHeaderColor, ")",
        guStackHeaderColor, ".",
      ],
    ];
  bIsSyntaxError = isinstance(oException, SyntaxError);
  auExceptionReraisingFrameIndices = [-1];
  for oFrame in oStack.aoFrames:
    bIsLastFrame = oFrame == oStack.aoFrames[-1] and not bIsSyntaxError;
    bIsExceptionFrame = oFrame.uExceptionLineNumber is not None;
    if bIsExceptionFrame and oFrame.uExceptionLineNumber != oFrame.uLastExecutedLineNumber:
      auExceptionReraisingFrameIndices.append(oFrame.uIndex);
    uCodeCallNameColor = guStackAtExceptionCallDescriptionColor if bIsLastFrame else guStackBeforeExceptionCallDescriptionColor;
    uCodeCallNameAndLocationJoinerColor = guStackAtExceptionCallDescriptionAndLocationJoinerColor if bIsLastFrame else guStackBeforeExceptionCallDescriptionAndLocationJoinerColor;
    uCodeCallLocationColor = guStackAtExceptionSourceFilePathColor if bIsLastFrame else guStackBeforeExceptionSourceFilePathColor;
    aasOutputLines += [
      [
        guStackTreeColor, " \xB3" * (oFrame.uIndex - 1), " \xC3" if oFrame.uIndex > 0 else "", "\xC4\xBF ",
        uCodeCallNameColor, oFrame.sCallDescription,
        uCodeCallNameAndLocationJoinerColor, " @ ",
        uCodeCallLocationColor, oFrame.sExceptionCodeLocation if bIsExceptionFrame else oFrame.sLastExecutedCodeLocation,
      ]
    ];
    uLineNumber = oFrame.uExceptionLineNumber if bIsExceptionFrame else oFrame.uLastExecutedLineNumber;
    aasOutputLines += faasOutputSourceCode(
      axOutputHeader = [guStackTreeColor, " \xB3" * (oFrame.uIndex + 1), " "],
      asModuleSourceCode = oFrame.asModuleSourceCode,
      uStartLineNumber = uLineNumber - 1,
      uEndLineNumber = uLineNumber + 1,
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor if bIsLastFrame else guStackBeforeExceptionInactiveSourceCodeColor,
      uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor if bIsLastFrame else guStackBeforeExceptionActiveSourceCodeColor,
    );
  uCurrentFrameIndex = oStack.aoFrames[-1].uIndex;
  uNextFrameIndex = auExceptionReraisingFrameIndices.pop() if auExceptionReraisingFrameIndices else -1;
  if oException:
    if bIsSyntaxError:
      aasOutputLines += [
        [
          guStackTreeColor, " \xB3" * uCurrentFrameIndex, " \xC3\xC4\xBF ",
          guStackAtExceptionCallDescriptionColor, "<module>",
          guStackAtExceptionCallDescriptionAndLocationJoinerColor, " @ ",
          guStackAtExceptionSourceFilePathColor, str(oException.filename), "/", str(oException.lineno),
        ]
      ];
      asModuleSourceCode = fasGetSourceCode(oException.filename);
      uCurrentFrameIndex += 1;
      aasOutputLines += faasOutputSourceCode(
        axOutputHeader = [guStackTreeColor, " \xB3" * (uCurrentFrameIndex + 1), " "],
        asModuleSourceCode = asModuleSourceCode,
        uStartLineNumber = oException.lineno - 1,
        uEndLineNumber = oException.lineno + 1,
        uLineNumberColor = guLineNumberColor,
        uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
        uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
      );
      uEndLineNumberSize = len(str(min(oException.lineno + 2, len(asModuleSourceCode) + 1)));
      aasOutputLines += [
        [
          guStackTreeColor, " \xB3" * (uCurrentFrameIndex + 1), " ",
          guStackAtExceptionColumnIndicatorColor, " " * (uEndLineNumberSize + oException.offset), "\x1E"
        ]
      ];
      sException = "%s(%s at character %d)" % (oException.__class__.__name__, repr(oException.msg), oException.offset);
    elif isinstance(oException, AssertionError):
      sException = "Assertion failed: %s" % oException.message;
    elif hasattr(oException, "message"):
      sException = "%s(%s)" % (oException.__class__.__name__, repr(oException.message));
    else:
      sException = repr(oException);
    aasOutputLines += [
      [
        guStackTreeColor, " \xB3" * uNextFrameIndex, " \xC3", "\xC4\xC1" * (uCurrentFrameIndex - uNextFrameIndex - 1), "\xC4\xD9",
        guStackAtExceptionInformationColor, " ==\x10 ", sException,
      ]
    ];
  while auExceptionReraisingFrameIndices:
    uCurrentFrameIndex = uNextFrameIndex;
    uNextFrameIndex = auExceptionReraisingFrameIndices.pop();
    oFrame = oStack.aoFrames[uCurrentFrameIndex];
    aasOutputLines += [
      [
        guStackTreeColor, " \xB3" * (oFrame.uIndex + 1), " ",
        guStackAfterExceptionCallDescriptorColor, oFrame.sCallDescription,
        guStackAfterExceptionCallDescriptorAndSourceFilePathJoinerColor, " @ ",
        guStackAfterExceptionSourceFilePathColor, oFrame.sLastExecutedCodeLocation,
      ]
    ];
    aasOutputLines += faasOutputSourceCode(
      axOutputHeader = [guStackTreeColor, " \xB3" * (oFrame.uIndex + 1), " "],
      asModuleSourceCode = oFrame.asModuleSourceCode,
      uStartLineNumber = oFrame.uLastExecutedLineNumber - 1,
      uEndLineNumber = oFrame.uLastExecutedLineNumber + 1,
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAfterExceptionInactiveSourceCodeColor,
      uActiveCodeColor = guStackAfterExceptionActiveSourceCodeColor,
    );
    aasOutputLines += [
      [
        guStackTreeColor, " \xB3" * (uNextFrameIndex), " \xC3" if uNextFrameIndex >= 0 else "", \
            "\xC4\xC1" * (uCurrentFrameIndex - uNextFrameIndex - 1), "\xC4\xD9 ",
        guStackAfterExceptionActiveSourceCodeColor, oFrame.sLastExecutedSourceCode or "<no code>",
      ]
    ];
  
  return aasOutputLines;
