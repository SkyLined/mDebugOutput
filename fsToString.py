import inspect, types;

gbmNotProvidedLoaded = False; # mNotProvided is loaded JIT to prevent import dependency issues.
gz0NotProvided = None;
def fsToString(xData, uMaxLength = 1000):
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
  
  fsEnumerate = lambda sFormatString, axValues, fsProcessValue: (
    sFormatString % ", ".join([fsProcessValue(xValue) for xValue in axValues])
  );
  sId = "#%X" % id(xData);
  if xData is None:
    sData = "None";
    sId = ""; # Not relevant;
  elif gz0NotProvided is not None and id(xData) == id(gz0NotProvided):
    sData = "zNotProvided";
    sId = ""; # Not relevant;
  elif isinstance(xData, type):
    sData = repr(xData); # types
  elif isinstance(xData, types.MethodType):
    if isinstance(xData.__self__, type):
      sData = "method %s.%s" % (xData.__self__.__name__, xData.__name__);
    else:
      sData = "method %s(#%X).%s" % (xData.__self__.__class__.__name__, id(xData.__self__), xData.__name__);
    if hasattr(xData, "__func__") and hasattr(xData.__func__, "__code__"):
      sData += " @ %s/%d" % (xData.__func__.__code__.co_filename, xData.__func__.__code__.co_firstlineno);
  elif isinstance(xData, types.FunctionType):
    sData = "function %s" % (xData.__name__,);
    if hasattr(xData, "__code__"):
      sData += " @ %s/%d" % (xData.__code__.co_filename, xData.__code__.co_firstlineno);
  elif isinstance(xData, set):
    sData = fsEnumerate("set(%s)", xData, lambda xValue: fsToString(xValue, uMaxLength));
  elif isinstance(xData, tuple):
    sData = fsEnumerate("tuple(%s)", xData, lambda xValue: fsToString(xValue, uMaxLength));
  elif isinstance(xData, list):
    sData = fsEnumerate("[%s]", xData, lambda xValue: fsToString(xValue, uMaxLength));
  elif isinstance(xData, dict):
    sData = fsEnumerate("{%s}", list(xData.items()), lambda txName_and_Value: "%s: %s" % (
      fsToString(txName_and_Value[0], uMaxLength),
      fsToString(txName_and_Value[1], uMaxLength)
    ));
  elif isinstance(xData, (str, int, float, bool)):
    sData = repr(xData)
    sId = ""; # Not relevant for these types.
  elif inspect.isclass(getattr(xData, "__class__", None)):
    try:
      sData = repr(xData);
    except:
      sData = "<instance %s:%s>" % (str(xData.__class__.__module__), str(xData.__class__.__name__));
    else:
      if sData[:1] != "<":
        sData = "<instance %s:%s %s>" % (str(xData.__class__.__module__), str(xData.__class__.__name__), repr(sData));
  elif inspect.isclass(xData):
    sData = "<%s:%s>" % (str(xData.__module__), str(xData.__name__));
  else:
    raise AssertionError("Unknown object type %s: %s" % (type(xData), repr(xData)));
  if uMaxLength is not None:
    uMaxLength -= len(sId); # id is always shown
    if uMaxLength < 16: uMaxLength = 16; # we have to show enough to make it visible...
    if len(sData) > uMaxLength:
      sData = sData[:uMaxLength - 8] + " \xFA\xFA\xFA " + sData[-3:];
  return sData + sId;
