from .cFrame import cFrame;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;
from .fDebugOutputHelper import fDebugOutputHelper;
from .fTerminateWithException import fTerminateWithException;
from .mGlobals import *;

def fShowDebugOutput(sMessage):
  try:
    oActiveFrame = cFrame.foForThisFunctionsCaller();
#    print "@@ %s" % (oActiveFrame.fsToString(),);
    if fbIsDebugOutputEnabledForSourceFilePathAndClass(oActiveFrame.sSourceFilePath, oActiveFrame.cClass):
      
      fDebugOutputHelper(
        oActiveFrame.uThreadId, oActiveFrame.sThreadName,
        oActiveFrame.sSourceFilePath, oActiveFrame.uLastExecutedLineNumber,
        sMessage
      );
  except Exception as oException:
    fTerminateWithException(oException);

