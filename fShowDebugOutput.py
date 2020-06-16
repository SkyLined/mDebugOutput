from .fDebugOutputHelper import fDebugOutputHelper;
from .mGlobals import *;
from .cCallStack import cCallStack;
from .fTerminateWithException import fTerminateWithException;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;

def fShowDebugOutput(sMessage):
  try:
    oActiveFrame = cCallStack.cFrame.foForThisFunctionsCaller();
    if fbIsDebugOutputEnabledForSourceFilePathAndClass(oActiveFrame.sSourceFilePath, oActiveFrame.cClass):
      fDebugOutputHelper(
        oActiveFrame.uThreadId, oActiveFrame.sThreadName,
        oActiveFrame.sSourceFilePath, oActiveFrame.uLastExecutedLineNumber,
        sMessage
      );
  except Exception as oException:
    fTerminateWithException(oException);

