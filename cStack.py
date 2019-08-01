import os, re, sys, threading, traceback;

class cStackEntry(object):
  def __init__(oSelf, uCallerIndex, uStackIndex, uThreadId):
    oSelf.uStackIndex = uStackIndex;
    oSelf.uThreadId = uThreadId;
    
    atsStack = traceback.extract_stack(limit = 3 + uCallerIndex + 1);
    (sCallersCallerFilePath, uCallersCallerLineNumber, sCallersCallerFunctionName, sCallersCallerSource) = atsStack[0];
    (sCallerFilePath, uCallerLineNumber, sCallerFunctionName, sCallerSource) = atsStack[1];
    
    # sCallingFunction identifies the function that made the call that created this stack entry.
    oSelf.sCallingFunction = sCallersCallerFunctionName;
    # sCallLocation identifies where the call was made.
    oSelf.sCallLocation = "%s/%d" % (os.path.basename(sCallersCallerFilePath), uCallersCallerLineNumber);
    # sCurrentFunction identifies the function that was called.
    oSelf.sCurrentFunction = sCallerFunctionName;
    # sCurrentLocation identifies where code is currently being executed.
    oSelf.sCurrentLocation = "%s/%d" % (os.path.basename(sCallerFilePath), uCallerLineNumber);
    oSelf.sFilePath = sCallerFilePath;
    # sId uniquely identifies that caller.
    oSelf.sId = "%s @ %s" % (sCallerFunctionName, sCallerFilePath);
  
  @property
  def bShowDebugOutput(oSelf):
    return cStack.fbShowDebugOutputForEntry(oSelf);

class cStack(object):
  # STATIC
  oThreadStacksLock = threading.Lock();
  doStack_by_uThreadId = {};
  
  __asShowDebugOutputForFilePaths = [];
  bShowAllOutput = False;
  
  @staticmethod
  def fShowFileDebugOutput(sFilePath):
    cStack.__asShowDebugOutputForFilePaths.append(sFilePath);
  
  @staticmethod
  def fShowFileDebugOutputForClass(cClass):
    cStack.fShowFileDebugOutput(sys.modules[cClass.__module__].__file__);
  
  @staticmethod
  def fbShowDebugOutputForEntry(oStackEntry):
    return cStack.bShowAllOutput or oStackEntry.sFilePath in cStack.__asShowDebugOutputForFilePaths;
  
  @staticmethod
  def foGetThreadStack():
    uThreadId = threading.currentThread().ident;
    cStack.oThreadStacksLock.acquire();
    try:
      oStack = cStack.doStack_by_uThreadId.get(uThreadId);
      if not oStack:
        oStack = cStack.doStack_by_uThreadId[uThreadId] = cStack(uThreadId);
    finally:
      cStack.oThreadStacksLock.release();
    return oStack;

  @staticmethod
  def foPushCaller(uCallerIndex):
    oStack = cStack.foGetThreadStack();
    return oStack.__foPushCaller(uCallerIndex + 1);
  
  @staticmethod
  def foGetCaller(uCallerIndex):
    oStack = cStack.foGetThreadStack();
    return oStack.__foGetCaller(uCallerIndex + 1);
  
  @staticmethod
  def foPopCaller(uCallerIndex):
    oStack = cStack.foGetThreadStack();
    oCaller = oStack.__foPopCaller(uCallerIndex + 1);
    if len(oStack.aoStackEntries) == 0:
      cStack.oThreadStacksLock.acquire();
      try:
        del cStack.doStack_by_uThreadId[oStack.uThreadId];
      finally:
        cStack.oThreadStacksLock.release();
    return oCaller;
  # INSTANCE
  def __init__(oSelf, uThreadId):
    oSelf.uThreadId = uThreadId;
    oSelf.oTop = None;
    oSelf.aoStackEntries = [];
    oSelf.uVisibleStackEntries = 0;
  
  def __foPushCaller(oSelf, uCallerIndex):
    oCaller = oSelf.oTop = cStackEntry(uCallerIndex + 1, oSelf.uVisibleStackEntries, oSelf.uThreadId);
    if oSelf.fbShowDebugOutputForEntry(oCaller):
      oSelf.uVisibleStackEntries += 1;
    oSelf.aoStackEntries.append(oCaller);
    return oCaller;
  
  def __foGetCaller(oSelf, uCallerIndex):
    oCaller = cStackEntry(uCallerIndex + 1, oSelf.uVisibleStackEntries - 1, oSelf.uThreadId);
    oLastCaller = oSelf.aoStackEntries[-1];
    assert oCaller.sId == oLastCaller.sId, \
        "%s != %s" % (oCaller.sId, oLastCaller.sId);
    return oCaller;
  
  def __foPopCaller(oSelf, uCallerIndex):
    oCaller = cStackEntry(uCallerIndex + 1, oSelf.uVisibleStackEntries - 1, oSelf.uThreadId);
    if oSelf.fbShowDebugOutputForEntry(oCaller):
      oSelf.uVisibleStackEntries -= 1;
    oLastCaller = oSelf.aoStackEntries.pop();
    assert oCaller.sId == oLastCaller.sId, \
        "%s != %s" % (oCaller.sId, oLastCaller.sId);
    return oCaller;
  
