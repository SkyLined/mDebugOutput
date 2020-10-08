from .mColors import *;
def fConsoleOutput(sTitle, aasConsoleOutputLines):
  # Lazy load to prevent depency loops.
  from oConsole import oConsole;
  oConsole.fLock();
  try:
    oConsole.fPrint(guBoxColor, "\xDA\xC4\xC4[ ", guBoxTitleColor, sTitle, guBoxColor, " ]", sPadding = "\xC4");
    for asConsoleOutputLine in aasConsoleOutputLines:
      oConsole.fPrint(guBoxColor, "\xB3 ", *asConsoleOutputLine);
    oConsole.fPrint(guBoxColor, "\xC0", sPadding = "\xC4");
  finally:
    oConsole.fUnlock();
  

