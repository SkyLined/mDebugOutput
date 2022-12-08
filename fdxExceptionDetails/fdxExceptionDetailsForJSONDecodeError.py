import re, sys;

guMaxNumberOfLinesToShow = 5;

def fdxExceptionDetailsForJSONDecodeError(oException):
  if len(oException.args) != 1:
    return {};
  s0JSONString = getattr(oException, "doc");
  u0ColumnNumber = getattr(oException, "colno");
  u0LineNumber = getattr(oException, "lineno");
  s0Message = getattr(oException, "msg");
  if s0JSONString is None or u0ColumnNumber is None or u0LineNumber is None or s0Message is None:
    return {};
  asJSONLines = s0JSONString.split("\n");
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
      guExceptionInformationHighlightColor, "Relevant JSON line", "s" if uFromLineIndex < uErrorLineIndex else "", ":",
    ],
  ];
  for uIndex in range(uFromLineIndex, uErrorLineIndex + 1):
    sJSONLine = asJSONLines[uIndex];
    aasConsoleOutputLines.append(
      [
        guExceptionInformationColor, str(uIndex + 1).ljust(uMaxIndexLength), " |",
        [
          guExceptionInformationHighlightColor, sJSONLine[:uErrorColumnIndex],
          guExceptionInformationErrorColor, sJSONLine[uErrorColumnIndex:],
        ] if uIndex == uErrorLineIndex else [
          guExceptionInformationHighlightColor, sJSONLine
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
      "doc": oException.doc,
      "lineno": oException.lineno,
      "msg": oException.msg,
      "pos": oException.pos,
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
    },
  };

from ..ShowDebugOutput import ShowDebugOutput;
from ..mColorsAndChars import *;
