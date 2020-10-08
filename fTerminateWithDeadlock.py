import os, threading;

from .cCallStack import cCallStack;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fsToString import fsToString;
from .fTerminateWithConsoleOutput import fTerminateWithConsoleOutput;
from .mColors import *;


def fTerminateWithDeadlock(sMessage = None, aasConsoleOutputLines = None, uDeadlockedWithThreadId = None):
  oPythonThread = threading.currentThread();
  sTitle = "Deadlock reported";
  doStack_by_uThreadId = dict([
    (oStack.uThreadId, oStack)
    for oStack in cCallStack.faoForAllThreads(
      uCurrentThreadEndStackOffset = 1
    )
  ]);
  if sMessage is not None:
    assert aasConsoleOutputLines is None, \
        "Cannot provide both sMessage and aasConsoleOutputLines!";
    aasConsoleOutputLines = [
      [guExceptionInformationHighlightColor, sMessage],
    ];
  else:
    assert aasConsoleOutputLines is not None, \
        "Cannot have sMessage == None and aasConsoleMessage == None";
  
  if uDeadlockedWithThreadId in [oPythonThread.ident, None]:
    aasConsoleOutputLines += [
      [
        guExceptionInformationColor, "This deadlock was detected in thread ",
        guExceptionInformationHighlightColor, "%d/0x%X" % (oPythonThread.ident, oPythonThread.ident),
        guExceptionInformationColor, ".",
      ],
      [],
    ] + faasCreateConsoleOutputForStack(doStack_by_uThreadId[oPythonThread.ident]);
    if uDeadlockedWithThreadId is None:
      if len(doStack_by_uThreadId) == 1:
        aasConsoleOutputLines += [
          [],
          [guExceptionInformationColor, "No other threads were running."],
        ]
      else:
        aasConsoleOutputLines += [
          [],
          [guExceptionInformationColor, "The following additional threads were running:"],
          [],
        ]
        for uThreadId in sorted(doStack_by_uThreadId.keys()):
          if uThreadId != oPythonThread.ident:
            aasConsoleOutputLines += faasCreateConsoleOutputForStack(doStack_by_uThreadId[uThreadId]);
  else:
    aasConsoleOutputLines += [
      [
        guExceptionInformationColor, "This deadlock was detected between thread ",
        guExceptionInformationHighlightColor, "%d/0x%X" % (oPythonThread.ident, oPythonThread.ident),
        guExceptionInformationColor, " and thread ",
        guExceptionInformationHighlightColor, "%d/0x%X" % (uDeadlockedWithThreadId, uDeadlockedWithThreadId),
        guExceptionInformationColor, ".",
        [],
      ],
    ] + faasCreateConsoleOutputForStack(doStack_by_uThreadId[oPythonThread.ident]) + [
      [],
    ] + faasCreateConsoleOutputForStack(doStack_by_uThreadId[uDeadlockedWithThreadId]);
  fTerminateWithConsoleOutput(sTitle, aasConsoleOutputLines)
