import re;

from .mColors import *;

def fdxExceptionDetailsForImportError(oException):
  oErrorMessageMatch = re.match(r"^cannot import name (\w+)$", oException.message);
  if not oErrorMessageMatch:
    return {
      "bShowLocals": False, # These won't provide useful information.
    };
  else:
    return {
      "aasConsoleOutputLines": [
        [
          guExceptionInformationColor, "An import failed because the module does not have a member named ",
          guExceptionInformationHighlightColor, oErrorMessageMatch.group(1),
          guExceptionInformationColor, ".",
        ],
      ],
      "dxHiddenProperties": {
        "message": oException.message,
        "args": (oException.message,),
      }, 
      "bShowLocals": False,
    };
