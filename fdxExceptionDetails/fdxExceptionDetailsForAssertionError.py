from ..mColors import *;

def fdxExceptionDetailsForAssertionError(oException):
  if len(oException.args) != 1:
    return {};
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationHighlightColor, oException.args[0],
      ],
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };
