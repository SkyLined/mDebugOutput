import types;

def ftocGetInstanceAndClassForUnknown(xUnknown):
  if isinstance(xUnknown, types.InstanceType):
    oInstance = xUnknown;
    cClass = oInstance.__class__;
  elif isinstance(xUnknown, (types.ClassType, type)):
    oInstance = None;
    cClass = xUnknown;
  elif isinstance(getattr(xUnknown, "__class__", None), type):
    oInstance = xUnknown;
    cClass = oInstance.__class__;
  else:
    oInstance = None;
    cClass = None;
  return (oInstance, cClass);
