import sys, threading;

from .HideInCallStack import HideInCallStack;

@HideInCallStack
def fConsoleOutputExceptionDetails(oException, o0Traceback = None, o0PythonThread = None, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  oTraceback = o0Traceback or sys.exc_info()[2];
  if oTraceback.tb_frame.f_code in gaoHideFunctionsForPythonCodes:
    # Not sure why I am added this code but I believe it may be a special handler for internal errors.
    import os, traceback
    traceback.print_exception(oException.__class__, oException, oTraceback);
  oStack = cCallStack.foFromTraceback(oTraceback, o0PythonThread);
  
  sBoxTitle = "Fatal %s.%s Exception in thread 0x%X" % (oException.__class__.__module__, oException.__class__.__name__, oStack.uThreadId);
  
  aasConsoleOutputLines = faasCreateConsoleOutputForException(oException, oTraceback, oStack);
  
  if a0asAdditionalConsoleOutputLines is not None:
    aasConsoleOutputLines += [
      [],
    ];
    aasConsoleOutputLines += a0asAdditionalConsoleOutputLines;
  
  aasConsoleOutputLines += [
    [],
  ];
  aasConsoleOutputLines += faasCreateConsoleOutputForStack(oStack, oException);
  
  if bShowStacksForAllThread:
    oPythonThread = threading.currentThread();
    doStack_by_uThreadId = dict([
      (oStack.uThreadId, oStack)
      for oStack in cCallStack.faoForAllThreads()
    ]);
    if len(doStack_by_uThreadId) != 1:
      aasConsoleOutputLines += [
        [],
        [guExceptionInformationColor, "The following additional threads were running:"],
        [],
      ]
      for uThreadId in sorted(doStack_by_uThreadId.keys()):
        if uThreadId != oPythonThread.ident:
          aasConsoleOutputLines += faasCreateConsoleOutputForStack(doStack_by_uThreadId[uThreadId]);
  fConsoleOutput(sBoxTitle, aasConsoleOutputLines);

from .cCallStack import cCallStack;
from .faasCreateConsoleOutputForException import faasCreateConsoleOutputForException;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fConsoleOutput import fConsoleOutput;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .mColorsAndChars import *;
