import re, sys;

def fdxExceptionDetailsForValueError(oException):
  if len(oException.args) != 1:
    return {};
  oTooManyValuesInTupleMatch = re.match(r"^too many values to unpack \(expected (\d+)\)$", oException.args[0]);
  if oTooManyValuesInTupleMatch:
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "Expected ",
        guExceptionInformationHighlightColor, oTooManyValuesInTupleMatch.group(1), 
        guExceptionInformationColor, " values in tuple but got more than that.",
      ],
    ];
  else:
    oTooFewValuesInTupleMatch = re.match(r"^not enough values to unpack \(expected (\d+), got (\d+)\)$", oException.args[0]);
    if oTooFewValuesInTupleMatch:
      aasConsoleOutputLines = [
        [
          guExceptionInformationColor, "Expected ",
          guExceptionInformationHighlightColor, oTooFewValuesInTupleMatch.group(1), 
          guExceptionInformationColor, " values in tuple but got only ",
          guExceptionInformationHighlightColor, oTooFewValuesInTupleMatch.group(2), 
          guExceptionInformationColor, ".",
        ],
      ];
    else:
      return {};
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };

from ..ShowDebugOutput import ShowDebugOutput;
from ..mColorsAndChars import *;
