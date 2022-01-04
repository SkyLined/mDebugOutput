import json, os, sys;

from mDebugOutput.cCallStack import cCallStack;
from mDebugOutput.faasCreateConsoleOutputForException import faasCreateConsoleOutputForException;
from mDebugOutput import fTerminateWithException;

def fRaiseAssertionError():
  assert False, "An assertionError\nWith two lines of message";

def fRaiseAttributeErrorOnClass():
  Exception.foobar;
def fRaiseAttributeErrorOnInstance():
  Exception().foobar;
def fRaiseAttributeErrorOnModule():
  sys.foobar;

def fRaiseModuleNotFoundError():
  import foobar;
def fRaiseRelativeImportError():
  from .foobar import foobar;
def fRaiseImportNameNotFoundError():
  from fTestExceptions import foobar;

def fRaiseJSONDecodeError():
  json.loads("foobar");

def fRaiseKeyError():
  {}["foobar"];

def fRaiseUndefinedNameError():
  foobar;
def fRaiseUninitializedNameError():
  foobar;
  foobar = 1;

def fRaiseSyntaxError():
  exec("!foobar");

def fRaiseBadKeywordArgumentTypeError():
  Exception(foobar = 1);

def fRaiseBadNumberOfArgumentsTypeError():
  fRaiseBadNumberOfArgumentsTypeError("foobar");

def fRaiseUnicodeDecodeError():
  bytes("foobar\u4141", "ascii", "strict");

def fRaiseTooManyValuesInTupleValueError():
  (foobar,) = (1,2);

def fRaiseTooFewValuesInTupleValueError():
  (foobar,) = tuple();

def fRaiseWindowsError1():
  os.mkdir("*")
def fRaiseWindowsError2():
  open("*")
def fRaiseWindowsError3():
  open(":");
def fRaiseWindowsError4():
  os.mkdir(__file__);
def fRaiseWindowsError5():
  open(os.getenv("windir") + "\\foobar", "wb");

def fTestExceptionMessages():
  for fRaiseException in (
    fRaiseAssertionError,
    fRaiseAttributeErrorOnClass,
    fRaiseAttributeErrorOnInstance,
    fRaiseAttributeErrorOnModule,
    fRaiseModuleNotFoundError,
    fRaiseRelativeImportError,
    fRaiseImportNameNotFoundError,
    fRaiseJSONDecodeError,
    fRaiseKeyError,
    fRaiseUndefinedNameError,
    fRaiseUninitializedNameError,
    fRaiseSyntaxError,
    fRaiseBadKeywordArgumentTypeError,
    fRaiseBadNumberOfArgumentsTypeError,
    fRaiseUnicodeDecodeError,
    fRaiseTooManyValuesInTupleValueError,
    fRaiseTooFewValuesInTupleValueError,
    fRaiseWindowsError1,
    fRaiseWindowsError2,
    fRaiseWindowsError3,
    fRaiseWindowsError4,
    fRaiseWindowsError5,
  ):
    try:
      fRaiseException();
    except Exception as oException:
      oTraceback = sys.exc_info()[2];
      o0PythonThread = None;
      oStack = cCallStack.foFromTraceback(oTraceback, o0PythonThread);
      aasOutputlines = faasCreateConsoleOutputForException(oException, oTraceback, oStack);
      for asOutputLine in aasOutputlines:
        sOutput = "";
        while asOutputLine:
          xOutput = asOutputLine.pop(0);
          if isinstance(xOutput, str):
            sOutput += xOutput;
          elif isinstance(xOutput, list):
            asOutputLine = xOutput + asOutputLine;
          else:
            assert isinstance(xOutput, int), \
                "Unexpected type in output: %s" % repr(xOutput);
        if sOutput in ["Exception attributes:", "Additional exception attributes:"]:
          # This was not processed properly; show the output again and terminate with an error code.
          fTerminateWithException(oException, 1);
    else:
      raise AssertionError("%s did not raise an exception!?" % fRaiseException);
