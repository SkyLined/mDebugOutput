import inspect;
from .faasCreateConsoleOutputForSourceCode import faasCreateConsoleOutputForSourceCode;
from .fasGetSourceCode import fasGetSourceCode;
from .mColors import *;

def faasCreateConsoleOutputForStack(oStack, oException = None, bAddHeader = True):
  aasConsoleOutputLines = [];
  # Header
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
    # Function, source file name and line number
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \u250A" * (oFrame.uIndex - 1), " \u251C" if oFrame.uIndex > 0 else "", "\u2500\u2510 ",
        uCodeCallNameColor, oFrame.sCallDescription,
        uCodeCallNameAndLocationJoinerColor, " @ ",
        uCodeCallLocationColor, oFrame.sExceptionCodeLocation if bIsExceptionReraisingFrame else oFrame.sLastExecutedCodeLocation,
      ]
    ];
    # Source code
    faasCreateConsoleOutputForFrameSourceCode = (
      oFrame.faasCreateConsoleOutputForExceptionSourceCode if bIsExceptionReraisingFrame else
      oFrame.faasCreateConsoleOutputForLastExecutedSourceCode
    );
    aasConsoleOutputLines += faasCreateConsoleOutputForFrameSourceCode(
      axOutputHeader = [guStackTreeColor, " \u250A" * oFrame.uIndex, " \u2502 "],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor if bIsExceptionFrame else guStackNormalInactiveSourceCodeColor,
      uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor if bIsExceptionFrame else guStackNormalActiveSourceCodeColor,
    );
  uCurrentFrameIndex = oStack.aoFrames[-1].uIndex;
  uNextFrameIndex = auExceptionReraisingFrameIndices.pop() if auExceptionReraisingFrameIndices else -1;
  if oException:
    if bIsSyntaxError:
      # Source file name and line number where syntax error was found
      uCurrentFrameIndex += 1;
      aasConsoleOutputLines += [
        [
          guStackTreeColor, " \u250A" * (uCurrentFrameIndex - 1), " \u251C" if uCurrentFrameIndex > 0 else "", "\u2500\u2510 ",
          guStackAtExceptionCallDescriptionColor, "<module>",
          guStackAtExceptionCallDescriptionAndLocationJoinerColor, " @ ",
          guStackAtExceptionSourceFilePathColor, str(oException.filename), "/", str(oException.lineno),
        ] + (
          ["/", str(oException.offset)] if oException.offset is not None else []
        )
      ];
      # Source code where syntax error was found
      aasConsoleOutputLines += faasCreateConsoleOutputForSourceCode(
        sSourceFilePath = oException.filename,
        uStartLineNumber = oException.lineno - 1,
        uEndLineNumber = oException.lineno + 1,
        axOutputHeader = [guStackTreeColor, " \u250A" * uCurrentFrameIndex, " \u2502 "],
        uLineNumberColor = guLineNumberColor,
        uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
        uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
      );
      asModuleSourceCode = fasGetSourceCode(oException.filename);
      uEndLineNumberSize = len(str(min(oException.lineno + 2, len(asModuleSourceCode) + 1)));
      if oException.offset is not None:
        aasConsoleOutputLines += [
          [
            guStackTreeColor, " \u250A" * uCurrentFrameIndex, " \u2502 ",
            guStackAtExceptionColumnIndicatorColor, "\u256D", "\u2504" * (uEndLineNumberSize + oException.offset - 1), "\u256F"
          ]
        ];
        sException = "%s(%s at character %d)" % (oException.__class__.__name__, repr(oException.msg), oException.offset);
      else:
        sException = "%s(%s)" % (oException.__class__.__name__, repr(oException.msg));
    elif isinstance(oException, AssertionError):
      sException = "Assertion failed: %s" % oException.args[0];
    elif hasattr(oException, "message"):
      sException = "%s(%s)" % (oException.__class__.__name__, ", ".join(repr(xArg) for xArg in oException.args));
    else:
      sException = repr(oException);
    # Exception
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \u250A" * uNextFrameIndex, 
      ] + (
        [
          " \u256D", "\u2500" * 2 * (uCurrentFrameIndex - uNextFrameIndex - 1), "\u2500\u256f",
        ] if uCurrentFrameIndex != uNextFrameIndex else [
          " \u2502",
        ] if uCurrentFrameIndex != 0 else [
          " \u2580",
        ]
      ) + [
        guStackExceptionInformationColor, " \u25A0 ", sException,
      ]
    ];
  while auExceptionReraisingFrameIndices:
    uLastFrameIndex = uCurrentFrameIndex;
    uCurrentFrameIndex = uNextFrameIndex;
    uNextFrameIndex = auExceptionReraisingFrameIndices.pop();
    oFrame = oStack.aoFrames[uCurrentFrameIndex];
    # Source file name and line number where the exception was handled
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \u250A" * oFrame.uIndex, " \u2502 ",
        guStackAfterExceptionCallDescriptorColor, oFrame.sCallDescription,
        guStackAfterExceptionCallDescriptorAndSourceFilePathJoinerColor, " @ ",
        guStackAfterExceptionSourceFilePathColor, oFrame.sLastExecutedCodeLocation,
      ]
    ];
    # Source code where the exception was handled
    aasConsoleOutputLines += oFrame.faasCreateConsoleOutputForLastExecutedSourceCode(
      axOutputHeader = [guStackTreeColor, " \u250A" * oFrame.uIndex, " \u2502 "],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAfterExceptionInactiveSourceCodeColor,
      uActiveCodeColor = guStackAfterExceptionActiveSourceCodeColor,
    );
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " \u250A" * uNextFrameIndex, " \u256D" if uNextFrameIndex >= 0 else "", \
      ] + (
        [
          "\u2500" * 2 * (uCurrentFrameIndex - uNextFrameIndex - 1), "\u2500",
        ] if uCurrentFrameIndex != 0 else [
          "\u25A0",
        ]
      ) + [
        "\u256f",
      ]
    ];
  
  return aasConsoleOutputLines;
