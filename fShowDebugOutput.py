from .fDebugOutputHelper import fDebugOutputHelper;
from .mGlobals import *;
from .cFrame import cFrame;
from .fTerminateWithException import fTerminateWithException;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;

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

