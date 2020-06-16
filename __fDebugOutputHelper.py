import os, threading, time, traceback;

from .mGlobals import *;
from oConsole import oConsole;

gnStartTime = time.clock();
guIndentation_by_uThreadId = {};
guThreadColor_by_uThreadId = {};
gauThreadColors = [0x0F07, 0x0F0C, 0x0F0E, 0x0F0A, 0x0F0B, 0x0F09, 0x0F0D];
aoPythonThreads = threading.enumerate();
assert len(aoPythonThreads) == 1, \
    "Expected only 1 thread!";
guMainThreadId = aoPythonThreads[0].ident;

def __fDebugOutputHelper(uThreadId, sThreadName, sSourceFilePath, uLineNumber, xOutputLines, uIndentationChange = 0, bAlwaysShow = False, bLineNumberIsUncertain = False):
  global guThreadColor_by_uThreadId, gauThreadColors;
  asOutputLines = xOutputLines if isinstance(xOutputLines, list) else [xOutputLines];
  sThreadIdHeader = "".join([
    "%4X" % uThreadId,
    "\x07" if uThreadId == guMainThreadId else "\xFA",
    sThreadName or "<unnamed>",
  ])[:64].ljust(64);
  sTime = "%8.4f" % (time.clock() - gnStartTime);
  uIndex = 0;
  uIndentation = guIndentation_by_uThreadId.setdefault(uThreadId, 0);
  if uIndentationChange == 1:
    guIndentation_by_uThreadId[uThreadId] += 1;
    sSingleIndentationHeader = sFirstIndentationHeader = (" \xB3" * (uIndentation - 1)) + (" \xC3" if uIndentation else "") + "\xC4\xBF";
    uIndentation += 1;
    sMiddleIndentationHeader = sLastIndentationHeader = (" \xB3" * uIndentation);
  elif uIndentationChange != -1:
    assert uIndentationChange == 0, \
        "Invalid uIndentationChange value %d" % uIndentationChange;
    sSingleIndentationHeader = sFirstIndentationHeader = \
        sMiddleIndentationHeader = sLastIndentationHeader = " \xB3" * uIndentation;
  else:
    if guIndentation_by_uThreadId[uThreadId] == 1:
      del guIndentation_by_uThreadId[uThreadId];
    else:
      guIndentation_by_uThreadId[uThreadId] -= 1;
    sFirstIndentationHeader = sMiddleIndentationHeader = " \xB3" * uIndentation;
    uIndentation -= 1;
    sSingleIndentationHeader = sLastIndentationHeader = (" \xB3" * (uIndentation - 1)) + (" \xC3" if uIndentation else "") + "\xC4\xD9";
  sLineNumber = str(uLineNumber) + ("+" if bLineNumberIsUncertain else "");
  sSourceCodeHeader = "%40s" % ("%s/%-5s" % (os.path.basename(sSourceFilePath), (sLineNumber)))[-40:];
  # Add headers to all output lines:
  asActualOutput = [];
  for sOutputLine in asOutputLines:
    if len(asOutputLines) == 1:
      sIndentationHeader = sSingleIndentationHeader;
      sMessageHeader = "";
    elif uIndex == 0:
      sIndentationHeader = sFirstIndentationHeader;
      sMessageHeader = "\xDA";
    elif uIndex != len(asOutputLines) - 1:
      sIndentationHeader = sMiddleIndentationHeader;
      sMessageHeader = "\xB3";
      sTime = ": ".rjust(len(sTime));
      sThreadIdHeader = " \xFA".ljust(len(sThreadId));
      sSourceCodeHeader = "\xFA    ".rjust(len(sSourceCodeHeader));
    else:
      sIndentationHeader = sLastIndentationHeader;
      sMessageHeader = "\xC0";
      sTime = "\xFA\xFA ".rjust(len(sTime));
      sThreadIdHeader = " \xFA\xFA".ljust(len(sThreadId));
      sSourceCodeHeader = "\xFA\xFA\xFA    ".rjust(len(sSourceCodeHeader));
    uIndex += 1;
    asActualOutput.append("\xB3".join([
      sTime,
      sThreadIdHeader[:64].ljust(64),
      sSourceCodeHeader,
    ]) + sIndentationHeader + sMessageHeader + sOutputLine);
  # Actually output the lines:
  oConsole.fLock();
  try:
    uThreadColor = guThreadColor_by_uThreadId.get(uThreadId);
    if uThreadColor is None:
      duCount_by_uThreadColor = dict([(uThreadColor, 0) for uThreadColor in gauThreadColors]);
      for uThreadColor in guThreadColor_by_uThreadId.values():
        duCount_by_uThreadColor[uThreadColor] += 1;
      uLowestCount = min([uCount for uCount in duCount_by_uThreadColor.values()]);
      for uThreadColor in gauThreadColors:
        if duCount_by_uThreadColor[uThreadColor] == uLowestCount:
          guThreadColor_by_uThreadId[uThreadId] = uThreadColor;
          break;
      else:
        raise AssertionError("Stars are not alligned correctly.");
    for sActualOutputLine in asActualOutput:
      oConsole.fPrint(uThreadColor, sActualOutputLine);
  finally:
    oConsole.fUnlock();
  return True;