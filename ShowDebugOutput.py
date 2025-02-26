import functools, inspect, sys, threading, time;

gbShowInternalDebugOutput = False;
guExceptionAsStringMaxSize = 400;
guArgumentAsStringMaxSize = 200;
guReturnValueAsStringMaxSize = 400;
guExitCodeInternalError = 1; # This is the common default I use. There's currently no good way to set this per application.

def ShowDebugOutput(fxFunction):
  sBadDecorator = {
    classmethod: "@classmethod",
    property: "@property/@.setter/@.deleter",
    staticmethod: "@staticmethod",
  }.get(type(fxFunction));
  if sBadDecorator:
    raise AssertionError("@ShowDebugOutput must not be followed by %s!" % sBadDecorator);
  sSourceFilePath = fxFunction.__code__.co_filename;
  oSignature = inspect.signature(fxFunction);
  axArgumentNames = list(oSignature.parameters.keys());
  s0FirstArgumentName = None;
  s0txArgumentName = None;
  s0dxArgumentName = None;
  for oParameter in oSignature.parameters.values():
    if s0FirstArgumentName is None:
      s0FirstArgumentName = oParameter.name;
    if oParameter.kind == inspect.Parameter.VAR_POSITIONAL:
      s0txArgumentName = oParameter.name;
    elif oParameter.kind == inspect.Parameter.VAR_KEYWORD:
      s0dxArgumentName = oParameter.name;
  
  @functools.wraps(fxFunction)
  def fxFunctionWrapper(*txCallArgumentValues, **dxCallArgumentValues):
    mDebugOutput_HideInCallStack = True; # Any exception in this code is likely not to be caused by this code.
    try:
      # This can fail if Python is ending, hence try....catch
      o0PythonThread = threading.current_thread();
    except:
      o0PythonThread = None;
    try:
      oInstance = None;
      cClass = None;
      if gbShowInternalDebugOutput:
        print("@ CALL %s(%s, %s)" % (fxFunction.__name__, repr(txCallArgumentValues)[1:-1], repr(dxCallArgumentValues)[1:-1]));
      if axArgumentNames:
        if s0FirstArgumentName in dxCallArgumentValues:
          xFirstArgumentValue = dxCallArgumentValues[s0FirstArgumentName];
        else:
          xFirstArgumentValue = txCallArgumentValues[0];
        (oInstance, cClass) = ftocGetInstanceAndClassForUnknown(xFirstArgumentValue);
        if gbShowInternalDebugOutput:
          print("xFirstArgument: %s" % repr(xFirstArgumentValue));
          print("oInstance: %s" % oInstance);
          print("cClass: %s" % cClass);
      sCallDescription = fsGetClassAndFunctionForClassAndCode(cClass, fxFunction.__code__);
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
      for uIndex in range(len(txCallArgumentValues)):
        xValue = txCallArgumentValues[uIndex];
        if uIndex < len(axArgumentNames):
          xName = axArgumentNames[uIndex];
          axUnusedArgumentNames.remove(xName);
          asUnnamedCallArguments.append("%s = %s" % (xName, fsToString(xValue, guArgumentAsStringMaxSize)));
        elif s0txArgumentName:
          txCallArgument = tuple(txCallArgumentValues[uIndex:]);
          break;
        else:
          # This argument is superfluous.
          asUnnamedCallArguments.append("???#%d = %s" % (uIndex, fsToString(xValue, guArgumentAsStringMaxSize)));
      # Process the rest of the arguments to see which ones are provided by
      # name and which ones are missing:
      axUnusedNamedCallArgumentNames = list(dxCallArgumentValues.keys());
      for xName in axUnusedArgumentNames[:]:
        if xName in dxCallArgumentValues:
          xValue = dxCallArgumentValues[xName];
          axUnusedNamedCallArgumentNames.remove(xName);
          asNamedCallArguments.append("%s = %s" % (xName, fsToString(xValue, guArgumentAsStringMaxSize)));
          axUnusedArgumentNames.remove(xName);
        else:
          # This argument is missing
          asNamedCallArguments.append("%s = ???" % (xName,));
      # Handle unused named arguments:
      if len(axUnusedNamedCallArgumentNames) > 0:
        if s0dxArgumentName:
          for xName in axUnusedNamedCallArgumentNames:
            dxCallArgument[xName] = dxCallArgumentValues[xName];
        else:
          for xName in axUnusedNamedCallArgumentNames:
            asNamedCallArguments.append("%s??? = %s" % (xName, fsToString(dxCallArgumentValues[xName], guArgumentAsStringMaxSize)));
      # Put everything together:
      asCallArguments = asUnnamedCallArguments;
      if s0txArgumentName:
        asCallArguments.append("*%s = %s" % (s0txArgumentName, fsToString(txCallArgument, guArgumentAsStringMaxSize)));
      asCallArguments += asNamedCallArguments;
      if s0dxArgumentName:
        asCallArguments.append("**%s = %s" % (s0dxArgumentName, fsToString(dxCallArgument, guArgumentAsStringMaxSize)));
      # This function is hidden, so if we ask for the the frame for this function, we will get
      # the frame of its caller.
      oCallFrame = cFrame.fo0ForCurrentThreadAndFunction();
      if gbShowInternalDebugOutput:
        sCallArguments = ", ".join(asCallArguments);
        if bShowDebugOutput:
          print("@ SHOW %s(%s) @ %s" % (sCallDescription, sCallArguments, repr(sSourceFilePath)));
        else:
          print("@ HIDE %s(%s) @ %s" % (sCallDescription, sCallArguments, repr(sSourceFilePath)));
      if bShowDebugOutput:
        fDebugOutputHelper(
          oCallFrame.u0ThreadId, oCallFrame.s0ThreadName,
          oCallFrame.sSourceFilePath, oCallFrame.uLastExecutedLineNumber,
          "%s(%s" % (sCallDescription,"" if len(asCallArguments) > 0 else ")"),
          uIndentationChange = +1,
        );
        if asCallArguments:
          for sCallArgument in asCallArguments:
            fDebugOutputHelper(
              oCallFrame.u0ThreadId, "",
              "", None,
              "  %s" % (sCallArgument,),
            );
          fDebugOutputHelper(
            oCallFrame.u0ThreadId, "",
            "", None,
            ")",
          );
    except Exception as oException:
      fTerminateWithException(oException, guExitCodeInternalError);
    if not bShowDebugOutput:
      return fxFunction(*txCallArgumentValues, **dxCallArgumentValues);
    nStartTime = time.time();
    try:
      xReturnValue = fxFunction(*txCallArgumentValues, **dxCallArgumentValues);
    except Exception as oException:
      try:
        nDuration = time.time() - nStartTime;
        # We detected this in the fxFunction call above (oTraceback) but it
        # was raised in fxFunction, which would be in the previous traceback.
        oTraceback = sys.exc_info()[2];
        if oTraceback.tb_next:
          oTraceback = oTraceback.tb_next;
        oCurrentTraceback = oTraceback
        # See if there are any calls to functions with ShowDebugOutput in
        # previous tracebacks. If not, this exception was triggered in a
        # function call that has not yet been shown. We need to show all functions
        # that (re-)raised it before to explain where it comes from.
        aoAdditionalTracebacksToShow = [];
        while oTraceback.tb_next and oTraceback.tb_next.tb_frame.f_code != ShowDebugOutput.oFunctionWrapperCode:
          oTraceback = oTraceback.tb_next;
          aoAdditionalTracebacksToShow.append(oTraceback);
        if oCurrentTraceback != oTraceback and not oTraceback.tb_next:
          uIndentation = len(aoAdditionalTracebacksToShow);
          for oTraceback in reversed(aoAdditionalTracebacksToShow):
            oExceptionFrame = cFrame.foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(
              oPythonFrame = oTraceback.tb_frame,
              o0PythonThread = o0PythonThread,
              u0ExceptionLineNumber = oTraceback.tb_lineno,
              u0ExceptionCharacterNumber = None,
            );
            fDebugOutputHelper(
              oExceptionFrame.u0ThreadId, oExceptionFrame.s0ThreadName,
              oExceptionFrame.sSourceFilePath, oExceptionFrame.u0ExceptionLineNumber,
              "%s %sraise %s;" % (
                " <" * uIndentation,
                "" if oTraceback.tb_next is None else "re-",
                fsToString(oException, guExceptionAsStringMaxSize),
              ),
            );
            uIndentation -= 1;
        oExceptionFrame = cFrame.foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(
          oPythonFrame = oCurrentTraceback.tb_frame,
          o0PythonThread = o0PythonThread,
          u0ExceptionLineNumber = oCurrentTraceback.tb_lineno,
          u0ExceptionCharacterNumber = None,
        );
        fDebugOutputHelper(
          oExceptionFrame.u0ThreadId, oExceptionFrame.s0ThreadName,
          oExceptionFrame.sSourceFilePath, oExceptionFrame.u0ExceptionLineNumber,
          "%sraise %s; // [%s] duration = %fs" % (
            "" if oCurrentTraceback.tb_next is None else "re-",
            fsToString(oException, guExceptionAsStringMaxSize),
            sCallDescription,
            nDuration
          ),
          uIndentationChange = -1,
          bAlwaysShow = True,
        );
      except Exception as oException:
        fTerminateWithException(oException, guExitCodeInternalError);
      raise;
    else:
      try:
        # Unfortunately, we do not know the line number where the function returned, so we cannot provide useful
        # information on that. We will show the file name and line number of the call, so you at least know where
        # it returned to. This will be indicated in the output (bIsReturnAddress = True).
        sReturnValue = fsToString(xReturnValue, guReturnValueAsStringMaxSize);
        fDebugOutputHelper(
          oCallFrame.u0ThreadId, oCallFrame.s0ThreadName,
          oCallFrame.sSourceFilePath, oCallFrame.uLastExecutedLineNumber,
          "return %s; // duration = %fs [%s] " % (sReturnValue, time.time() - nStartTime, sCallDescription),
          uIndentationChange = -1,
          bAlwaysShow = True,
          bIsReturnAddress = True,
        );
      except Exception as oException:
        fTerminateWithException(oException, guExitCodeInternalError);
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
from .mGlobals import *;

# ShowDebugOutput should have an attribute "oFunctionWrapperCode" for
# fTerminateWithException to use. This attribute will be set the first time we
# use ShowDebugOutput, so let's do that with a dummy function:
ShowDebugOutput(lambda: 0);
