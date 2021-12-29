import re;

def fdxExceptionDetailsForNameError(oException):
  if len(oException.args) != 1:
    return {};
  dxHiddenProperties = {
    "args": oException.args,
    "with_traceback": oException.with_traceback,
  };
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
    # Python behavior is inconsistent; the property "name" may or may not exist.
    if hasattr(oException, "name"):
      if sVariableName != oException.name:
        return {}; # Sanity check.
      dxHiddenProperties["name"] = oException.name;
    sProblemDescription = "Undefined variable";
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, sProblemDescription, " ",
        guExceptionInformationHighlightColor, sVariableName, 
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": dxHiddenProperties,
  };

from ..mColorsAndChars import *;

