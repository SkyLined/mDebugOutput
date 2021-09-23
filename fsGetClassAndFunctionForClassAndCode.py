import inspect, sys;

gbDebugOutput = True;

def fsGetClassAndFunctionForClassAndCode(cClass, oCode):
  sFunctionName = oCode.co_name;
  sCodeFileName = oCode.co_filename;
  asLog = [];
  if gbDebugOutput: asLog.append("Looking for %s (%s from %s)" % (repr(oCode), sFunctionName, sCodeFileName));
  
  def foGetCodeForFunction(xPotentialFunction):
    if not xPotentialFunction:
      return None;
    # Handle @ShowDebugOutput wrapped functions:
    fxWrappedFunction = getattr(xPotentialFunction, "fxWrappedFunction", None);
    if fxWrappedFunction:
      return fxWrappedFunction.__code__;
    return getattr(xPotentialFunction, "func_code", None);
  
  def fszGetCallDescriptorForClassAndAttribute(cPotentialClass, xAttribute):
    if oCode is foGetCodeForFunction(xAttribute): # function
      return "%s.%s" % (cPotentialClass.__name__, sFunctionName)
    
    oMethodFunctionCode = foGetCodeForFunction(getattr(xAttribute, "__func__", None));
    if oMethodFunctionCode:
      if oCode is oMethodFunctionCode: # (class/static)method
        return "%s.%s" % (cPotentialClass.__name__, sFunctionName)
      if gbDebugOutput: asLog.append("%s.%s -> method = %s" % (cPotentialClass.__name__, sFunctionName, repr(oMethodFunctionCode)));
      return None;
    oGetterCode = foGetCodeForFunction(getattr(xAttribute, "fget", None));
    if oCode is oGetterCode: # property getter
      return "%s.get:%s" % (cPotentialClass.__name__, sFunctionName)
    oSetterCode = foGetCodeForFunction(getattr(xAttribute, "fset", None));
    if oCode is oSetterCode: # property setter
      return "%s.set:%s" % (cPotentialClass.__name__, sFunctionName)
    oDeleterCode = foGetCodeForFunction(getattr(xAttribute, "fdel", None));
    if oCode is oDeleterCode: # property deleter
      return "%s.delete:%s" % (cPotentialClass.__name__, sFunctionName)
    if oGetterCode or oSetterCode or oDeleterCode:
      if gbDebugOutput: 
        if oGetterCode: asLog.append("%s.get %s -> %s" % (cPotentialClass.__name__, sFunctionName, repr(oGetterCode)));
        if oSetterCode: asLog.append("%s.get %s -> %s" % (cPotentialClass.__name__, sFunctionName, repr(oSetterCode)));
        if oDeleterCode: asLog.append("%s.get %s -> %s" % (cPotentialClass.__name__, sFunctionName, repr(oDeleterCode)));
      return;
    if gbDebugOutput: asLog.append("%s.%s -> unhandled %s" % (cPotentialClass.__name__, sFunctionName, repr(xAttribute)));
    return None;
  atxPotentialClassesAndAttributeNames = [];
  acUnprocessedClasses = [cClass];
  while acUnprocessedClasses:
    cUnprocessedClass = acUnprocessedClasses.pop(0);
    for cBaseClass in cUnprocessedClass.__bases__:
      if cBaseClass not in (None, object):
        acUnprocessedClasses.append(cBaseClass);
    sClassFilename = getattr(sys.modules.get(cUnprocessedClass.__module__), "__file__", None);
    if sClassFilename != sCodeFileName:
      if gbDebugOutput: asLog.append("%s -> source file is %s" % (cUnprocessedClass.__name__, sClassFilename));
      continue;
    sMangledFunctionName = "_%s_%s" % (cUnprocessedClass.__name__, sFunctionName[1:]) if sFunctionName.startswith("__") else None;
    if hasattr(cUnprocessedClass, sFunctionName):
      atxPotentialClassesAndAttributeNames.insert(0, (cUnprocessedClass, sFunctionName));
    elif sMangledFunctionName:
      atxPotentialClassesAndAttributeNames.insert(0, (cUnprocessedClass, sMangledFunctionName));
    else:
      if gbDebugOutput: asLog.append("%s.%s -> not found" % (cUnprocessedClass.__name__, sFunctionName));
      continue;
  for (cPotentialClass, sAttributeName) in atxPotentialClassesAndAttributeNames:
    xAttribute = getattr(cPotentialClass, sAttributeName);
    szCallDescriptor = fszGetCallDescriptorForClassAndAttribute(cPotentialClass, xAttribute);
    if szCallDescriptor: return szCallDescriptor;
  return "%s?.%s" % (cClass.__name__, sFunctionName);

if __name__ == "__main__":
  def fOutputCaller(cClass):
    oCode = inspect.currentframe().f_back.f_code;
    print(fsGetClassAndFunctionForClassAndCode(cClass, oCode));
    
  class a(object):
    @staticmethod
    def fStaticA():
      fOutputCaller(a);
    @classmethod
    def fClassA(cClass):
      fOutputCaller(cClass);
    def fMethodA(o):
      fOutputCaller(o.__class__);
    
    @staticmethod
    def fStatic():
      fOutputCaller(a);
    @classmethod
    def fClass(cClass):
      fOutputCaller(cClass);
    def fMethod(o):
      fOutputCaller(o.__class__);
    
  class b(a):
    @staticmethod
    def fStaticB():
      fOutputCaller(b);
      a.fStaticA();
    @classmethod
    def fClassB(cClass):
      fOutputCaller(cClass);
      cClass.fClassA();
    def fMethodB(o):
      fOutputCaller(o.__class__);
      o.fMethodA();
    
    @staticmethod
    def fStatic():
      fOutputCaller(b);
      super(b, b).fStatic();
    @classmethod
    def fClass(cClass):
      fOutputCaller(cClass);
      super(b, cClass).fClass();
    def fMethod(o):
      fOutputCaller(o.__class__);
      super(b, o).fMethod();
  
  class c(b):
    @staticmethod
    def fStatic():
      fOutputCaller(c);
      super(c, c).fStatic();
    @classmethod
    def fClass(cClass):
      fOutputCaller(cClass);
      super(c, cClass).fClass();
    def fMethod(o):
      fOutputCaller(o.__class__);
      super(c, o).fMethod();
  
  o=c();
  print("-" * 80);
  o.fStaticA();
  print("-" * 80);
  o.fStaticB();
  print("-" * 80);
  o.fClassA();
  print("-" * 80);
  o.fClassB();
  print("-" * 80);
  o.fMethodA();
  print("-" * 80);
  o.fMethodB();
  print("-" * 80);
  o.fStatic();
  print("-" * 80);
  o.fClass();
  print("-" * 80);
  o.fMethod();
