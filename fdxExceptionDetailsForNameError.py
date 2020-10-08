import re;

from .mColors import *;

def fdxExceptionDetailsForNameError(oException):
  oUnknownVariableErrorMessageMatch = re.match(r"^(?:global )?name '([_\w]+)' is not defined$", oException.message);
  if not oUnknownVariableErrorMessageMatch:
    return {};
  sVariableName = oUnknownVariableErrorMessageMatch.group(1);
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Undefined variable ",
        guExceptionInformationHighlightColor, sVariableName, 
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": {
      "message": oException.message,
      "args": (oException.message,),
    },
  };
