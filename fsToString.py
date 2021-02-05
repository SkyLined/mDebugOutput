import inspect, types;

def fsToString(xData, uMaxLength = 1000):
  def fsEnumerate(sFormatString, axValues, fsProcessValue):
    return sFormatString % ", ".join([fsProcessValue(xValue) for xValue in axValues]);
  sId = " #%X" % id(xData);
  if isinstance(xData, types.MethodType):
    if isinstance(xData.im_self, (types.ClassType, type)):
      sData = "method %s.%s" % (xData.im_self.__name__, xData.__name__);
    else:
      sData = "method %s(#%X).%s" % (xData.im_class.__name__, id(xData.im_self), xData.__name__);
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
    sData = fsEnumerate("{%s}", xData.items(), lambda txName_and_Value: "%s: %s" % (
      fsToString(txName_and_Value[0], uMaxLength),
      fsToString(txName_and_Value[1], uMaxLength)
    ));
  elif isinstance(xData, (str, int, unicode, long, float, bool)):
    sData = repr(xData)
    sId = ""; # Not relevant for these types.
  elif (
    isinstance(xData, types.InstanceType) # Old style objects
    or inspect.isclass(getattr(xData, "__class__", None)) # New style objects
  ):
    try:
      sData = repr(xData);
    except:
      sData = xData.__class__.__name__;
      sId = "(#%X)" % id(xData);
    else:
      sId = "";
  elif (
    isinstance(xData, types.ClassType) # Old style classes
    or inspect.isclass(xData) # New style classes
  ):
    sData = xData.__name__;
  else:
    raise AssertionError("Unknown object type %s: %s" % (type(xData), repr(xData)));
  if uMaxLength is not None:
    uMaxLength -= len(sId); # id is always shown
    if uMaxLength < 16: uMaxLength = 16; # we have to show enough to make it visible...
    if len(sData) > uMaxLength:
      sData = sData[:uMaxLength - 8] + " \xFA\xFA\xFA " + sData[-3:];
  return sData + sId;
