import sys;

from .HideInCallStack import HideInCallStack;

@HideInCallStack
def fTerminateWithException(oException, uExitCode, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  fConsoleOutputExceptionDetails(oException, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False)
  sys.exit(uExitCode);

from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;

