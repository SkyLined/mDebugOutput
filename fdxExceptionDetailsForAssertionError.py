from .mColors import *;

def fdxExceptionDetailsForAssertionError(oException):
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationHighlightColor, oException.message,
      ],
    ],
    "dxHiddenProperties": {
      "message": oException.message,
      "args": (oException.message,),
    },
  };
