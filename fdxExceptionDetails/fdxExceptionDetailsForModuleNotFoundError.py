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
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
      "msg": oException.msg,
      "name": oException.name,
      "name_from": None, # This is undocumented - I've only seen this set to None.
      "path": oException.path, # Currently not shown - I've only seen this set to None.
    }, 
    "bShowLocals": False,
  };

from ..mColorsAndChars import *;

