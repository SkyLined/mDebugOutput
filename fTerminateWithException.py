import os;

def fTerminateWithException(
  oException,
  uExitCode = 1, # default for internal exceptions in all my scripts.
  a0asAdditionalConsoleOutputLines = None,
  bShowStacksForAllThread = False,
  bPauseBeforeExit = False,
):
  try:
    fConsoleOutputExceptionDetails(
      oException,
      a0asAdditionalConsoleOutputLines = a0asAdditionalConsoleOutputLines,
      bShowStacksForAllThread = bShowStacksForAllThread,
    );
  finally:
    if bPauseBeforeExit:
      input("Press any key to exit...");
    os._exit(uExitCode);

from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;

