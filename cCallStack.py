import inspect, os, sys, threading;

from .fasGetSourceCode import fasGetSourceCode;
from .fsGetClassAndFunctionForClassAndCode import fsGetClassAndFunctionForClassAndCode;
from .fsToString import fsToString;
from .ftocGetInstanceAndClassForUnknown import ftocGetInstanceAndClassForUnknown;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;
from .faasCreateConsoleOutputForSourceCode import faasCreateConsoleOutputForSourceCode;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .HideInCallStack import HideInCallStack;
from .mColors import *;

goPythonCode_by_mModule = {};
gfxFunction_by_oPythonCode = {};
gfxStaticOrClassMethod_by_oPythonCode = {};
gfClass_by_oPythonCode = {};

gbDebugDumpRawStacksAndTracebacks = False;

def fDumpPythonFrame(oPythonFrame, sPrefix = "", sSuffix = "", bExpand = True):
  sFlags = " ".join([s for s in [
    repr(oPythonFrame.f_exc_type) if oPythonFrame.f_exc_type else None,
    repr(oPythonFrame.f_exc_value) if oPythonFrame.f_exc_value else None,
  ] if s]);
  print "%s%s @ %s/%d%s" % (
    sPrefix, oPythonFrame.f_code.co_name,
    oPythonFrame.f_code.co_filename, oPythonFrame.f_lineno,
    " (%s)" % sSuffix if sSuffix else ""
  );
  sPrefix = " " * len(sPrefix);
  if bExpand:
    if oPythonFrame.f_back:
      fDumpPythonFrame(oPythonFrame.f_back, sPrefix + "  <-", bExpand = False);
    if oPythonFrame.f_exc_type is not None or oPythonFrame.f_exc_value is not None:
      print "%s  E>%s: %s" % (sPrefix, repr(oPythonFrame.f_exc_type), repr(oPythonFrame.f_exc_value));
    if oPythonFrame.f_exc_traceback is not None:
      fDumpTraceback(oPythonFrame.f_exc_traceback, sPrefix + "  T>", bExpand = False);

def fDumpTraceback(oTraceback, sPrefix = "", bExpand = True):
  if oTraceback.tb_frame:
    print "%s%s @ %s/%d" % (sPrefix, oTraceback.tb_frame.f_code.co_name, oTraceback.tb_frame.f_code.co_filename, oTraceback.tb_lineno);
  else:
    print "%s???/%d" % (sPrefix, oTraceback.tb_lineno);
  if oTraceback.tb_next:
    fDumpTraceback(oTraceback.tb_next, sPrefix, bExpand = True);

class cCallStack():
  class cFrame():
    @classmethod
    @HideInCallStack
    def foFromPythonFrameThreadAndExceptionLineNumber(cClass, oPythonFrame, oPythonThread, uExceptionLineNumber):
      oPythonCode = oPythonFrame.f_code;
      uLastExecutedLineNumber = oPythonFrame.f_lineno;
      (tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables) = inspect.getargvalues(oPythonFrame);
      return cClass(
        oPythonCode, uExceptionLineNumber, uLastExecutedLineNumber,
        oPythonThread, 
        tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables
      );
    
    @classmethod
    @HideInCallStack
    def foForCurrentThread(cClass, uEndIndex = 0):
      # Create a list of all PythonFrames on the stack in the current thread.
      oPythonFrame = inspect.currentframe();
      aoPythonFrames = [];
      # We are ignoring frames with hidden functions in our indices, so we need to
      # take that into account when determining the end index for this first frame:
      oWantedPythonFrame = None;
      uCurrentEndIndex = 0;
      while oPythonFrame:
        aoPythonFrames.insert(0, oPythonFrame);
        if oPythonFrame.f_code not in gaoHideFunctionsForPythonCodes:
          if uEndIndex == uCurrentEndIndex:
            if oWantedPythonFrame is None:
              oWantedPythonFrame = oPythonFrame;
              if not gbDebugDumpRawStacksAndTracebacks:
                break;
          uCurrentEndIndex += 1;
        oPythonFrame = oPythonFrame.f_back;
      assert oWantedPythonFrame, \
          "Cannot find end stack frame %d" % uEndIndex;
      if gbDebugDumpRawStacksAndTracebacks:
        print "--[ cCallStack.cFrame.foForCurrentThread ]".ljust(80, "-");
        uIndex = 0;
        for oPythonFrame in aoPythonFrames:
          if oPythonFrame.f_code in gaoHideFunctionsForPythonCodes:
            fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
          else:
            uCurrentEndIndex -= 1;
            if oPythonFrame == oWantedPythonFrame:
              assert uCurrentEndIndex == uEndIndex, \
                  "uCurrentEndIndex (%d) != uEndIndex (%d)!" % (uCurrentEndIndex, uEndIndex);
              fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex, "uEndIndex = %d" % uCurrentEndIndex);
            else:
              fDumpPythonFrame(oPythonFrame, "  - ", "uEndIndex = %s" % uCurrentEndIndex);
            uIndex += 1;
        print "-" * 80;
      oPythonThread = threading.currentThread();
      return cClass.foFromPythonFrameThreadAndExceptionLineNumber(oWantedPythonFrame, oPythonThread, None);
    
    @classmethod
    @HideInCallStack
    def foForThisFunction(cClass):
      # A call to this function will be at the top of the stack, so we need to skip that to get to our caller.
      return cClass.foForCurrentThread();
    
    @classmethod
    @HideInCallStack
    def foForThisFunctionsCaller(cClass):
      # A call to this function will be at the top of the stack, so we need to skip that to get to our caller.
      return cClass.foForCurrentThread(uEndIndex = 1); 
    
    @classmethod
    @HideInCallStack
    def foFromLastException(cClass, uEndIndex = 0):
      # A call to this function will be at the top of the stack, so we need to skip that to get to our caller.
      uEndIndex += 1;
      oTraceback = sys.exc_info()[2];
      if gbDebugDumpRawStacksAndTracebacks:
        print "--[ Traceback ]".ljust(80, "-");
        fDumpTraceback(oTraceback, sPrefix = "| ");
        print "-" * 80;
      while uEndIndex > 0 and oTraceback.tb_next:
        oTraceback = oTraceback.tb_next;
        uEndIndex -= 1;
      return cClass.foFromPythonFrameThreadAndExceptionLineNumber(
        oPythonFrame = oTraceback.tb_frame,
        oPythonThread = threading.currentThread(),
        uExceptionLineNumber = oTraceback.tb_lineno,
      );
    
    def __init__(
      oSelf,
      oPythonCode, uExceptionLineNumber, uLastExecutedLineNumber,
      oPythonThread, 
      tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables,
    ):
      oSelf.oPythonCode = oPythonCode;
      oSelf.uLineNumber = uExceptionLineNumber if uExceptionLineNumber is not None else uLastExecutedLineNumber;
      oSelf.uExceptionLineNumber = uExceptionLineNumber;
      oSelf.uLastExecutedLineNumber = uLastExecutedLineNumber;
      oSelf.uThreadId = oPythonThread.ident;
      oSelf.sThreadName = oPythonThread.name;
      oSelf.tsArgumentNames = tsArgumentNames;
      oSelf.stxArgumentsName = stxArgumentsName;
      oSelf.sdxArgumentsName = sdxArgumentsName;
      oSelf.dxLocalVariables = dxLocalVariables;
      
      oSelf.__oCachedModule = None;
      oSelf.__bFunctionMethodInstanceAndClassHaveBeenCached = False;
      oSelf.__bIsModuleCode = None;
      oSelf.__fxCachedFunction = None;
      oSelf.__fxCachedMethod = None;
      oSelf.__oCachedInstance = None;
      oSelf.__cCachedClass = None;
      oSelf.oStack = None;
      oSelf.uIndex = None;
      oSelf.oParentFrame = None;
      oSelf.oChildFrame = None;
    
    @property
    def sSourceFilePath(oSelf):
      return oSelf.oPythonCode.co_filename;
    
    @property
    def mModule(oSelf):
      mModule = inspect.getmodule(oSelf.oPythonCode);
      # This can return None if the module is currently being loaded.
      return mModule;
    
    @property
    def sSourceFileName(oSelf):
      return os.path.basename(oSelf.oPythonCode.co_filename);
    
    def __fCacheFunctionMethodInstanceClass(oSelf):
      if oSelf.__bFunctionMethodInstanceAndClassHaveBeenCached:
        return;
      oSelf.__bFunctionMethodInstanceAndClassHaveBeenCached = True;
      oPythonCode = oSelf.oPythonCode;
      if oPythonCode in gfxStaticOrClassMethod_by_oPythonCode:
        # For known static or class methods the function and class should be known too and the instance is None:
        oSelf.__bIsModuleCode = False;
        oSelf.__fxCachedFunction = gfxFunction_by_oPythonCode[oPythonCode];
        oSelf.__fxCachedMethod = gfxStaticOrClassMethod_by_oPythonCode[oPythonCode];
        oSelf.__oCachedInstance = None;
        oSelf.__cCachedClass = gfClass_by_oPythonCode[oPythonCode];
      elif oPythonCode in goPythonCode_by_mModule:
        oSelf.__bIsModuleCode = True;
        oSelf.__fxCachedFunction = None;
        oSelf.__fxCachedMethod = None;
        oSelf.__oCachedInstance = None;
        oSelf.__cCachedClass = None;
      else:
        if len(oSelf.tsArgumentNames) == 0:
          xFirstArgument = None;
        else:
          sFirstArgumentName = oSelf.tsArgumentNames[0];
          xFirstArgument = oSelf.dxLocalVariables[sFirstArgumentName];
        (
          afxFunctions,
          oSelf.__fxCachedMethod,
          oSelf.__oCachedInstance,
          oSelf.__cCachedClass,
        ) = ftxGetFunctionsMethodInstanceAndClassForPythonCode(oPythonCode, xFirstArgument);
        oSelf.__bIsModuleCode = len(afxFunctions) == 0;
        if oSelf.__bIsModuleCode and oSelf.mModule:
          goPythonCode_by_mModule[oSelf.mModule] = oPythonCode;
        oSelf.__fxCachedFunction = gfxFunction_by_oPythonCode[oPythonCode] = afxFunctions[0] if len(afxFunctions) == 1 else None;
        if oSelf.__oCachedInstance is None:
          gfxStaticOrClassMethod_by_oPythonCode[oPythonCode] = oSelf.__fxCachedMethod;
        gfClass_by_oPythonCode[oPythonCode] = oSelf.__cCachedClass;
    
    @property
    def bIsModuleCode(oSelf):
      oSelf.__fCacheFunctionMethodInstanceClass();
      return oSelf.__bIsModuleCode;
    
    @property
    def fxFunction(oSelf):
      oSelf.__fCacheFunctionMethodInstanceClass();
      return oSelf.__fxCachedFunction;
    
    @property
    def sFunctionName(oSelf):
      return oSelf.oPythonCode.co_name;
    
    @property
    def fMethod(oSelf):
      oSelf.__fCacheFunctionMethodInstanceClass();
      return oSelf.__fxCachedMethod;
    
    @property
    def oInstance(oSelf):
      oSelf.__fCacheFunctionMethodInstanceClass();
      return oSelf.__oCachedInstance;
    
    @property
    def cClass(oSelf):
      oSelf.__fCacheFunctionMethodInstanceClass();
      return oSelf.__cCachedClass;
    
    @property
    def sCallDescription(oSelf):
      return fsGetClassAndFunctionForClassAndCode(oSelf.cClass, oSelf.oPythonCode) if oSelf.cClass else oSelf.sFunctionName;
    
    @property
    def sExceptionCodeLocation(oSelf):
      return "%s/%d" % (oSelf.sSourceFilePath, oSelf.uExceptionLineNumber);
    @property
    def sLastExecutedCodeLocation(oSelf):
      return "%s/%d" % (oSelf.sSourceFilePath, oSelf.uLastExecutedLineNumber);
    
    def ftxGetCallArguments(oSelf):
      atArgument_xValue_and_sNames = [
        (sArgumentName, oSelf.dxLocalVariables[sArgumentName])
        for sArgumentName in oSelf.tsArgumentNames
      ];
      if oSelf.stxArgumentsName:
        txArguments = oSelf.dxLocalVariables[oSelf.stxArgumentsName];
        atArgument_xValue_and_sNames.append(
          ("*" + oSelf.stxArgumentsName, txArguments)
        );
      if oSelf.sdxArgumentsName:
        dxArguments = oSelf.dxLocalVariables[oSelf.sdxArgumentsName];
        atArgument_xValue_and_sNames.append(
          ("**" + oSelf.sdxArgumentsName, dxArguments)
        );
      return atArgument_xValue_and_sNames;
    
    @property
    def asModuleSourceCode(oSelf):
      return fasGetSourceCode(oSelf.sSourceFilePath);
    
    @property
    def sSourceCode(oSelf):
      return oSelf.asModuleSourceCode[oSelf.uLineNumber - 1];
    
    def faasCreateConsoleOutputForExceptionSourceCode(
      oSelf,
      axOutputHeader = [],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackNormalInactiveSourceCodeColor,
      uActiveCodeColor = guStackNormalActiveSourceCodeColor,
    ):
      assert oSelf.uExceptionLineNumber is not None, \
          "Cannot create console output for exception source code if no exception took place!";
      return faasCreateConsoleOutputForSourceCode(
        oSelf.sSourceFilePath,
        oSelf.uExceptionLineNumber - 1, oSelf.uExceptionLineNumber + 1,
        axOutputHeader,
        uLineNumberColor,
        uInactiveCodeColor, uActiveCodeColor,
      );
    def faasCreateConsoleOutputForLastExecutedSourceCode(
      oSelf,
      axOutputHeader = [],
      uLineNumberColor = guLineNumberColor,
      uInactiveCodeColor = guStackNormalInactiveSourceCodeColor,
      uActiveCodeColor = guStackNormalActiveSourceCodeColor,
    ):
      return faasCreateConsoleOutputForSourceCode(
        oSelf.sSourceFilePath,
        oSelf.uLastExecutedLineNumber - 1, oSelf.uLastExecutedLineNumber + 1,
        axOutputHeader,
        uLineNumberColor,
        uInactiveCodeColor, uActiveCodeColor,
      );
    
    @property
    def sExceptionSourceCode(oSelf):
      return oSelf.asModuleSourceCode[oSelf.uExceptionLineNumber - 1];
    
    @property
    def sLastExecutedSourceCode(oSelf):
      return oSelf.asModuleSourceCode[oSelf.uLastExecutedLineNumber - 1];
    
    def fasGetSourceLines(oSelf, uStartOffset = 0, uEndOffset = 0):
      uStartIndex = max(0, oSelf.uLineNumber - 1 - uStartOffset);
      uEndIndex = oSelf.uLineNumber + uEndOffset - 1;
      if uStartIndex >= uEndIndex: return [];
      return oSelf.asModuleSourceCode[uStartIndex: uEndIndex];

    def fasGetExceptionSourceLines(oSelf, uStartOffset = 0, uEndOffset = 1):
      uStartIndex = max(0, oSelf.uExceptionLineNumber - 1 + uStartOffset);
      uEndIndex = max(0, oSelf.uExceptionLineNumber + uEndOffset - 1);
      if uStartIndex >= uEndIndex: return [];
      return oSelf.asModuleSourceCode[uStartIndex: uEndIndex];

    def fasGetLastExecutedSourceLines(oSelf, uStartOffset = 0, uEndOffset = 1):
      uStartIndex = max(0, oSelf.uLastExecutedLineNumber - 1 + uStartOffset);
      uEndIndex = max(0, oSelf.uLastExecutedLineNumber + uEndOffset - 1);
      if uStartIndex >= uEndIndex: return [];
      return oSelf.asModuleSourceCode[uStartIndex: uEndIndex];
    
    @property
    def sLastExecutedCodeLocation(oSelf):
      return "%s/%d" % (oSelf.sSourceFilePath, oSelf.uLastExecutedLineNumber);
    
    def fsToString(oSelf):
      return "<%s#%X %s/%s @ %s, thread = %d/0x%X (%s)>" % (
        oSelf.__class__.__name__, id(oSelf),
        oSelf.sCallDescription, 
        "%d" % oSelf.uLastExecutedLineNumber if oSelf.uExceptionLineNumber is None else
          "*%d" if oSelf.uLastExecutedLineNumber == oSelf.uExceptionLineNumber else
          "*%d/%d" % (oSelf.uExceptionLineNumber, oSelf.uLastExecutedLineNumber),
        oSelf.sSourceFilePath,
        oSelf.uThreadId, oSelf.uThreadId, oSelf.sThreadName,
      );
  
  @classmethod
  @HideInCallStack
  def __foFromPythonFramesAndExceptionLineNumbers(cClass, atxPythonFrames_and_uExceptionLineNumbers, oPythonThread = None):
    oPythonThread = oPythonThread or threading.currentThread();
    return cClass([
      cCallStack.cFrame.foFromPythonFrameThreadAndExceptionLineNumber(oPythonFrame, oPythonThread, uExceptionLineNumber)
      for (oPythonFrame, uExceptionLineNumber) in atxPythonFrames_and_uExceptionLineNumbers
    ]);
  @classmethod
  @HideInCallStack
  def foFromThisFunction(cClass):
    return cClass.foForCurrentThread();
  @classmethod
  @HideInCallStack
  def foFromThisFunctionsCaller(cClass):
    return cClass.foForCurrentThread(uEndIndex = 1);
  @classmethod
  @HideInCallStack
  def foForCurrentThread(cClass, uStartIndex = None, uEndIndex = None):
    return cClass.foFromPythonFrameAndThread(inspect.currentframe(), threading.currentThread(), uStartIndex, uEndIndex);
  @classmethod
  @HideInCallStack
  def foFromPythonFrameAndThread(cClass, oPythonFrame, oPythonThread, uStartIndex = 0, uEndIndex = 0):
    # Create a list of all PythonFrames on the stack in the current thread.
    aoPythonFrames = [];
    # We are ignoring frames with hidden functions in our indices, so we need to
    # take that into account when determining the end index for this first frame:
    uCurrentEndIndex = -1;
    while oPythonFrame:
      aoPythonFrames.insert(0, oPythonFrame);
      if oPythonFrame.f_code not in gaoHideFunctionsForPythonCodes:
        uCurrentEndIndex += 1;
      oPythonFrame = oPythonFrame.f_back;
    if gbDebugDumpRawStacksAndTracebacks:
      print "--[ cCallStack.foFromPythonFrameAndThread ]".ljust(80, "-");
      if uStartIndex:
        print "uStartIndex: %d" % uStartIndex;
      if uEndIndex:
        print "uEndIndex: %d" % uEndIndex;
    uIndex = 0;
    atxPythonFramesAndExceptionLineNumbers = [];
    for oPythonFrame in aoPythonFrames:
      if oPythonFrame.f_code in gaoHideFunctionsForPythonCodes:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
      else:
        if uStartIndex and uIndex < uStartIndex:
          if gbDebugDumpRawStacksAndTracebacks:
            fDumpPythonFrame(oPythonFrame, "%2d- " % uIndex, "uStartIndex = %d" % uStartIndex);
        elif uEndIndex and uCurrentEndIndex < uEndIndex:
          # Taking into account that calling this function added another frame ------^
          if gbDebugDumpRawStacksAndTracebacks:
            fDumpPythonFrame(oPythonFrame, "%2d- " % uIndex, "uEndIndex = %d" % uCurrentEndIndex);
        else:
          if gbDebugDumpRawStacksAndTracebacks:
            fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex);
          atxPythonFramesAndExceptionLineNumbers.append((oPythonFrame, None));
        uIndex += 1;
        uCurrentEndIndex -= 1;
    if gbDebugDumpRawStacksAndTracebacks:
      print "-" * 80;
    return cClass.__foFromPythonFramesAndExceptionLineNumbers(atxPythonFramesAndExceptionLineNumbers, oPythonThread);
  
  @classmethod
  @HideInCallStack
  def faoForAllThreads(cClass, uCurrentThreadEndIndex = 0):
     doPythonThread_by_uThreadId = dict([
      (oPythonThread.ident, oPythonThread)
      for oPythonThread in threading.enumerate()
     ])
     uCurrentThreadId = threading.currentThread().ident;
     return [
       cClass.foFromPythonFrameAndThread(
         oTopPythonFrame,
         doPythonThread_by_uThreadId[uThreadId],
         uEndIndex = None if uThreadId != uCurrentThreadId else uCurrentThreadEndIndex,
       )
       for (uThreadId, oTopPythonFrame) in sys._current_frames().items()
     ];
  
  @classmethod
  def foFromTraceback(cClass, oTraceback, oPythonThread = None):
    assert oTraceback, \
        "A traceback is required!";
    atxPythonFrames_and_uExceptionLineNumbers = [];
    if gbDebugDumpRawStacksAndTracebacks:
      print "--[ cCallStack.foFromTraceback ]".ljust(80, "-");
    uIndex = 0;
    while oTraceback:
      oPythonFrame = oTraceback.tb_frame;
      if oPythonFrame.f_code in gaoHideFunctionsForPythonCodes:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
      else:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex);
        atxPythonFrames_and_uExceptionLineNumbers.append((oPythonFrame, oTraceback.tb_lineno));
        uIndex += 1;
      oTraceback = oTraceback.tb_next;
    if gbDebugDumpRawStacksAndTracebacks:
      print "-" * 80;
    oStack = cClass.__foFromPythonFramesAndExceptionLineNumbers(atxPythonFrames_and_uExceptionLineNumbers, oPythonThread);
    return oStack;
  
  @classmethod
  def foFromLastException(cClass):
    return cClass.foFromTraceback(sys.exc_info()[2]);
  
  def __init__(oSelf, aoFrames):
    assert len(aoFrames) > 0, \
        "A stack must have at least one frame!";
    oSelf.aoFrames = aoFrames; # frame 0 is the top frame.
    
    for uIndex in xrange(len(oSelf.aoFrames)):
      oFrame = oSelf.aoFrames[uIndex];
      oFrame.oStack = oSelf;
      oFrame.uIndex = uIndex;
      oFrame.oParentFrame = oSelf.aoFrames[uIndex - 1] if uIndex > 0 else None;
      oFrame.oChildFrame = oSelf.aoFrames[uIndex + 1] if uIndex < len(oSelf.aoFrames) - 1 else None;
  
  @property
  def uThreadId(oSelf):
    return oSelf.aoFrames[0].uThreadId;
  
  @property
  def sThreadName(oSelf):
    return oSelf.aoFrames[0].sThreadName;
  
  @property
  def oTopFrame(oSelf):
    return oSelf.aoFrames[-1];
  
  def faasCreateConsoleOutput(oSelf, *txArguments, **dxArguments):
    return faasCreateConsoleOutputForStack(oSelf, *txArguments, **dxArguments);
  
  def fsToString(oSelf):
    return "<%s#%X thread = %d/0x%X (%s), %d frames @ %s>" % (
      oSelf.__class__.__name__, id(oSelf),
      oSelf.uThreadId, oSelf.uThreadId, oSelf.sThreadName,
      len(oSelf.aoFrames),
      oSelf.aoFrames[-1].sCallDescription
    );
