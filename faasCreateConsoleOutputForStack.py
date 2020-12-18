import inspect;
from .faasCreateConsoleOutputForSourceCode import faasCreateConsoleOutputForSourceCode;
from .fasGetSourceCode import fasGetSourceCode;
from .mColors import *;

def faasCreateConsoleOutputForStack(oStack, oException = None, bAddHeader = True):
  aasConsoleOutputLines = [];
  if bAddHeader:
    aasConsoleOutputLines += [
      [
        guStackHeaderColor, "Stack for thread ", guStackHeaderHighlightColor, "%d/0x%X" % (oStack.uThreadId, oStack.uThreadId),
        guStackHeaderColor, " (", guStackHeaderHighlightColor, oStack.sThreadName or "<unnamed>", guStackHeaderColor, ")",
        guStackHeaderColor, ":",
      ],
    ];
  bIsSyntaxError = isinstance(oException, SyntaxError);
  auExceptionReraisingFrameIndices = [-1];
  for oFrame in oStack.aoFrames:
    bIsExceptionFrame = oException and oFrame == oStack.aoFrames[-1] and not bIsSyntaxError;
    bIsExceptionReraisingFrame = oFrame.u0ExceptionLineNumber is not None;
    if bIsExceptionReraisingFrame and oFrame.u0ExceptionLineNumber != oFrame.uLastExecutedLineNumber:
      auExceptionReraisingFrameIndices.append(oFrame.uIndex);
    uCodeCallNameColor = guStackAtExceptionCallDescriptionColor if bIsExceptionFrame else guStackNormalCallDescriptionColor;
    uCodeCallNameAndLocationJoinerColor = guStackAtExceptionCallDescriptionAndLocationJoinerColor if bIsExceptionFrame else guStackNormalCallDescriptionAndLocationJoinerColor;
    uCodeCallLocationColor = guStackAtExceptionSourceFilePathColor if bIsExceptionFrame else guStackNormalSourceFilePathColor;
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \xB3" * (oFrame.uIndex - 1), " \xC3" if oFrame.uIndex > 0 else "", "\xC4\xBF ",
        uCodeCallNameColor, oFrame.sCallDescription,
        uCodeCallNameAndLocationJoinerColor, " @ ",
        uCodeCallLocationColor, oFrame.sExceptionCodeLocation if bIsExceptionReraisingFrame else oFrame.sLastExecutedCodeLocation,
      ]
    ];
    faasCreateConsoleOutputForFrameSourceCode = (
      oFrame.faasCreateConsoleOutputForExceptionSourceCode if bIsExceptionReraisingFrame else
      oFrame.faasCreateConsoleOutputForLastExecutedSourceCode
    );
    aasConsoleOutputLines += faasCreateConsoleOutputForFrameSourceCode(
      axOutputHeader = [guStackTreeColor, " \xB3" * (oFrame.uIndex + 1), " "],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor if bIsExceptionFrame else guStackNormalInactiveSourceCodeColor,
      uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor if bIsExceptionFrame else guStackNormalActiveSourceCodeColor,
    );
  uCurrentFrameIndex = oStack.aoFrames[-1].uIndex;
  uNextFrameIndex = auExceptionReraisingFrameIndices.pop() if auExceptionReraisingFrameIndices else -1;
  if oException:
    if bIsSyntaxError:
      aasConsoleOutputLines += [
        [
          guStackTreeColor, " \xB3" * uCurrentFrameIndex, " \xC3\xC4\xBF ",
          guStackAtExceptionCallDescriptionColor, "<module>",
          guStackAtExceptionCallDescriptionAndLocationJoinerColor, " @ ",
          guStackAtExceptionSourceFilePathColor, str(oException.filename), "/", str(oException.lineno), "/", str(oException.offset),
        ]
      ];
      uCurrentFrameIndex += 1;
      aasConsoleOutputLines += faasCreateConsoleOutputForSourceCode(
        sSourceFilePath = oException.filename,
        uStartLineNumber = oException.lineno - 1,
        uEndLineNumber = oException.lineno + 1,
        axOutputHeader = [guStackTreeColor, " \xB3" * (uCurrentFrameIndex + 1), " "],
        uLineNumberColor = guLineNumberColor,
        uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
        uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
      );
      asModuleSourceCode = fasGetSourceCode(oException.filename);
      uEndLineNumberSize = len(str(min(oException.lineno + 2, len(asModuleSourceCode) + 1)));
      if oException.offset is not None:
        aasConsoleOutputLines += [
          [
            guStackTreeColor, " \xB3" * (uCurrentFrameIndex + 1), " ",
            guStackAtExceptionColumnIndicatorColor, " " * (uEndLineNumberSize + oException.offset), "\x1E"
          ]
        ];
        sException = "%s(%s at character %d)" % (oException.__class__.__name__, repr(oException.msg), oException.offset);
      else:
        sException = "%s(%s)" % (oException.__class__.__name__, repr(oException.msg));
    elif isinstance(oException, AssertionError):
      sException = "Assertion failed: %s" % oException.message;
    elif hasattr(oException, "message"):
      sException = "%s(%s)" % (oException.__class__.__name__, repr(oException.message));
    else:
      sException = repr(oException);
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \xB3" * uNextFrameIndex, " \xC3", "\xC4\xC1" * (uCurrentFrameIndex - uNextFrameIndex - 1), "\xC4\xD9",
        guStackAtExceptionInformationColor, " ==\x10 ", sException,
      ]
    ];
  while auExceptionReraisingFrameIndices:
    uCurrentFrameIndex = uNextFrameIndex;
    uNextFrameIndex = auExceptionReraisingFrameIndices.pop();
    oFrame = oStack.aoFrames[uCurrentFrameIndex];
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \xB3" * (oFrame.uIndex + 1), " ",
        guStackAfterExceptionCallDescriptorColor, oFrame.sCallDescription,
        guStackAfterExceptionCallDescriptorAndSourceFilePathJoinerColor, " @ ",
        guStackAfterExceptionSourceFilePathColor, oFrame.sLastExecutedCodeLocation,
      ]
    ];
    aasConsoleOutputLines += oFrame.faasCreateConsoleOutputForLastExecutedSourceCode(
      axOutputHeader = [guStackTreeColor, " \xB3" * (oFrame.uIndex + 1), " "],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAfterExceptionInactiveSourceCodeColor,
      uActiveCodeColor = guStackAfterExceptionActiveSourceCodeColor,
    );
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \xB3" * (uNextFrameIndex), " \xC3" if uNextFrameIndex >= 0 else "", \
            "\xC4\xC1" * (uCurrentFrameIndex - uNextFrameIndex - 1), "\xC4\xD9 ",
        guStackAfterExceptionActiveSourceCodeColor, oFrame.sLastExecutedSourceCode or "<no code>",
      ]
    ];
  
  return aasConsoleOutputLines;
