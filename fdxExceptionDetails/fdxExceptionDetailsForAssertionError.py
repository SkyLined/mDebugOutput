
def fdxExceptionDetailsForAssertionError(oException):
  if len(oException.args) != 1:
    return {};
  return {
    "aasConsoleOutputLines": [
      [ guExceptionInformationHighlightColor, sLine.rstrip("\r") ]
      for sLine in oException.args[0].split("\n")
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };

from ..mColorsAndChars import *;

