import re;

from .mColors import *;

def fdxExceptionDetailsForAttributeError(oException):
  oErrorMessageMatch = re.match(r"^'(\w+)' object has no attribute '(\w+)'$", oException.message);
  if not oErrorMessageMatch:
    return {};
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationHighlightColor, oErrorMessageMatch.group(1),
        guExceptionInformationColor, " instance has no attribute ",
        guExceptionInformationHighlightColor, oErrorMessageMatch.group(2),
        guExceptionInformationColor, ":"
      ],
    ],
    "dxHiddenProperties": {
      "message": oException.message,
      "args": (oException.message,),
    },
  };
