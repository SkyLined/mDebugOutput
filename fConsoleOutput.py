from .foConsoleLoader import foConsoleLoader;

def fConsoleOutput(sTitle, aasConsoleOutputLines):
  oConsole = foConsoleLoader();
  oConsole.fLock();
  try:
    oConsole.fOutput(guBoxColor, "┌───[", guBoxTitleColor, " ", sTitle, " ", guBoxColor, "]", sPadding = "─");
    for asConsoleOutputLine in aasConsoleOutputLines:
      oConsole.fOutput(guBoxColor, "│ ", *asConsoleOutputLine);
    oConsole.fOutput(guBoxColor, "└", sPadding = "─");
  finally:
    oConsole.fUnlock();
  

from .mColorsAndChars import *;
