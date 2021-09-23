import sys;

from .fConsoleOutput import fConsoleOutput;

def fTerminateWithConsoleOutput(sTitle, aasConsoleOutputLines, uExitCode = 3):
  fConsoleOutput(sTitle, aasConsoleOutputLines);
  sys.exit(uExitCode);

