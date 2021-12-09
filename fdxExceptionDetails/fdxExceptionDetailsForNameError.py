import re;

def fdxExceptionDetailsForNameError(oException):
  if len(oException.args) < 1:
    return {};
  sVariableName = oException.name;
  # Old code used in Python 2 to get the name from the error message:
  # oUnknownVariableErrorMessageMatch = re.match(r"^(?:global )?name '([_\w]+)' is not defined$", oException.args[0]);
  # if not oUnknownVariableErrorMessageMatch:
  #   return {};
  # sVariableName = oUnknownVariableErrorMessageMatch.group(1);
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Undefined variable ",
        guExceptionInformationHighlightColor, sVariableName, 
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "name": oException.name,
      "with_traceback": oException.with_traceback,
    },
  };

from ..mColorsAndChars import *;

