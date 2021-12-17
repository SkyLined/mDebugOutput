import re;

def fdxExceptionDetailsForNameError(oException):
  if len(oException.args) != 1:
    return {};
  if isinstance(oException, UnboundLocalError):
    oUnboundLocalErrorMessageMatch = re.match(r"^local variable '([_\w]+)' referenced before assignment$", oException.args[0]);
    if not oUnboundLocalErrorMessageMatch:
      return {};
    sVariableName = oUnboundLocalErrorMessageMatch.group(1);
    sProblemDescription = "Uninitialised variable";
  else:
    oNameErrorMessageMatch = re.match(r"^(?:global )?name '([_\w]+)' is not defined$", oException.args[0]);
    if not oNameErrorMessageMatch:
      return {};
    sVariableName = oNameErrorMessageMatch.group(1);
    if sVariableName != oException.name:
      return {}; # Sanity check.
    sProblemDescription = "Undefined variable";
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, sProblemDescription, " ",
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

