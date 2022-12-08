import re;

def fdxExceptionDetailsForNameError(oException):
  if len(oException.args) != 1:
    return {};
  oNameErrorMessageMatch = re.match(r"^(?:global )?name '([_\w]+)' is not defined$", oException.args[0]);
  if not oNameErrorMessageMatch:
    return {};
  sVariableName = oNameErrorMessageMatch.group(1);
  # Python behavior is inconsistent; the property "name" may or may not exist.
  # In addition it may be None even if the name of the variable is known.
  dxHiddenProperties = {
    "args": oException.args,
    "with_traceback": oException.with_traceback,
    "add_note": oException.add_note,
  };
  if hasattr(oException, "name"):
    dxHiddenProperties["name"] = sVariableName if oException.name is not None else None;
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Undefined variable ",
        guExceptionInformationHighlightColor, sVariableName, 
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": dxHiddenProperties,
  };

from ..mColorsAndChars import *;

