import re;

from .mColors import *;

def fdxExceptionDetailsForUnboundLocalError(oException):
  oUninitializedVariableErrorMessageMatch = re.match(r"^local variable '([_\w]+)' referenced before assignment$", oException.message);
  if not oUninitializedVariableErrorMessageMatch:
    return {};
  sVariableName = oUninitializedVariableErrorMessageMatch.group(1);
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Use of uninitialized variable ",
        guExceptionInformationHighlightColor, sVariableName, 
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": {
      "message": oException.message,
      "args": (oException.message,),
    },
  };
