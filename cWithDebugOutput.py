from .cStack import cStack;
from .fDebugOutput import fDebugOutput;
from .fFatalExceptionOutput import fFatalExceptionOutput;
from .fsToString import fsToString;

class cWithDebugOutput(object):
  def fEnterFunctionOutput(oSelf, **dxArguments):
    oCaller = cStack.foPushCaller(uCallerIndex = 0);
    if oCaller.bShowDebugOutput:
      fDebugOutput("".join([
        "%60s" % oCaller.sCallLocation,
        "%s \xC3\xC4\xBF " % (" \xB3" * oCaller.uStackIndex),
        "%s.%s(%s)" % (oSelf.__class__.__name__, oCaller.sCurrentFunction, ", ".join(
          ["oSelf=%s" % (fsToString(oSelf) if oCaller.sCurrentFunction != "__init__" else "...")] +
          ["%s=%s" % (sName, fsToString(xValue, 60)) for (sName, xValue) in dxArguments.items()]
        )),
      ]));
  def fStatusOutput(oSelf, sMessage, bCalledFromSubFunction = False, bVerbose = True):
    oCaller = cStack.foGetCaller(uCallerIndex = 1 if bCalledFromSubFunction else 0);
    if oCaller.bShowDebugOutput:
      fDebugOutput("".join([
        "%60s" % oCaller.sCurrentLocation,
        "%s \xC3 " % (" \xB3" * (oCaller.uStackIndex + 1)),
        "%s" % sMessage if isinstance(sMessage, (str, unicode)) else repr(sMessage),
      ]));
  
  def fExitFunctionOutput(oSelf, sDetails = None):
    oSelf.__fExitFunctionOutput(None, False, sDetails);
  def fxExitFunctionOutput(oSelf, xReturnValue, sDetails = None):
    oSelf.__fExitFunctionOutput(xReturnValue, True, sDetails);
    return xReturnValue;
  def __fExitFunctionOutput(oSelf, xReturnValue, bShowReturnValue, sDetails):
    oCaller = cStack.foPopCaller(uCallerIndex = 1);
    if oCaller.bShowDebugOutput:
      fDebugOutput("".join([
        "%60s" % oCaller.sCurrentLocation,
        "%s \xC3\xC4\xD9 " % (" \xB3" * oCaller.uStackIndex),
        "%s.%s" % (oSelf.__class__.__name__, oCaller.sCurrentFunction),
        " <\xCD %s" % fsToString(xReturnValue, 200) if bShowReturnValue else "",
        " (%s)" % (sDetails if isinstance(sDetails, (str, unicode)) else repr(sDetails)) if sDetails else "",
      ]));
  
  def fxRaiseExceptionOutput(oSelf, oException):
    oSelf.__fExceptionOutput(oException);
    return oException;
  def fFatalExceptionOutput(oSelf, oException):
    oSelf.__fExceptionOutput(oException);
    fFatalExceptionOutput(oException);
  def __fExceptionOutput(oSelf, oException):
    oCaller = cStack.foPopCaller(uCallerIndex = 1, bMayHaveBeenPoppedAlready = True);
    if oCaller.bShowDebugOutput:
      fDebugOutput("".join([
        "%60s" % oCaller.sCurrentLocation,
        "%s\xC4\xD9 " % (" \xB3" * (oCaller.uStackIndex + 1)),
        "!! %s" % fsToString(oException, 200),
      ]));
    return oException;

  def fsToString(oSelf):
    return "%s{#%d}" % (oSelf.__class__.__name__, id(oSelf));

