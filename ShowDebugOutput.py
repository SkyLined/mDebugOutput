import functools, inspect, threading, time;

gbShowInternalDebugOutput = False;
guExceptionAsStringMaxSize = 400;
guArgumentAsStringMaxSize = 200;
guReturnValueAsStringMaxSize = 400;

def ShowDebugOutput(fxFunction):
  sBadDecorator = {
    classmethod: "@classmethod",
    property: "@property/@.setter/@.deleter",
    staticmethod: "@staticmethod",
  }.get(type(fxFunction));
  if sBadDecorator:
    raise AssertionError("@ShowDebugOutput must not be followed by %s!" % sBadDecorator);
  sSourceFilePath = fxFunction.func_code.co_filename;
  uLineNumber = fxFunction.func_code.co_firstlineno;
  (axArgumentNames, stxArgumentName, sdxArgumentName, txDefaultArgumentValues) = inspect.getargspec(fxFunction);
  sFirstArgumentName = axArgumentNames[0] if len(axArgumentNames) > 0 and isinstance(axArgumentNames[0], str) else None;
  dxDefaultArgumentValue_by_xName = {};
  if txDefaultArgumentValues:
    for uArgumentIndex in xrange(-len(txDefaultArgumentValues), 0, 1):
      xArgumentName = axArgumentNames[uArgumentIndex];
      xDefaultArgumentValue = txDefaultArgumentValues[uArgumentIndex];
      dxDefaultArgumentValue_by_xName[xArgumentName] = xDefaultArgumentValue;
  if gbShowInternalDebugOutput:
    print "@ WRAP %s(%s%s%s) @ %s" % (
      fxFunction.func_name,
      ", ".join([
        "%s%s" % (
          repr(xArgumentName),
          " = %s" % repr(dxDefaultArgumentValue_by_xName[xArgumentName])
            if xArgumentName in dxDefaultArgumentValue_by_xName
            else ""
        )
        for xArgumentName in axArgumentNames
      ]),
      ", *%s" % stxArgumentName if stxArgumentName is not None else "",
      ", **%s" % sdxArgumentName if sdxArgumentName is not None else "",
      sSourceFilePath
    );
    print "  sFirstArgumentName: %s" % sFirstArgumentName;
  
  @functools.wraps(fxFunction)
  @HideInCallStack
  def fxFunctionWrapper(*txCallArgumentValues, **dxCallArgumentValues):
    try:
      oInstance = None;
      cClass = None;
      if gbShowInternalDebugOutput:
        print "@ CALL %s(%s, %s)" % (fxFunction.func_name, repr(txCallArgumentValues)[1:-1], repr(dxCallArgumentValues)[1:-1]);
      if sFirstArgumentName is not None:
        if sFirstArgumentName in dxCallArgumentValues:
          xFirstArgumentValue = dxCallArgumentValues[sFirstArgumentName];
        else:
          xFirstArgumentValue = txCallArgumentValues[0];
        (oInstance, cClass) = ftocGetInstanceAndClassForUnknown(xFirstArgumentValue);
        if gbShowInternalDebugOutput:
          print "xFirstArgument: %s" % repr(xFirstArgumentValue);
          print "oInstance: %s" % oInstance;
          print "cClass: %s" % cClass;
      sCallDescription = fsGetClassAndFunctionForClassAndCode(cClass, fxFunction.func_code);
      bShowDebugOutput = fbIsDebugOutputEnabledForSourceFilePathAndClass(sSourceFilePath, cClass);
      # The user may be trying to pass too many arguments or non-existing 
      # keyword arguments, which leads to TypeError exceptions in inspect.getcallargs. We'll
      # filter these out:
      axUnusedArgumentNames = axArgumentNames[:];
      asUnnamedCallArguments = [];
      txCallArgument = tuple();
      asNamedCallArguments = [];
      dxCallArgument = {};
      uIndex = 0;
      # Process the unnamed call arguments first:
      for uIndex in xrange(len(txCallArgumentValues)):
        xValue = txCallArgumentValues[uIndex];
        if uIndex < len(axArgumentNames):
          xName = axArgumentNames[uIndex];
          axUnusedArgumentNames.remove(xName);
          asUnnamedCallArguments.append("%s = %s" % (xName, fsToString(xValue, guArgumentAsStringMaxSize)));
          sName = repr(xName);
        elif stxArgumentName:
          txCallArgument = tuple(txCallArgumentValues[uIndex:]);
          break;
        else:
          # This argument is superfluous.
          asUnnamedCallArguments.append("???#%d = %s" % (uIndex, fsToString(xValue, guArgumentAsStringMaxSize)));
      # Process the rest of the arguments to see which ones are provided by
      # name and which ones are missing:
      axUnusedNamedCallArgumentNames = dxCallArgumentValues.keys();
      for xName in axUnusedArgumentNames[:]:
        if xName in dxCallArgumentValues:
          xValue = dxCallArgumentValues[xName];
          axUnusedNamedCallArgumentNames.remove(xName);
          asNamedCallArguments.append("%s = %s" % (xName, fsToString(xValue, guArgumentAsStringMaxSize)));
          axUnusedArgumentNames.remove(xName);
        elif xName not in dxDefaultArgumentValue_by_xName:
          # This argument is missing
          asNamedCallArguments.append("%s = ???" % (xName,));
      # Handle unused named arguments:
      if len(axUnusedNamedCallArgumentNames) > 0:
        if sdxArgumentName:
          for xName in axUnusedNamedCallArgumentNames:
            dxCallArgument[xName] = dxCallArgumentValues[xName];
        else:
          for xName in axUnusedNamedCallArgumentNames:
            asNamedCallArguments.append("%s??? = %s" % (xName, fsToString(dxCallArgumentValues[xName], guArgumentAsStringMaxSize)));
      # Put everything together:
      asCallArguments = asUnnamedCallArguments;
      if stxArgumentName:
        asCallArguments.append("*%s = %s" % (stxArgumentName, fsToString(txCallArgument, guArgumentAsStringMaxSize)));
      asCallArguments += asNamedCallArguments;
      if sdxArgumentName:
        asCallArguments.append("**%s = %s" % (sdxArgumentName, fsToString(dxCallArgument, guArgumentAsStringMaxSize)));
      sCallArguments = ", ".join(asCallArguments);
      oCallFrame = cFrame.foForThisFunction();
      if gbShowInternalDebugOutput:
        if not bShowDebugOutput:
          print "@ HIDE %s(%s) @ %s" % (sCallDescription, sCallArguments, repr(sSourceFilePath));
        else:
          print "@ SHOW %s(%s) @ %s" % (sCallDescription, sCallArguments, repr(sSourceFilePath));
      if bShowDebugOutput:
        fDebugOutputHelper(
          oCallFrame.uThreadId, oCallFrame.sThreadName,
          oCallFrame.sSourceFilePath, oCallFrame.uLastExecutedLineNumber,
          "%s(%s)" % (sCallDescription, sCallArguments),
          uIndentationChange = +1,
        );
      oPythonThread = threading.currentThread();
    except Exception as oException:
      fTerminateWithException(oException);
    if not bShowDebugOutput:
      return fxFunction(*txCallArgumentValues, **dxCallArgumentValues);
    nStartTime = time.time();
    try:
      xReturnValue = fxFunction(*txCallArgumentValues, **dxCallArgumentValues);
    except Exception as oException:
      try:
        oExceptionFrame = cFrame.foFromLastException();
        fDebugOutputHelper(
          oExceptionFrame.uThreadId, oExceptionFrame.sThreadName,
          oExceptionFrame.sSourceFilePath, oExceptionFrame.u0ExceptionLineNumber,
          "raise %s // [%s] duration = %fs" % (fsToString(oException, guExceptionAsStringMaxSize), sCallDescription, time.time() - nStartTime),
          uIndentationChange = -1,
          bAlwaysShow = True,
        );
      except Exception as oException:
        fTerminateWithException(oException);
      raise;
    else:
      try:
        sReturnValue = fsToString(xReturnValue, guReturnValueAsStringMaxSize) if xReturnValue is not None else None;
        fDebugOutputHelper(
          oCallFrame.uThreadId, oCallFrame.sThreadName,
          # The return is shown as taking place in the called function at unknown line number but after the first.
          sSourceFilePath, uLineNumber,
          "return%s // [%s] duration = %fs" % (" %s" % sReturnValue if sReturnValue else "", sCallDescription, time.time() - nStartTime),
          uIndentationChange = -1,
          bAlwaysShow = True,
          bLineNumberIsUncertain = True,
        );
      except Exception as oException:
        fTerminateWithException(oException);
      return xReturnValue;
  fxFunctionWrapper.fxWrappedFunction = fxFunction;
  ShowDebugOutput.oFunctionWrapperCode = fxFunctionWrapper.__code__;
  return fxFunctionWrapper;

from .cFrame import cFrame;
from .fbIsDebugOutputEnabledForSourceFilePathAndClass import fbIsDebugOutputEnabledForSourceFilePathAndClass;
from .fDebugOutputHelper import fDebugOutputHelper;
from .fsGetClassAndFunctionForClassAndCode import fsGetClassAndFunctionForClassAndCode;
from .fsToString import fsToString;
from .fTerminateWithException import fTerminateWithException;
from .ftocGetInstanceAndClassForUnknown import ftocGetInstanceAndClassForUnknown;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;
from .HideInCallStack import HideInCallStack;
from .mGlobals import *;

# ShowDebugOutput should have an attribute "oFunctionWrapperCode" for
# fTerminateWithException to use. This attribute will be set the first time we
# use ShowDebugOutput, so let's do that with a dummy function:
ShowDebugOutput(lambda: 0);
