import re;

def fdxExceptionDetailsForNameError(oException):
  if len(oException.args) < 1:
    return {};
  oUnknownVariableErrorMessageMatch = re.match(r"^(?:global )?name '([_\w]+)' is not defined$", oException.args[0]);
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
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };

from ..mColorsAndChars import *;

