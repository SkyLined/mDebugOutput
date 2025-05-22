import inspect, types;

from .dxConfig import dxConfig;

gbmNotProvidedLoaded = False; # mNotProvided is loaded JIT to prevent import dependency issues.
gz0NotProvided = None;

def fsToString(xValue, uMaxLength = 1000, axAlreadyProcessingValues = None):
  if uMaxLength is not None and uMaxLength < 16:
    uMaxLength = 16; # we have to show enough to make it visible...
  global gbmNotProvidedLoaded, gz0NotProvided;
  if not gbmNotProvidedLoaded:
    gbmNotProvidedLoaded = True;
    try: # mDebugOutput use is Optional
      from mNotProvided import zNotProvided;
    except ModuleNotFoundError as oException:
      if oException.args[0] != "No module named 'mNotProvided'":
        raise;
    else:
      gz0NotProvided = zNotProvided;
  if xValue is None:
    sValue = "None";
  elif gz0NotProvided is not None and id(xValue) == id(gz0NotProvided):
    sValue = "zNotProvided";
  elif isinstance(xValue, (str, int, float, bool, bytes)):
    sValue = repr(xValue);
  else:
    # We will recursively process elements of lists, sets, tuples, dicts, etc.
    # This can cause a loop, so we track which values we're already processing
    # and when we encounter a value for the second time, we return a reference
    # to the first time we encountered it instead of full details. This should
    # prevent further loops.
    if axAlreadyProcessingValues is None:
      axAlreadyProcessingValues = [];
    bRecursiveCall = xValue in axAlreadyProcessingValues;
    if bRecursiveCall:
      sId = "#%d" % (axAlreadyProcessingValues.index(xValue) + 1,);
    else:
      axAlreadyProcessingValues.append(xValue);
      sId = "#%d" % (len(axAlreadyProcessingValues),);
    def fsEnumerate(axValues, fsProcessValue):
      assert not bRecursiveCall;
      return ", ".join([
        fsProcessValue(xValue)
        for xValue in axValues
      ]);
    if isinstance(xValue, set):
      if bRecursiveCall:
        sDetails = "...";
      else:
        sDetails = fsEnumerate(xValue, lambda xValue: fsToString(xValue, uMaxLength, axAlreadyProcessingValues));
      sValue = "set(%s)%s" % (sDetails, sId);
    elif isinstance(xValue, tuple):
      if bRecursiveCall:
        sDetails = "...";
      else:
        sDetails = fsEnumerate(xValue, lambda xValue: fsToString(xValue, uMaxLength, axAlreadyProcessingValues));
      sValue = "tuple(%s)%s" % (sDetails, sId);
    elif isinstance(xValue, list):
      if bRecursiveCall:
        sDetails = "...";
      else:
        sDetails = fsEnumerate(xValue, lambda xValue: fsToString(xValue, uMaxLength, axAlreadyProcessingValues));
      sValue = "[%s]%s" % (sDetails, sId);
    elif isinstance(xValue, dict):
      if bRecursiveCall:
        sDetails = "...";
      else:
        sDetails = fsEnumerate(list(xValue.items()), lambda txName_and_Value: "%s: %s" % (
          fsToString(txName_and_Value[0], uMaxLength, axAlreadyProcessingValues),
          fsToString(txName_and_Value[1], uMaxLength, axAlreadyProcessingValues),
        ));
      sValue = "{%s}%s" % (sDetails, sId);
    elif isinstance(xValue, types.MethodType):
      if isinstance(xValue.__self__, type):
        sDetails = "method %s.%s" % (xValue.__self__.__name__, xValue.__name__);
      else:
        sDetails = "method %s.%s" % (xValue.__self__.__class__.__name__, xValue.__name__);
      if hasattr(xValue, "__func__") and hasattr(xValue.__func__, "__code__"):
        if bRecursiveCall:
          sDetails += " ...";
        else:
          sDetails += " @ %s%s%d" % (
            xValue.__func__.__code__.co_filename,
            dxConfig["sLineNumberAfterPathPrefix"],
            xValue.__func__.__code__.co_firstlineno,
          );
      sValue = "<%s %s>" % (sDetails, sId);
    elif isinstance(xValue, types.FunctionType):
      sDetails = "function %s" % (xValue.__name__,);
      if hasattr(xValue, "__code__"):
        if bRecursiveCall:
          sDetails += " ...";
        else:
          sDetails += " @ %s%s%d" % (
            xValue.__code__.co_filename,
            dxConfig["sLineNumberAfterPathPrefix"],
            xValue.__code__.co_firstlineno
          );
      sValue = "<%s %s>" % (sDetails, sId);
    elif inspect.isclass(getattr(xValue, "__class__", None)):
      sDetails = "instance %s:%s" % (xValue.__class__.__module__, xValue.__class__.__name__);
      if bRecursiveCall:
        sDetails += " ...";
      else:
        try:
          sRepr = repr(xValue);
        except Exception as oException:
          try:
            sDetails += f" ({oException})";
          except:
            sDetails += " (cannot get details)";
        else:
          if sRepr[:1] == "<" and sRepr[-1:] == ">":
            sDetails = sRepr[1:-1];
          else:
            sDetails += " " + sRepr;
      sValue = "<%s %s>" % (sDetails, sId);
    elif inspect.isclass(xValue):
      sDetails = "%s:%s" % (str(xValue.__module__), str(xValue.__name__));
      sValue = "<%s %s>" % (sDetails, sId);
    else:
      raise AssertionError("Unknown object type %s" % (type(xValue),));
  if uMaxLength is not None and len(sValue) > uMaxLength:
    sValue = sValue[:uMaxLength - 7] + "… " + sValue[-5:];
  return sValue;
