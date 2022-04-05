import inspect;

def faasCreateConsoleOutputForStack(oStack, oException = None, bAddHeader = True):
  aasConsoleOutputLines = [];
  # Header
  if bAddHeader:
    aasConsoleOutputLines += [
      [
        guStackHeaderColor, "Stack for ",
        [
          "thread ",
          guStackHeaderHighlightColor, "%d/0x%X" % (oStack.u0ThreadId, oStack.u0ThreadId),
          guStackHeaderColor, " (",
          guStackHeaderHighlightColor, oStack.s0ThreadName or "<unnamed>",
          guStackHeaderColor, ")",
        ] if oStack.u0ThreadId is not None else [
          "unknown thread"
        ],
        ":"
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
  uCurrentFrameIndex = oStack.aoFrames[-1].uIndex if oStack.aoFrames else -1;
  uNextFrameIndex = auExceptionReraisingFrameIndices.pop() if auExceptionReraisingFrameIndices else -1;
  if oException:
    if bIsSyntaxError:
      if uCurrentFrameIndex != -1:
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
        asModuleSourceCode = fasGetSourceCode(oException.filename);
        uEndLineNumberSize = len(str(min(oException.lineno + 2, len(asModuleSourceCode) + 1)));
        sExceptionLine = asModuleSourceCode[oException.lineno - 1];
        bEndOffsetIsValid = (
          oException.lineno != oException.end_lineno or
          oException.end_offset > oException.offset
        );
        uStartIndex = min(oException.offset, oException.end_offset) if bEndOffsetIsValid else oException.offset;
        if oException.lineno != oException.end_lineno:
          aasConsoleOutputLines += faasCreateConsoleOutputForSourceCode(
            sSourceFilePath = oException.filename,
            uStartLineNumber = oException.lineno - 1,
            uEndLineNumber = oException.lineno + 1,
            axOutputHeader = [guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ", "  "],
            uLineNumberColor = guLineNumberColor,
            uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
            uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
          );
        if oException.lineno == oException.end_lineno - 1:
          bTopFirst = oException.offset < oException.end_offset;
          uHighlightLength = abs(oException.offset - oException.end_offset);
          aasConsoleOutputLines += [
            [
              guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ", 
              guStackAtExceptionColumnIndicatorColor,
                "╭",
                "╴" * (uEndLineNumberSize + uStartIndex + 1),
                [
                  "┘" if bTopFirst else "┐",
                  "╴"  * (uHighlightLength - 1), # 0 or greater because `uHighlightLength > 1` in following line
                  "╮" if bTopFirst else "╯",
                ] if uHighlightLength > 0 else [
                  "┤"
                ],
            ]
          ];
        if oException.lineno < oException.end_lineno - 1:
          aasConsoleOutputLines += [
            [
              guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ", 
              guStackAtExceptionColumnIndicatorColor,
                "╭",
                "╴" * (uEndLineNumberSize + oException.offset + 1),
                "╯",
            ]
          ];
          aasConsoleOutputLines += faasCreateConsoleOutputForSourceCode(
            sSourceFilePath = oException.filename,
            uStartLineNumber = oException.lineno + 1,
            uEndLineNumber = oException.end_lineno,
            axOutputHeader = [
              guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ",
              guStackAtExceptionColumnIndicatorColor, "╷ "
            ],
            uLineNumberColor = guLineNumberColor,
            uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
            uActiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
          );
          aasConsoleOutputLines += [
            [
              guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ", 
              guStackAtExceptionColumnIndicatorColor,
                "┌",
                "╴" * (uEndLineNumberSize + uStartIndex + 1),
                "╮",
            ]
          ];
        if oException.lineno < oException.end_lineno:
          aasConsoleOutputLines += faasCreateConsoleOutputForSourceCode(
            sSourceFilePath = oException.filename,
            uStartLineNumber = oException.end_lineno,
            uEndLineNumber = oException.end_lineno + 1,
            axOutputHeader = [
              guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ",
              guStackAtExceptionColumnIndicatorColor, "╷ "
            ],
            uLineNumberColor = guLineNumberColor,
            uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
            uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
          );
        else:
          aasConsoleOutputLines += faasCreateConsoleOutputForSourceCode(
            sSourceFilePath = oException.filename,
            uStartLineNumber = oException.lineno - 1,
            uEndLineNumber = oException.end_lineno + 1,
            axOutputHeader = [guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ "],
            uLineNumberColor = guLineNumberColor,
            uInactiveCodeColor = guStackAtExceptionInactiveSourceCodeColor,
            uActiveCodeColor = guStackAtExceptionActiveSourceCodeColor,
          );
          uHighlightLength = oException.end_offset - oException.offset if bEndOffsetIsValid else 1;
          aasConsoleOutputLines += [
            [
              guStackTreeColor, " ╷" * uCurrentFrameIndex, " │ ", 
              guStackAtExceptionColumnIndicatorColor,
                "╭",
                "╴" * (uEndLineNumberSize + uStartIndex - 1),
                [
                  "┘",
                  "╴"  * (uHighlightLength - 1) # 0 or greater because `uHighlightLength > 1` in following line
                ] if oException.lineno == oException.end_lineno and uHighlightLength > 1 else [],
                "╯"
            ]
          ];
        if oException.offset:
          sException = "%s(%s at character %d)" % (oException.__class__.__name__, repr(oException.msg), oException.offset);
        else:
          sException = "%s(%s)" % (oException.__class__.__name__, repr(oException.msg));
    elif isinstance(oException, AssertionError):
      if oException.args:
        sException = "Assertion failed: %s" % ", ".join(repr(xArg) for xArg in oException.args);
      else:
        sException = "Assertion failed";
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
