import os, traceback;

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
  except Exception as oInternalException:
    print("*** INTERNAL EXCEPTION IN EXCEPTION HANDLER ***");
    print(traceback.format_exc());
    print("Original exception: %s" % repr(oException));
  finally:
    if bPauseBeforeExit:
      input("Press any key to exit...");
    os._exit(uExitCode);

from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;

