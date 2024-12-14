import os, sys, traceback;

def fTerminateWithException(
  oException,
  uExitCode = 1, # default for internal exceptions in all my scripts.
  a0asAdditionalConsoleOutputLines = None,
  bShowStacksForAllThread = False,
  bPauseBeforeExit = False,
):
  if isinstance(oException, RecursionError):
    sys.setrecursionlimit(sys.getrecursionlimit() + 100);
  try:
    fConsoleOutputExceptionDetails(
      oException,
      a0asAdditionalConsoleOutputLines = a0asAdditionalConsoleOutputLines,
      bShowStacksForAllThread = bShowStacksForAllThread,
    );
  except Exception as oInternalException:
    print("*** INTERNAL EXCEPTION IN EXCEPTION HANDLER ***");
    print("Original exception: %s" % repr(oException));
    print(traceback.format_exc());
  finally:
    if bPauseBeforeExit:
      input("Press any key to exit...");
    os._exit(uExitCode);

from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;

