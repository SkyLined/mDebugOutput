import os, threading;

from oConsole import oConsole;

from .mColors import *;

def fTerminateWithConsoleOutput(sTitle, aasConsoleOutputLines):
  oConsole.fLock();
  try:
    oConsole.fPrint(guBoxColor, "\xDA\xC4\xC4[ ", guBoxTitleColor, sTitle, guBoxColor, " ]", sPadding = "\xC4");
    for asConsoleOutputLine in aasConsoleOutputLines:
      oConsole.fPrint(guBoxColor, "\xB3 ", *asConsoleOutputLine);
    oConsole.fPrint(guBoxColor, "\xC0", sPadding = "\xC4");
    os._exit(3);
  finally:
    oConsole.fUnlock();
  

