from .cFrame import cFrame;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;
from .fDebugOutputHelper import fDebugOutputHelper;
from .fTerminateWithException import fTerminateWithException;
from .mGlobals import *;
guExitCodeInternalError = 1; # This is the common default I use. There's currently no good way to set this per application.

def fShowDebugOutput(sMessage):
  try:
    o0ActiveFrame = cFrame.fo0ForCurrentThreadAndFunctionCaller();
    assert o0ActiveFrame, \
        "You cannot use fDebugOutput if all functions on the stack are hidden!";
    if fbIsDebugOutputEnabledForSourceFilePathAndClass(o0ActiveFrame.sSourceFilePath, o0ActiveFrame.cClass):
      fDebugOutputHelper(
        o0ActiveFrame.u0ThreadId, o0ActiveFrame.s0ThreadName,
        o0ActiveFrame.sSourceFilePath, o0ActiveFrame.uLastExecutedLineNumber,
        sMessage
      );
  except Exception as oException:
    fTerminateWithException(oException, guExitCodeInternalError);

