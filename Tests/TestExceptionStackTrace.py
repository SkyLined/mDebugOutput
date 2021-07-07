import gc, inspect, sys, traceback, types;
sys.path.append("..");
from mDebugOutput.cCallStack import cCallStack;
from mDebugOutput.fTerminateWithException import fTerminateWithException;

class cOldStyleTest():
  def __init__(oSelf, fErrorFunction):
    try:
      oSelf.fTestOldStyleInstanceMethod(fErrorFunction);
    except:
      raise;
  
  def fTestOldStyleInstanceMethod(oSelf, fErrorFunction):
    oSelf.__class__.fTestOldStyleClassMethod(fErrorFunction);
  
  @classmethod
  def fTestOldStyleClassMethod(cClass, fErrorFunction):
    cClass.fTestOldStyleStaticMethod(fErrorFunction);

  @staticmethod
  def fTestOldStyleStaticMethod(fErrorFunction):
    cNewStyleTest(fErrorFunction);
  
class cNewStyleTest(object):
  def __init__(oSelf, fErrorFunction):
    try:
      oSelf.fTestNewStyleInstanceMethod(fErrorFunction);
    except:
      raise;
  
  def fTestNewStyleInstanceMethod(oSelf, fErrorFunction):
    oSelf.__class__.fTestNewStyleClassMethod(fErrorFunction);
  
  @classmethod
  def fTestNewStyleClassMethod(cClass, fErrorFunction):
    cClass.fTestNewStyleStaticMethod(fErrorFunction);

  @staticmethod
  def fTestNewStyleStaticMethod(fErrorFunction):
    fErrorFunction();
  
def fErrorFunction():
  assert 0, "";

def fDumpObject(xObject):
  print((",-- %s %s " % (type(xObject).__name__, repr(xObject))).ljust(80, "-"));
  for sName in dir(xObject):
    if sName not in [
      "__cmp__",
      "__delattr__", "__doc__",
      "__format__",
      "__get__", "__getattribute__",
      "__hash__",
      "__reduce__", "__reduce_ex__", "__repr__",
      "__setattr__", "__sizeof__", "__str__", "__subclasshook__"
    ]:
      print("| %s = %s" % (sName, getattr(xObject, sName)));
  if isinstance(xObject, dict):
    print("|-- dict pairs ".ljust(80, "-"));
    for (sName, xValue) in xObject.items():
      print("| %s: %s" % (sName, repr(xValue)));
  print("|-- Referrers ".ljust(80, "-"));
  for xReferrer in gc.get_referrers(xObject):
    print("| %s" % repr(xReferrer)[:200]);
  print(("'").ljust(80, "-"));

def fTestFunction(fErrorFunction):
  cOldStyleTest(fErrorFunction);

try:
  fTestFunction(fErrorFunction);
except Exception as oException:
  fTerminateWithException(oException);
