import re;

def fdxExceptionDetailsForKeyError(oException):
  if len(oException.args) < 1:
    return {};
  sKeyName = oException.args[0];
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "The key ",
        guExceptionInformationHighlightColor, sKeyName, 
        guExceptionInformationColor, " was not found in a dictionary.",
      ],
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
    },
  };

from ..mColorsAndChars import *;

