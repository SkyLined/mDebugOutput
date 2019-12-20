import os, sys, threading, traceback;

def fFatalExceptionOutput(oException):
  cException, oException2, oTraceBack = sys.exc_info();
  assert oException == oException2, \
      "Wrong exception!?";
  oThread = threading.currentThread();
  atxStack = traceback.extract_tb(oTraceBack);
  asOutputLines = [
    "Fatal %s Exception:" % cException.__name__,
  ] + [
    "  %s = %s" % (sName, fsToString(getattr(oException, sName)))
    for sName in dir(oException)
    if sName[0] != "_"
  ] + [
    "",
    "Thread #%d (%s) Stack:" % (oThread.ident, oThread.name),
  ];
  if cException == SyntaxError:
    atxStack.append((
      oException.filename,
      oException.lineno,
      "<module>",
      oException.text.rstrip("\n").rstrip("\r"),
    ));
  uFrameIndex = 0;
  for (sFileName, uLineNumber, sFunctionName, sCode) in atxStack:
    sSource = "%s/%d" % (sFileName, uLineNumber);
    if sFunctionName != "<module>":
      sSource = "%s @ %s" % (sFunctionName, sSource);
    sHeader = "%s \xC3" % (" \xB3" * (uFrameIndex - 1)) if uFrameIndex > 0 else "";
    asOutputLines.append("%s\xC4\xBF %s" % (sHeader, sSource));
    if sCode:
      sHeader = "%s %s" % (" \xB3" * uFrameIndex, "\xB3" if uFrameIndex != len(atxStack) - 1 else "*");
      asOutputLines.append("%s %s" % (sHeader, sCode.replace("\t", "  ") if sCode else "<no code>"));
    uFrameIndex += 1;
  fDebugOutput(*asOutputLines);
  os._exit(3);

from .fDebugOutput import fDebugOutput;
from .fsToString import fsToString;
