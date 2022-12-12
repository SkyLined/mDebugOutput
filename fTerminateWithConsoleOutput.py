import os;

from .fConsoleOutput import fConsoleOutput;

def fTerminateWithConsoleOutput(
  sTitle,
  aasConsoleOutputLines,
  uExitCode = 0, # assume there is no error
  bPauseBeforeExit = False,
):
  fConsoleOutput(
    sTitle,
    aasConsoleOutputLines,
  );
  if bPauseBeforeExit:
    input("Press any key to exit...");
  os._exit(uExitCode);

