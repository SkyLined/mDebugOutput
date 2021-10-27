import inspect;

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
        guStackTreeColor, " ╷" * (oFrame.uIndex - 1), " ├" if oFrame.uIndex > 0 else "", "─┐ ",
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
      axOutputHeader = [guStackTreeColor, " ╷" * oFrame.uIndex, " │ "],
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
          guStackTreeColor, " ╷" * (uCurrentFrameIndex - 1), " ├" if uCurrentFrameIndex > 0 else "", "─┐ ",
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
        axOutputHeader = [guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ "],
        uLineNumberColor = guLineNumberColor,
        uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
        uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
      );
      asModuleSourceCode = fasGetSourceCode(oException.filename);
      uEndLineNumberSize = len(str(min(oException.lineno + 2, len(asModuleSourceCode) + 1)));
      if oException.offset is not None:
        aasConsoleOutputLines += [
          [
            guStackTreeColor, " ╷" * uCurrentFrameIndex, " │", 
            # The below calculation will never give a negative result because uEndLineNumberSize is always larger than 1
            guStackAtExceptionColumnIndicatorColor, " ╭", "─" * (uEndLineNumberSize + oException.offset - 1), "╯"
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
    asExceptionLines = sException.split("\n");
    uLineNumber = 0;
    sHeader1 = (
      " ╒" + ("═" * (2 * (uCurrentFrameIndex - uNextFrameIndex) - 1)) + "╛"
    ) if uCurrentFrameIndex != uNextFrameIndex else (
      " │"
    ) if uCurrentFrameIndex != 0 else (
      ""
    );
    sHeaderN = (
      " │" + (" " * (2 * (uCurrentFrameIndex - uNextFrameIndex)))
    ) if uCurrentFrameIndex != uNextFrameIndex else (
      sHeader1
    );
    for sExceptionLine in asExceptionLines:
      uLineNumber += 1;
      aasConsoleOutputLines += [
        [
          guStackTreeColor, " ╷" * uNextFrameIndex, 
        ] + [
          sHeader1 if uLineNumber == 1 else sHeaderN
        ] + [
          guStackExceptionInformationColor, " ▲ " if uLineNumber == 1 else "   ", sExceptionLine.rstrip("\r"),
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
        guStackTreeColor, " ╷" * oFrame.uIndex, " │ ",
        guStackAfterExceptionCallDescriptorColor, oFrame.sCallDescription,
        guStackAfterExceptionCallDescriptorAndSourceFilePathJoinerColor, " @ ",
        guStackAfterExceptionSourceFilePathColor, oFrame.sLastExecutedCodeLocation,
      ]
    ];
    # Source code where the exception was handled
    aasConsoleOutputLines += oFrame.faasCreateConsoleOutputForLastExecutedSourceCode(
      axOutputHeader = [guStackTreeColor, " ╷" * oFrame.uIndex, " │ "],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackAfterExceptionInactiveSourceCodeColor,
      uActiveCodeColor = guStackAfterExceptionActiveSourceCodeColor,
    );
    aasConsoleOutputLines += [
      [
        guStackTreeColor, " ╷" * uNextFrameIndex, " ╒" if uNextFrameIndex >= 0 else "", \
      ] + ([
        "═" * 2 * (uCurrentFrameIndex - uNextFrameIndex - 1)
      ] if uCurrentFrameIndex != 0 else []) + [
        "═╛",
      ] + ([
        guStackTerminatedInformationColor, " ▲ Application terminated because exception was not handled.",
      ] if uCurrentFrameIndex == 0 else [])
    ];
  
  return aasConsoleOutputLines;

from .faasCreateConsoleOutputForSourceCode import faasCreateConsoleOutputForSourceCode;
from .fasGetSourceCode import fasGetSourceCode;
from .mColorsAndChars import *;
