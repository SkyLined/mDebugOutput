def fdxExceptionDetailsForUnicodeDecodeError(oException):
  sInputString = oException.object;
  sOffensiveChars = sInputString[oException.start: oException.end];
  bInputIsUnicode = isinstance(sInputString, str);
  aasConsoleOutputLines = [
    [
      guExceptionInformationColor, "Cannot decode characters in string at offset ",
      guExceptionInformationHighlightColor, str(oException.start),
      guExceptionInformationColor, " because ",
      guExceptionInformationHighlightColor, fsToString(oException.reason),
      guExceptionInformationColor, ".",
    ], [
      guExceptionInformationColor, "The offensive character", " is" if len(sOffensiveChars) == 1 else "s are", ":",
    ], [
      guExceptionInformationHighlightColor, "  ", fsToString(sOffensiveChars),
    ], [
      guExceptionInformationColor, "  (Hex: ",
      guExceptionInformationHighlightColor, " ".join([
        ("%04X" if bInputIsUnicode else "%02X") % ord(sChar)
        for sChar in sOffensiveChars
      ]),
      guExceptionInformationColor, ")",
    ], [
      guExceptionInformationColor, "The input string was:",
    ],
  ];
  # Put a caret under the location of the error.
  sHumanReadbleInputString = fsToString(sInputString, uMaxLength = 200);
  sHumanReadbleInputStringUpToOffensiveCharacters = fsToString(sInputString[:oException.start], uMaxLength = 200)[:-1];
  if len(sHumanReadbleInputStringUpToOffensiveCharacters) < 1000:
    sHumanReadbleOffensiveCharacters = fsToString(sOffensiveChars, uMaxLength = 200)[1:-1];
    sHumanReadbleInputStringAfterOffensiveCharacters = fsToString(sInputString[oException.end:], uMaxLength = 200)[1:];
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
        guExceptionInformationColor, "  ", fsToString(sInputString, 1000),
     ],
    );
  
  dxHiddenProperties = {
    "args": (oException.encoding, oException.object, oException.start, oException.end, oException.reason),
    "with_traceback": oException.with_traceback,
    "encoding": oException.encoding,
    "end": oException.end,
    "object": oException.object,
    "reason": oException.reason,
    "start": oException.start,
  };

from ..mColorsAndChars import *;
from ..fsToString import fsToString;
