def fdxExceptionDetailsForUnicodeDecodeError(oException):
  sxInputString = oException.object;
  sxOffensiveChars = sxInputString[oException.start: oException.end];
  bInputIsUnicode = isinstance(sxInputString, str);
  aasConsoleOutputLines = [
    [
      guExceptionInformationColor, "Cannot decode characters in string at offset ",
      guExceptionInformationHighlightColor, str(oException.start),
      guExceptionInformationColor, " because ",
      guExceptionInformationHighlightColor, fsToString(oException.reason),
      guExceptionInformationColor, ".",
    ], [
      guExceptionInformationColor, "The offensive character", " is" if len(sxOffensiveChars) == 1 else "s are", ":",
    ], [
      guExceptionInformationHighlightColor, "  ", fsToString(sxOffensiveChars),
    ], [
      guExceptionInformationColor, "  (Hex: ",
      guExceptionInformationHighlightColor, " ".join([
        ("%04X" % ord(xChar)) if bInputIsUnicode else # convert characters to an integer codepoints and print their hex values
        ("%02X") % xChar # bytes are already integers; print their hex value.
        for xChar in sxOffensiveChars
      ]),
      guExceptionInformationColor, ")",
    ], [
      guExceptionInformationColor, "The input string was:",
    ],
  ];
  # Put a caret under the location of the error.
  sHumanReadbleInputString = fsToString(sxInputString, uMaxLength = 200);
  sHumanReadbleInputStringUpToOffensiveCharacters = fsToString(sxInputString[:oException.start], uMaxLength = 200)[:-1];
  if len(sHumanReadbleInputStringUpToOffensiveCharacters) < 1000:
    sHumanReadbleOffensiveCharacters = fsToString(sxOffensiveChars, uMaxLength = 200)[1:-1];
    sHumanReadbleInputStringAfterOffensiveCharacters = fsToString(sxInputString[oException.end:], uMaxLength = 200)[1:];
    # Show input string with offensive characters highlighted.
    aasConsoleOutputLines.append(
      [
        guExceptionInformationColor, "  ", sHumanReadbleInputStringUpToOffensiveCharacters,
        guExceptionInformationErrorColor, sHumanReadbleOffensiveCharacters,
        guExceptionInformationColor, sHumanReadbleInputStringAfterOffensiveCharacters,
      ],
    );
  else:
    # String is too large to show additional useful information:
    aasConsoleOutputLines.append(
      [
        guExceptionInformationColor, "  ", fsToString(sxInputString, 1000),
      ],
    );
  
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": (oException.encoding, oException.object, oException.start, oException.end, oException.reason),
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
      "encoding": oException.encoding,
      "end": oException.end,
      "object": oException.object,
      "reason": oException.reason,
      "start": oException.start,
    },
  };

from ..mColorsAndChars import *;
from ..fsToString import fsToString;
