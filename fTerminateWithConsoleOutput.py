import os;

from fConsoleOutput import fConsoleOutput;

def fTerminateWithConsoleOutput(sTitle, aasConsoleOutputLines):
  fConsoleOutput(sTitle, aasConsoleOutputLines);
  os._exit(3);

