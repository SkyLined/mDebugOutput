from .cFrame import cFrame;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;
from .fDebugOutputHelper import fDebugOutputHelper;
from .fTerminateWithException import fTerminateWithException;
from .mGlobals import *;
guExitCodeInternalError = 1; # This is the common default I use. There's currently no good way to set this per application.

def fShowDebugOutput(oObject_or_sMessage, s0Message = None):
  if s0Message is not None:
    sMessage = s0Message;
    o0Object = oObject_or_sMessage;
  else:
    sMessage = oObject_or_sMessage;
    o0Object = None;
  try:
    o0ActiveFrame = cFrame.fo0ForCurrentThreadAndFunctionCaller();
    assert o0ActiveFrame, \
        "You cannot use fDebugOutput if all functions on the stack are hidden!";
    if fbIsDebugOutputEnabledForSourceFilePathAndClass(o0ActiveFrame.sSourceFilePath, o0Object.__class__ if o0Object else o0ActiveFrame.cClass):
      fDebugOutputHelper(
        o0ActiveFrame.u0ThreadId, o0ActiveFrame.s0ThreadName,
        o0ActiveFrame.sSourceFilePath, o0ActiveFrame.uLastExecutedLineNumber,
        sMessage
      );
  except Exception as oException:
    fTerminateWithException(oException, guExitCodeInternalError);
