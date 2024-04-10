import inspect, os, sys, threading;

from .dxConfig import dxConfig;
from .mColorsAndChars import *;
# The rest of the imports are done at the bottom to prevent import loops.

goPythonCode_by_mModule = {};
gfxFunction_by_oPythonCode = {};
gfxStaticOrClassMethod_by_oPythonCode = {};
gfClass_by_oPythonCode = {};

gbDebugDumpRawStacksAndTracebacks = False;

class cFrame():
  @classmethod
  def foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(cClass, oPythonFrame, o0PythonThread, u0ExceptionLineNumber, u0ExceptionCharacterNumber):
    oPythonCode = oPythonFrame.f_code;
    uLastExecutedLineNumber = oPythonFrame.f_lineno;
    (tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables) = inspect.getargvalues(oPythonFrame);
    return cClass(
      oPythonCode, u0ExceptionLineNumber, u0ExceptionCharacterNumber, uLastExecutedLineNumber,
      o0PythonThread, 
      tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables
    );
  
  @classmethod
  def fo0ForCurrentThreadAndFunction(cClass):
    mDebugOutput_HideInCallStack = 1; # This function should not show up on the stack.
    return cClass.__fo0ForCurrentThread(False);
  @classmethod
  def fo0ForCurrentThreadAndFunctionCaller(cClass):
    mDebugOutput_HideInCallStack = 1; # This function should not show up on the stack.
    return cClass.__fo0ForCurrentThread(True);
  @classmethod
  def __fo0ForCurrentThread(cClass, bReturnCallerFrame):
    mDebugOutput_HideInCallStack = 1; # This function should not show up on the stack.
    # Create a list of all PythonFrames on the stack in the current thread.
    oPythonFrame = inspect.currentframe();
    aoPythonFrames = [];
    # We are ignoring frames with hidden functions in our indices, so we need to
    # take that into account when determining the end index for this first frame:
    o0WantedPythonFrame = None;
    bCurrentFunctionFrameFound = False;
    while oPythonFrame:
      aoPythonFrames.insert(0, oPythonFrame);
      # This function ignores hidden frames.
      if "mDebugOutput_HideInCallStack" not in oPythonFrame.f_code.co_varnames:
        # If we haven't found the frame we want yet, and:
        # * if we want the function's frame and we haven't found it yet
        # * or if we want the function's caller frame and we have previously
        #   found the function's fram.
        # ... then this is the frame we want.
        if (
          o0WantedPythonFrame is None
        ) and (
          (
            not bReturnCallerFrame and not bCurrentFunctionFrameFound
          ) or (
            bReturnCallerFrame and bCurrentFunctionFrameFound
          )
        ):
          o0WantedPythonFrame = oPythonFrame;
          if not gbDebugDumpRawStacksAndTracebacks:
            break;
        bCurrentFunctionFrameFound = True;
      oPythonFrame = oPythonFrame.f_back;
    if gbDebugDumpRawStacksAndTracebacks:
      print((
        "--[ cCallStack.cFrame.fo0ForCurrentThreadAndFunction%s ]" % ("Caller" if bReturnCallerFrame else "")
      ).ljust(80, "-"));
      uIndex = 0;
      for oPythonFrame in aoPythonFrames:
        if "mDebugOutput_HideInCallStack" in oPythonFrame.f_code.co_varnames:
          fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
        else:
          uCurrentEndIndex -= 1;
          if oPythonFrame == o0WantedPythonFrame:
            fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex, "Wanted frame");
          else:
            fDumpPythonFrame(oPythonFrame, "  - ", "");
          uIndex += 1;
      print("-" * 80);
    if not o0WantedPythonFrame:
      return None; # All frames are hidden.
    try: # This can fail during shutdown, so we catch any exceptions and ignore them.
      o0PythonThread = threading.current_thread();
    except:
      o0PythonThread = None;
    return cClass.foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(
      oPythonFrame = o0WantedPythonFrame,
      o0PythonThread = o0PythonThread,
      u0ExceptionLineNumber = None,
      u0ExceptionCharacterNumber = None,
    );
  
  def __init__(
    oSelf,
    oPythonCode, u0ExceptionLineNumber, u0ExceptionCharacterNumber, uLastExecutedLineNumber,
    o0PythonThread, 
    tsArgumentNames, stxArgumentsName, sdxArgumentsName, dxLocalVariables,
  ):
    oSelf.oPythonCode = oPythonCode;
    oSelf.uLineNumber = u0ExceptionLineNumber if u0ExceptionLineNumber is not None else uLastExecutedLineNumber;
    oSelf.u0ExceptionCharacterNumber = u0ExceptionCharacterNumber;
    oSelf.u0ExceptionLineNumber = u0ExceptionLineNumber;
    oSelf.uLastExecutedLineNumber = uLastExecutedLineNumber;
    oSelf.u0ThreadId = o0PythonThread.ident if o0PythonThread else None;
    oSelf.s0ThreadName = o0PythonThread.name if o0PythonThread else None;
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
  def m0Module(oSelf):
    try:
      # This can return None if the module is currently being loaded
      return inspect.getmodule(oSelf.oPythonCode);
    except:
      # This can throw an exception if Python is ending.
      return None;
  
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
      if oSelf.__bIsModuleCode and oSelf.m0Module:
        goPythonCode_by_mModule[oSelf.m0Module] = oPythonCode;
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
    return "%s%s%d" % (oSelf.sSourceFilePath, dxConfig["sLineNumberAfterPathPrefix"], oSelf.u0ExceptionLineNumber);
  @property
  def sLastExecutedCodeLocation(oSelf):
    return "%s%s%d" % (oSelf.sSourceFilePath, dxConfig["sLineNumberAfterPathPrefix"], oSelf.uLastExecutedLineNumber);
  
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
    return "%s%s%d" % (oSelf.sSourceFilePath, dxConfig["sLineNumberAfterPathPrefix"], oSelf.uLastExecutedLineNumber);
  
  def fsToString(oSelf):
    return "<%s#%X %s %s @ %s, thread %s>" % (
      oSelf.__class__.__name__, id(oSelf),
      oSelf.sCallDescription, 
      "at line %d" % oSelf.uLastExecutedLineNumber if oSelf.u0ExceptionLineNumber is None else \
          "at except line %d" if oSelf.uLastExecutedLineNumber == oSelf.u0ExceptionLineNumber else \
          "*at except line %d/line %d" % (oSelf.u0ExceptionLineNumber, oSelf.u0LastExecutedLineNumber),
      oSelf.sSourceFilePath,
      "%d/0x%X (%s)" % (oSelf.u0ThreadId, oSelf.u0ThreadId, oSelf.s0ThreadName) if oSelf.u0ThreadId else \
          "unknown",
    );

from .fasGetSourceCode import fasGetSourceCode;
from .faasCreateConsoleOutputForSourceCode import faasCreateConsoleOutputForSourceCode;
from .fDumpPythonFrame import fDumpPythonFrame;
from .fDumpTraceback import fDumpTraceback;
from .fsGetClassAndFunctionForClassAndCode import fsGetClassAndFunctionForClassAndCode;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;

