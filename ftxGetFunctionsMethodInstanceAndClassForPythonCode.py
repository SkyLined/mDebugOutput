import gc, types;

from .ftocGetInstanceAndClassForUnknown import ftocGetInstanceAndClassForUnknown;

gbDebugCacheHelper = False; # Used during development to show decision making.

def ftxGetFunctionsMethodInstanceAndClassForPythonCode(oPythonCode, xFirstArgumentValueInCall = None):
  if gbDebugCacheHelper: print("--- Looking up %s ---" % repr(oPythonCode));
  sFunctionName = oPythonCode.co_name;
  if gbDebugCacheHelper: print("sFunctionName is %s" % sFunctionName);
  
  if xFirstArgumentValueInCall is not None:
    if gbDebugCacheHelper: print("xFirstArgumentValueInCall = %s: %s" % \
        (repr(type(xFirstArgumentValueInCall)), repr(xFirstArgumentValueInCall)));
    (oInstance, cClass) = ftocGetInstanceAndClassForUnknown(xFirstArgumentValueInCall);
    if gbDebugCacheHelper: print("oInstance = %s" % (("object %s" % repr(oInstance)) if oInstance is not None else "None"));
    if gbDebugCacheHelper: print("cClass = %s" % (("class %s" % repr(cClass)) if cClass else "None"));
    fxClassOrStaticMethod = getattr(cClass, sFunctionName, None);
    if not isinstance(fxClassOrStaticMethod, types.MethodType):
      if hasattr(cClass, sFunctionName):
        if gbDebugCacheHelper: print("Not an instance or class method: attribute %s is not a method in class but %s" % \
            (sFunctionName, fxClassOrStaticMethod));
      else:
        if gbDebugCacheHelper: print("Not an instance or class method: attribute %s not found in class" % \
            (sFunctionName));
      oInstance = None;
      cClass = None;
    else:
      if gbDebugCacheHelper: print("fxClassOrStaticMethod may be %s" % repr(fxClassOrStaticMethod));
      fxFunction = fxClassOrStaticMethod.__func__;
      fxWrappedFunction = None;#getattr(fxFunction, "fxWrappedFunction", None);
      fxVisibleFunction = fxWrappedFunction or fxFunction;
      if fxWrappedFunction:
        if gbDebugCacheHelper: print("%s wraps %s" % (fxFunction.__name__, fxWrappedFunction.__name__));
      if sFunctionName is not fxVisibleFunction.__name__:
        if gbDebugCacheHelper: print("Not an instance or class method: attribute %s in class is a function with name %s" % \
            (sFunctionName, fxVisibleFunction.__name__));
      elif oPythonCode is not fxVisibleFunction.__code__:
        if gbDebugCacheHelper: print("Not an instance or class method: attribute %s in class is a function with different code %s" % \
            (sFunctionName, fxVisibleFunction.__code__.co_name));
      else:
        fInstanceMethod = oInstance is not None and getattr(oInstance, sFunctionName, None);
        if not isinstance(fInstanceMethod, types.MethodType):
          if gbDebugCacheHelper: print("Not an instance method: attribute %s in instance is not a method but %s" % \
              (sFunctionName, repr(fInstanceMethod)));
        elif fInstanceMethod.__name__ != fxClassOrStaticMethod.__name__:
          if gbDebugCacheHelper: print("Not an instance method: attribute %s in instance is a method with name %s" % \
              (sFunctionName, fInstanceMethod.__name__));
        elif fInstanceMethod.__self__ is not oInstance:
          if gbDebugCacheHelper: print("Not an instance method: attribute %s in instance is a method with im_self %s" % \
              (sFunctionName, repr(fInstanceMethod.__self__)));
        elif fInstanceMethod.__self__.__class__ is not cClass:
          if gbDebugCacheHelper: print("Not an instance method: attribute %s in instance is a method with im_class %s" % \
              (sFunctionName, repr(fInstanceMethod.__self__.__class__)));
        else:
          if gbDebugCacheHelper: print("Found instance method %s" % repr(fInstanceMethod));
          return (
            [fInstanceMethod.__func__], # Functions
            fInstanceMethod, # Method
            oInstance, # Instance
            cClass, # Class
          );
        if fxClassOrStaticMethod.__self__ is not cClass:
          if gbDebugCacheHelper: print("Not a class method: attribute %s in class is a method with im_self %s" % \
              (sFunctionName, repr(fxClassOrStaticMethod.__self__)));
        elif fxClassOrStaticMethod.__self__.__class__ not in (type, type):
          if gbDebugCacheHelper: print("Not a class method: attribute %s in class is a method with im_class %s" % \
              (sFunctionName, repr(fxClassOrStaticMethod.__self__.__class__)));
        else:
          if gbDebugCacheHelper: print("Found class or static method %s" % repr(fxClassOrStaticMethod));
          return (
            [fxClassOrStaticMethod.__func__], # Functions
            fxClassOrStaticMethod, # Method
            None, # Instance
            cClass, # Class
          );
  # If this is a method, it's going to be a static method (a function that is an attribute of a class).
  # But it may also be a function, so let's track those as well, just in case:
  afxFunctions = [];
  for xUnknown in gc.get_objects():
    if (
      isinstance(xUnknown, types.FunctionType)
      and xUnknown.__code__ is oPythonCode
      and xUnknown.__name__ == sFunctionName
    ):
      afxFunctions.append(xUnknown);
      continue;
    if isinstance(xUnknown, type):
      fxStaticMethodFunction = getattr(xUnknown, sFunctionName, None);
      if (
        isinstance(fxStaticMethodFunction, types.FunctionType)
        and fxStaticMethodFunction.__code__ is oPythonCode
        and fxStaticMethodFunction.__name__ == sFunctionName
      ):
        if gbDebugCacheHelper: print("Found static method %s" % repr(fxStaticMethodFunction));
        return (
          [fxStaticMethodFunction], # Functions
          None, # Method
          None, # Instance
          xUnknown, # Class
        );
  # It's not a static method, but it could be we found it as one or more functions or it is module code:
  if gbDebugCacheHelper: 
    if len(afxFunctions) > 1:
      print("Found %d functions" % len(afxFunctions));
    elif len(afxFunctions) == 1:
      print("Found function %s" % repr(afxFunctions[0]));
    else:
      print("Found module");
  return (
    afxFunctions, # Functions
    None, # Method
    None, # Instance
    None, # Class
  );
