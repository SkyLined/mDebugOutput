
def fdxExceptionDetailsForAssertionError(oException):
  if len(oException.args) != 1 or type(oException.args[0]) != str:
    return {};
  return {
    "aasConsoleOutputLines": [
      [ guExceptionInformationHighlightColor, sLine.rstrip("\r") ]
      for sLine in oException.args[0].split("\n")
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
    },
  };

from ..mColorsAndChars import *;

