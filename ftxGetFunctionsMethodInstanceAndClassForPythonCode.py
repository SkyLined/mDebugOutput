import gc, types;

from .ftocGetInstanceAndClassForUnknown import ftocGetInstanceAndClassForUnknown;

gbDebugCacheHelper = False; # Used during development to show decision making.

def ftxGetFunctionsMethodInstanceAndClassForPythonCode(oPythonCode, xFirstArgumentValueInCall = None):
  if gbDebugCacheHelper: print "--- Looking up %s ---" % repr(oPythonCode);
  sFunctionName = oPythonCode.co_name;
  if gbDebugCacheHelper: print "sFunctionName is %s" % sFunctionName;
  
  if xFirstArgumentValueInCall:
    if gbDebugCacheHelper: print "xFirstArgumentValueInCall = %s: %s" % \
        (repr(type(xFirstArgumentValueInCall)), repr(xFirstArgumentValueInCall));
    (oInstance, cClass) = ftocGetInstanceAndClassForUnknown(xFirstArgumentValueInCall);
    if gbDebugCacheHelper: print "oInstance = %s" % (("object %s" % repr(oInstance)) if oInstance else "None");
    if gbDebugCacheHelper: print "cClass = %s" % (("class %s" % repr(cClass)) if cClass else "None");
    fxClassOrStaticMethod = getattr(cClass, sFunctionName, None);
    if not isinstance(fxClassOrStaticMethod, types.MethodType):
      if hasattr(cClass, sFunctionName):
        if gbDebugCacheHelper: print "Not an instance or class method: attribute %s is not a method in class but %s" % \
            (sFunctionName, fxClassOrStaticMethod);
      else:
        if gbDebugCacheHelper: print "Not an instance or class method: attribute %s not found in class" % \
            (sFunctionName);
      oInstance = None;
      cClass = None;
    else:
      if gbDebugCacheHelper: print "fxClassOrStaticMethod may be %s" % repr(fxClassOrStaticMethod);
      fxFunction = fxClassOrStaticMethod.im_func;
      fxWrappedFunction = None;#getattr(fxFunction, "fxWrappedFunction", None);
      fxVisibleFunction = fxWrappedFunction or fxFunction;
      if fxWrappedFunction:
        if gbDebugCacheHelper: print "%s wraps %s" % (fxFunction.func_name, fxWrappedFunction.func_name);
      if sFunctionName is not fxVisibleFunction.func_name:
        if gbDebugCacheHelper: print "Not an instance or class method: attribute %s in class is a function with name %s" % \
            (sFunctionName, fxVisibleFunction.func_name);
      elif oPythonCode is not fxVisibleFunction.func_code:
        if gbDebugCacheHelper: print "Not an instance or class method: attribute %s in class is a function with different code %s" % \
            (sFunctionName, fxVisibleFunction.func_code.co_name);
      else:
        fInstanceMethod = oInstance and getattr(oInstance, sFunctionName, None);
        if not isinstance(fInstanceMethod, types.MethodType):
          if gbDebugCacheHelper: print "Not an instance method: attribute %s in instance is not a method but %s" % \
              (sFunctionName, repr(fInstanceMethod));
        elif fInstanceMethod.__name__ != fxClassOrStaticMethod.__name__:
          if gbDebugCacheHelper: print "Not an instance method: attribute %s in instance is a method with name %s" % \
              (sFunctionName, fInstanceMethod.__name__);
        elif fInstanceMethod.im_self is not oInstance:
          if gbDebugCacheHelper: print "Not an instance method: attribute %s in instance is a method with im_self %s" % \
              (sFunctionName, repr(fInstanceMethod.im_self));
        elif fInstanceMethod.im_class is not cClass:
          if gbDebugCacheHelper: print "Not an instance method: attribute %s in instance is a method with im_class %s" % \
              (sFunctionName, repr(fInstanceMethod.im_class));
        else:
          if gbDebugCacheHelper: print "Found instance method %s" % repr(fInstanceMethod);
          return (
            [fInstanceMethod.im_func], # Functions
            fInstanceMethod, # Method
            oInstance, # Instance
            cClass, # Class
          );
        if fxClassOrStaticMethod.im_self is not cClass:
          if gbDebugCacheHelper: print "Not a class method: attribute %s in class is a method with im_self %s" % \
              (sFunctionName, repr(fxClassOrStaticMethod.im_self));
        elif fxClassOrStaticMethod.im_class not in (types.ClassType, type):
          if gbDebugCacheHelper: print "Not a class method: attribute %s in class is a method with im_class %s" % \
              (sFunctionName, repr(fxClassOrStaticMethod.im_class));
        else:
          if gbDebugCacheHelper: print "Found class or static method %s" % repr(fxClassOrStaticMethod);
          return (
            [fxClassOrStaticMethod.im_func], # Functions
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
      and xUnknown.func_code is oPythonCode
      and xUnknown.func_name == sFunctionName
    ):
      afxFunctions.append(xUnknown);
      continue;
    if isinstance(xUnknown, (types.ClassType, type)):
      fxStaticMethodFunction = getattr(xUnknown, sFunctionName, None);
      if (
        isinstance(fxStaticMethodFunction, types.FunctionType)
        and fxStaticMethodFunction.func_code is oPythonCode
        and fxStaticMethodFunction.func_name == sFunctionName
      ):
        if gbDebugCacheHelper: print "Found static method %s" % repr(fxStaticMethodFunction);
        return (
          [fxStaticMethodFunction], # Functions
          None, # Method
          None, # Instance
          xUnknown, # Class
        );
  # It's not a static method, but it could be we found it as one or more functions or it is module code:
  if gbDebugCacheHelper: 
    if len(afxFunctions) > 1:
      print "Found %d functions" % len(afxFunctions);
    elif len(afxFunctions) == 1:
      print "Found function %s" % repr(afxFunctions[0]);
    else:
      print "Found module";
  return (
    afxFunctions, # Functions
    None, # Method
    None, # Instance
    None, # Class
  );
