import re;

def fdxExceptionDetailsForModuleNotFoundError(oException):
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "An import failed because the module ",
        guExceptionInformationHighlightColor, oException.name,
        guExceptionInformationColor, " can not be found.",
      ],
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "msg": oException.msg,
      "name": oException.name,
      "path": oException.path, # Currently not shown - I've only seen this set to None.
      "with_traceback": oException.with_traceback,
    }, 
    "bShowLocals": False,
  };

from ..mColorsAndChars import *;

