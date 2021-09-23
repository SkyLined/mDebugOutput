from .mColorsAndChars import *;
# The rest of the imports are done at the bottom to prevent import loops.

def faasCreateConsoleOutputForSourceCode(
  sSourceFilePath,
  uStartLineNumber, uEndLineNumber,
  axOutputHeader = [],
  uLineNumberColor = guLineNumberColor,
  uInactiveCodeColor = guStackNormalInactiveSourceCodeColor,
  uActiveCodeColor = guStackNormalActiveSourceCodeColor,
):
  asModuleSourceCode = fasGetSourceCode(sSourceFilePath);
  aasConsoleOutputLines = [];
  uStartLineNumber = max(uStartLineNumber, 1);
  uEndLineNumber = min(uEndLineNumber, len(asModuleSourceCode) + 1);
  if uStartLineNumber < uEndLineNumber:
    uLineNumberSize = len(str(uEndLineNumber))
    for uLineNumber in range(uStartLineNumber, uEndLineNumber):
      sSourceCodeLine = asModuleSourceCode[uLineNumber - 1];
      uColor = uInactiveCodeColor if uLineNumber + 1 < uEndLineNumber else uActiveCodeColor;
      aasConsoleOutputLines += [
        axOutputHeader + [
          uLineNumberColor, str(uLineNumber).rjust(uLineNumberSize), ":",
          uColor, sSourceCodeLine
        ]
      ];
  return aasConsoleOutputLines;

from .fasGetSourceCode import fasGetSourceCode;
