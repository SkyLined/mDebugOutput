import re;

def fdxExceptionDetailsForUnboundLocalError(oException):
  if len(oException.args) != 1:
    return {};
  oUnboundLocalErrorMessageMatch = re.match(
    r"^("
      r"local variable '([_\w]+)' referenced before assignment"
    r"|"
      r"cannot access local variable '([_\w]+)' where it is not associated with a value"
    r")$",
    oException.args[0],
  );
  if not oUnboundLocalErrorMessageMatch:
    return {};
  sVariableName = oUnboundLocalErrorMessageMatch.group(1) or oUnboundLocalErrorMessageMatch.group(2);
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
        guExceptionInformationColor, "Uninitialised variable ",
        guExceptionInformationHighlightColor, sVariableName, 
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": dxHiddenProperties,
  };

from ..mColorsAndChars import *;

