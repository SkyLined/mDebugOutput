import re;

from ..mColors import *;

def fdxExceptionDetailsForUnboundLocalError(oException):
  if len(oException.args) != 1:
    return {};
  oUninitializedVariableErrorMessageMatch = re.match(r"^local variable '([_\w]+)' referenced before assignment$", oException.args[0]);
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
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };
