import sys, threading;

def fConsoleOutputExceptionDetails(oException, o0Traceback = None, o0PythonThread = None, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  oTraceback = o0Traceback or sys.exc_info()[2];
  oStack = cCallStack.foFromTraceback(oTraceback, o0PythonThread);
  
  sBoxTitle = "Fatal %s.%s Exception in %s" % (
    oException.__class__.__module__, oException.__class__.__name__,
    "thread %d/0x%X (%s)" % (oStack.u0ThreadId, oStack.u0ThreadId, oStack.s0ThreadName or "<unnamed>")
        if oStack.u0ThreadId is not None else "unknown thread"
  );
  
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
    oPythonThread = threading.current_thread();
    doStack_by_uThreadId = dict([
      (oStack.u0ThreadId, oStack)
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
from .mColorsAndChars import *;
