from .cFrame import cFrame;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;
from .fDebugOutputHelper import fDebugOutputHelper;
from .fTerminateWithException import fTerminateWithException;
from .mGlobals import *;
guExitCodeInternalError = 1; # This is the common default I use. There's currently no good way to set this per application.

def fShowDebugOutput(sMessage):
  try:
    oActiveFrame = cFrame.foForThisFunctionsCaller();
#    print "@@ %s" % (oActiveFrame.fsToString(),);
    if fbIsDebugOutputEnabledForSourceFilePathAndClass(oActiveFrame.sSourceFilePath, oActiveFrame.cClass):
      
      fDebugOutputHelper(
        oActiveFrame.u0ThreadId, oActiveFrame.s0ThreadName,
        oActiveFrame.sSourceFilePath, oActiveFrame.uLastExecutedLineNumber,
        sMessage
      );
  except Exception as oException:
    fTerminateWithException(oException, guExitCodeInternalError);

