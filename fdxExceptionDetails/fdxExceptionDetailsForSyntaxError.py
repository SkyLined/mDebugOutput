def fdxExceptionDetailsForSyntaxError(oException):
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationColor, "Syntax error in ", guExceptionInformationHighlightColor, str(oException.filename),
        [
          guExceptionInformationColor, " starting on line ",
          guExceptionInformationHighlightColor, str(oException.lineno),
          guExceptionInformationColor, ", column ",
          guExceptionInformationHighlightColor, str(oException.offset),
          guExceptionInformationColor, " and ending on line ",
          guExceptionInformationHighlightColor, str(oException.end_lineno),
          guExceptionInformationColor, ", column ",
          guExceptionInformationHighlightColor, str(oException.end_offset),
        ] if oException.lineno != oException.end_lineno else [
          guExceptionInformationColor, " on line ",
          guExceptionInformationHighlightColor, str(oException.lineno),
          guExceptionInformationColor, ", starting at column ",
          guExceptionInformationHighlightColor, str(oException.offset),
          guExceptionInformationColor, " and ending at column ",
          guExceptionInformationHighlightColor, str(oException.end_offset),
        ] if oException.end_offset - oException.offset > 1 else [
          guExceptionInformationColor, " on line ",
          guExceptionInformationHighlightColor, str(oException.lineno),
          guExceptionInformationColor, ", column ", guExceptionInformationHighlightColor, str(oException.offset),
        ],
        guExceptionInformationColor, ":",
      ],
      [
        guExceptionInformationColor, oException.msg,
      ],
    ],
    "dxHiddenProperties": {
      "args": (oException.msg, (oException.filename, oException.lineno, oException.offset, oException.text, oException.end_lineno, oException.end_offset)),
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
      "filename": oException.filename,
      "lineno": oException.lineno,
      "end_lineno": oException.end_lineno,
      "msg": oException.msg,
      "offset": oException.offset,
      "end_offset": oException.end_offset,
      "print_file_and_line": None,
      "text": oException.text,
    },
    "bShowLocals": False,
  };

from ..mColorsAndChars import *;

