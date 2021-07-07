import re;

from ..mColors import *;

def fdxExceptionDetailsForImportError(oException):
  if len(oException.args) != 1:
    return {
      "bShowLocals": False, # These won't provide useful information.
    };
  oErrorMessageMatch = re.match(r"^cannot import name (\w+)$", oException.args[0]);
  if not oErrorMessageMatch:
    return {
      "bShowLocals": False, # These won't provide useful information.
    };
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "An import failed because the module does not have a member named ",
        guExceptionInformationHighlightColor, oErrorMessageMatch.group(1),
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    }, 
    "bShowLocals": False,
  };
