import inspect, os, sys, threading;

from .fasGetSourceCode import fasGetSourceCode;
from .faasCreateConsoleOutputForSourceCode import faasCreateConsoleOutputForSourceCode;
from .fDumpPythonFrame import fDumpPythonFrame;
from .fDumpTraceback import fDumpTraceback;
from .fsGetClassAndFunctionForClassAndCode import fsGetClassAndFunctionForClassAndCode;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .HideInCallStack import HideInCallStack;
from .mColors import *;

goPythonCode_by_mModule = {};
gfxFunction_by_oPythonCode = {};
gfxStaticOrClassMethod_by_oPythonCode = {};
gfClass_by_oPythonCode = {};

gbDebugDumpRawStacksAndTracebacks = False;

class cFrame():
  @classmethod
  @HideInCallStack
  def foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(cClass, oPythonFrame, oPythonThread, u0ExceptionLineNumber, u0ExceptionCharacterNumber):
    oPythonCode = oPythonFrame.f_code;
    uLastExecutedLineNumber = oPythonFrame.f_lineno;
    (tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables) = inspect.getargvalues(oPythonFrame);
    return cClass(
      oPythonCode, u0ExceptionLineNumber, u0ExceptionCharacterNumber, uLastExecutedLineNumber,
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
      print("--[ cCallStack.cFrame.foForCurrentThread ]".ljust(80, "-"));
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
      print("-" * 80);
    return cClass.foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(
      oPythonFrame = oWantedPythonFrame,
      oPythonThread = threading.currentThread(),
      u0ExceptionLineNumber = None,
      u0ExceptionCharacterNumber = None,
    );
  
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
  
  def __init__(
    oSelf,
    oPythonCode, u0ExceptionLineNumber, u0ExceptionCharacterNumber, uLastExecutedLineNumber,
    oPythonThread, 
    tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables,
  ):
    oSelf.oPythonCode = oPythonCode;
    oSelf.uLineNumber = u0ExceptionLineNumber if u0ExceptionLineNumber is not None else uLastExecutedLineNumber;
    oSelf.u0ExceptionCharacterNumber = u0ExceptionCharacterNumber;
    oSelf.u0ExceptionLineNumber = u0ExceptionLineNumber;
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
    assert oSelf.u0ExceptionLineNumber is not None, \
        "This frame does not appear to be for an exception, as there is no exception line number specified!";
    return "%s/%d" % (oSelf.sSourceFilePath, oSelf.u0ExceptionLineNumber);
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
    assert oSelf.u0ExceptionLineNumber is not None, \
        "This frame does not appear to be for an exception, as there is no exception line number specified!";
    return faasCreateConsoleOutputForSourceCode(
      oSelf.sSourceFilePath,
      oSelf.u0ExceptionLineNumber - 1, oSelf.u0ExceptionLineNumber + 1,
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
    assert oSelf.u0ExceptionLineNumber is not None, \
        "This frame does not appear to be for an exception, as there is no exception line number specified!";
    return oSelf.asModuleSourceCode[oSelf.u0ExceptionLineNumber - 1];
  
  @property
  def sLastExecutedSourceCode(oSelf):
    return oSelf.asModuleSourceCode[oSelf.uLastExecutedLineNumber - 1];
  
  def fasGetSourceLines(oSelf, uStartOffset = 0, uEndOffset = 0):
    uStartIndex = max(0, oSelf.uLineNumber - 1 - uStartOffset);
    uEndIndex = oSelf.uLineNumber + uEndOffset - 1;
    if uStartIndex >= uEndIndex: return [];
    return oSelf.asModuleSourceCode[uStartIndex: uEndIndex];

  def fasGetExceptionSourceLines(oSelf, uStartOffset = 0, uEndOffset = 1):
    assert oSelf.u0ExceptionLineNumber is not None, \
        "This frame does not appear to be for an exception, as there is no exception line number specified!";
    uStartIndex = max(0, oSelf.u0ExceptionLineNumber - 1 + uStartOffset);
    uEndIndex = max(0, oSelf.u0ExceptionLineNumber + uEndOffset - 1);
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
      "%d" % oSelf.uLastExecutedLineNumber if oSelf.u0ExceptionLineNumber is None else
        "*%d" if oSelf.uLastExecutedLineNumber == oSelf.u0ExceptionLineNumber else
        "*%d/%d" % (oSelf.u0ExceptionLineNumber, oSelf.u0LastExecutedLineNumber),
      oSelf.sSourceFilePath,
      oSelf.uThreadId, oSelf.uThreadId, oSelf.sThreadName,
    );
