import re;

def fdxExceptionDetailsForImportError(oException):
  oErrorMessageMatch = re.match(r"^cannot import name (\w+)$", oException.msg);
  if oErrorMessageMatch:
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "An import failed because the module does not have a member named ",
        guExceptionInformationHighlightColor, oErrorMessageMatch.group(1),
        guExceptionInformationColor, ".",
      ],
    ];
  elif oException.msg == "attempted relative import with no known parent package":
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "Relative imports are not possible from scripts that are not imported as modules.",
      ],
    ];
  else:
    return {
      "bShowLocals": False, # These won't provide useful information.
    };
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": (oException.msg,),
      "msg": oException.msg,
      "name": None,
      "path": oException.path, # Currently not shown - I've only seen this set to None.
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
    }, 
    "bShowLocals": False,
  };

from ..mColorsAndChars import *;

