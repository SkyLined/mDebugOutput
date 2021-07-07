from .mColors import *;
from .foConsoleLoader import foConsoleLoader;

def fConsoleOutput(sTitle, aasConsoleOutputLines):
  oConsole = foConsoleLoader();
  oConsole.fLock();
  try:
    oConsole.fOutput(guBoxColor, "\u250C\u2500\u2500[ ", guBoxTitleColor, sTitle, guBoxColor, " ]", sPadding = "\u2500");
    for asConsoleOutputLine in aasConsoleOutputLines:
      oConsole.fOutput(guBoxColor, "\u2502 ", *asConsoleOutputLine);
    oConsole.fOutput(guBoxColor, "\u2514", sPadding = "\u2500");
  finally:
    oConsole.fUnlock();
  

