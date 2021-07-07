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
    return {};
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };

from ..ShowDebugOutput import ShowDebugOutput;
from ..mColors import *;
