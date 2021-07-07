from ..mColors import *;

def fdxExceptionDetailsForSyntaxError(oException):
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Syntax error in ", guExceptionInformationHighlightColor, str(oException.filename),
        guExceptionInformationColor, " on line ", guExceptionInformationHighlightColor, str(oException.lineno),
        guExceptionInformationColor, ", column ", guExceptionInformationHighlightColor, str(oException.offset),
        guExceptionInformationColor, ":",
      ],
      [
        guExceptionInformationColor, "\u25BA ", oException.msg,
      ],
    ],
    "dxHiddenProperties": {
      "args": (oException.msg, (oException.filename, oException.lineno, oException.offset, oException.text)),
      "with_traceback": oException.with_traceback,
      "filename": oException.filename,
      "lineno": oException.lineno,
      "msg": oException.msg,
      "offset": oException.offset,
      "print_file_and_line": None,
      "text": oException.text,
    },
    "bShowLocals": False,
  };
