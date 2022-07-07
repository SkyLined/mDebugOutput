guMaxNumberOfLinesToShow = 5;

def fdxExceptionDetailsForReError(oException):
  if len(oException.args) != 1:
    return {};
  sx0Pattern = getattr(oException, "pattern");
  s0Pattern = (
    sx0Pattern if isinstance(sx0Pattern, str) else 
    str(sx0Pattern, "ascii", "replace") if isinstance(sx0Pattern, bytes) else
    None
  );
  u0ColumnNumber = getattr(oException, "colno");
  u0LineNumber = getattr(oException, "lineno");
  s0Message = getattr(oException, "msg");
  if s0Pattern is None or u0ColumnNumber is None or u0LineNumber is None or s0Message is None:
    return {};
  asPatternLines = s0Pattern.split("\n");
  uErrorLineIndex = u0LineNumber - 1;
  uErrorColumnIndex = u0ColumnNumber - 1;
  uFromLineIndex = max(0, uErrorLineIndex - guMaxNumberOfLinesToShow);
  uMaxIndexLength = len(str(uErrorLineIndex));
  aasConsoleOutputLines = [
    [
      guExceptionInformationColor, s0Message, " on line ",
      guExceptionInformationHighlightColor, str(u0LineNumber), 
      guExceptionInformationColor, ", column ",
      guExceptionInformationHighlightColor, str(u0ColumnNumber), 
      guExceptionInformationColor, ".",
    ], [
    ], [
      guExceptionInformationHighlightColor, "Relevant pattern line", "s" if uFromLineIndex < uErrorLineIndex else "", ":",
    ],
  ];
  for uIndex in range(uFromLineIndex, uErrorLineIndex + 1):
    sPatternLine = asPatternLines[uIndex];
    aasConsoleOutputLines.append(
      [
        guExceptionInformationColor, str(uIndex + 1).ljust(uMaxIndexLength), " |",
        [
          guExceptionInformationHighlightColor, sPatternLine[:uErrorColumnIndex],
          guExceptionInformationErrorColor, sPatternLine[uErrorColumnIndex:],
        ] if uIndex == uErrorLineIndex else [
          guExceptionInformationHighlightColor, sPatternLine
        ],
      ]
    );
  aasConsoleOutputLines.append(
    [
      guExceptionInformationColor, " " * uMaxIndexLength, "  ", " " * uErrorColumnIndex,
      guExceptionInformationHighlightColor, "▲ ", str(oException.msg),
    ]
  );
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": oException.args,
      "colno": oException.colno,
      "lineno": oException.lineno,
      "msg": oException.msg,
      "pattern": oException.pattern,
      "pos": oException.pos,
      "with_traceback": oException.with_traceback,
    },
  };

from ..mColorsAndChars import *;
