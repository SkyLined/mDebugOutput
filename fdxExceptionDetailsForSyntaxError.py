from .mColors import *;

def fdxExceptionDetailsForSyntaxError(oException):
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Syntax error in ", guExceptionInformationHighlightColor, str(oException.filename),
        guExceptionInformationColor, " on line ", guExceptionInformationHighlightColor, str(oException.lineno),
        guExceptionInformationColor, ", column ", guExceptionInformationHighlightColor, str(oException.offset),
        guExceptionInformationColor, ".",
      ],
    ],
    "dxHiddenProperties": {
      "args": ('invalid syntax', (oException.filename, oException.lineno, oException.offset, oException.text)),
      "filename": oException.filename,
      "lineno": oException.lineno,
      "message": '',
      "msg": 'invalid syntax',
      "offset": oException.offset,
      "print_file_and_line": None,
      "text": oException.text,
    },
    "bShowLocals": False,
  };
