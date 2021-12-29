import os;

def fTerminateWithException(oException, uExitCode, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  fConsoleOutputExceptionDetails(oException, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False)
  os._exit(uExitCode);

from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;

