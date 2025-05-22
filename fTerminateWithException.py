import os, sys, traceback;

gbRecursionAvoidanceActive = False;

def fTerminateWithException(
  oException,
  uExitCode = 1, # default for internal exceptions in all my scripts.
  a0asAdditionalConsoleOutputLines = None,
  bShowStacksForAllThread = False,
  bPauseBeforeExit = False,
):
  # We're going to try to turn various values into a readable string, which
  # could results in additional exceptions. That can cause an infinite loop.
  # We will raise an assertion exception as soon as we are called recursively.
  # If all goes well, the code that attempted to turn the problematic value
  # into a string, will catch that exception and try a different way, or give
  # up. Either way, this should allow us to report _something_ even if
  # everything we touch is broken.
  global gbRecursionAvoidanceActive;
  assert not gbRecursionAvoidanceActive;
  gbRecursionAvoidanceActive = True;
  try:
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
      print(traceback.format_exc());
      print("Original exception: %s" % repr(oException));
    finally:
      if bPauseBeforeExit:
        input("Press any key to exit...");
      os._exit(uExitCode);
  finally:
    gbRecursionAvoidanceActive = False;

from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;

