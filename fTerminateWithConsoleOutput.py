import os;

from .fConsoleOutput import fConsoleOutput;

def fTerminateWithConsoleOutput(sTitle, aasConsoleOutputLines, uExitCode = 3):
  fConsoleOutput(sTitle, aasConsoleOutputLines);
  os._exit(uExitCode);

