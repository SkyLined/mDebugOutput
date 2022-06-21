import os, threading, time;

from .dxConfig import dxConfig;
from .foConsoleLoader import foConsoleLoader;
from .mGlobals import *;

gnStartTime = time.time();
guIndentation_by_uThreadId = {};
guThreadColor_by_uThreadId = {};
gauThreadColors = [0x0F07, 0x0F0C, 0x0F0E, 0x0F0A, 0x0F0B, 0x0F09, 0x0F0D];
aoPythonThreads = threading.enumerate();
assert len(aoPythonThreads) == 1, \
    "Expected only 1 thread!";
guMainThreadId = aoPythonThreads[0].ident;

def fDebugOutputHelper(u0ThreadId, s0ThreadName, sSourceFilePath, uLineNumber, xOutputLines, uIndentationChange = 0, bAlwaysShow = False, bIsReturnAddress = False):
  global guThreadColor_by_uThreadId, gauThreadColors;
  oConsole = foConsoleLoader();
  
  asOutputLines = xOutputLines if isinstance(xOutputLines, list) else [xOutputLines];
  sThreadIdHeader = "".join([
    "%4X" % u0ThreadId,
    "\u2022" if u0ThreadId == guMainThreadId else "\u00B7",
    s0ThreadName or "<unnamed>",
  ])[:64].ljust(64) if u0ThreadId is not None else "<unknown thread>";
  sTime = "%8.4f" % (time.time() - gnStartTime);
  uIndex = 0;
  uIndentation = guIndentation_by_uThreadId.setdefault(u0ThreadId, 0) if u0ThreadId is not None else 0;
  if uIndentationChange == 1:
    if u0ThreadId is not None:
      guIndentation_by_uThreadId[u0ThreadId] += 1;
    sSingleIndentationHeader = sFirstIndentationHeader = (" \u2502" * (uIndentation - 1)) + (" \u251C" if uIndentation else "") + "\u2500\u2510";
    uIndentation += 1;
    sMiddleIndentationHeader = sLastIndentationHeader = (" \u2502" * uIndentation);
  elif uIndentationChange != -1:
    assert uIndentationChange == 0, \
        "Invalid uIndentationChange value %d" % uIndentationChange;
    sSingleIndentationHeader = sFirstIndentationHeader = \
        sMiddleIndentationHeader = sLastIndentationHeader = " \u2502" * uIndentation;
  else:
    if u0ThreadId is not None:
      if guIndentation_by_uThreadId[u0ThreadId] == 1:
        del guIndentation_by_uThreadId[u0ThreadId];
      else:
        guIndentation_by_uThreadId[u0ThreadId] -= 1;
    sFirstIndentationHeader = sMiddleIndentationHeader = " \u2502" * uIndentation;
    uIndentation -= 1;
    sSingleIndentationHeader = sLastIndentationHeader = (" \u2502" * (uIndentation - 1)) + (" \u251C" if uIndentation else "") + "\u2500\u2518";
  sSourceCodeHeader = (
    "%33s%s%-5s" % (
      os.path.basename(sSourceFilePath),
      dxConfig["sLineNumberAfterPathPrefix"],
      str(uLineNumber) + (
        "\u25C4" if bIsReturnAddress else
        "\u25B2" if uIndentationChange < 0 else # must be an exception!
        " "
      ),
    )
  )[-39:];
  # Add headers to all output lines:
  asActualOutput = [];
  for sOutputLine in asOutputLines:
    if len(asOutputLines) == 1:
      sIndentationHeader = sSingleIndentationHeader;
      sMessageHeader = "";
    elif uIndex == 0:
      sIndentationHeader = sFirstIndentationHeader;
      sMessageHeader = "\u250C";
    elif uIndex != len(asOutputLines) - 1:
      sIndentationHeader = sMiddleIndentationHeader;
      sMessageHeader = "\u2502";
      sTime = ": ".rjust(len(sTime));
      sThreadIdHeader = " \u00B7".ljust(len(sThreadId));
      sSourceCodeHeader = "\u00B7    ".rjust(len(sSourceCodeHeader));
    else:
      sIndentationHeader = sLastIndentationHeader;
      sMessageHeader = "\u2514";
      sTime = "\u00B7\u00B7 ".rjust(len(sTime));
      sThreadIdHeader = " \u00B7\u00B7".ljust(len(sThreadId));
      sSourceCodeHeader = "\u00B7\u00B7\u00B7    ".rjust(len(sSourceCodeHeader));
    uIndex += 1;
    asActualOutput.append("\u2502".join([
      sTime,
      sThreadIdHeader[:64].ljust(64),
      sSourceCodeHeader,
    ]) + sIndentationHeader + sMessageHeader + sOutputLine);
  # Actually output the lines:
  oConsole.fLock();
  try:
    uThreadColor = guThreadColor_by_uThreadId.get(u0ThreadId) if u0ThreadId is not None else gauThreadColors[0];
    if uThreadColor is None:
      duCount_by_uThreadColor = dict([(uThreadColor, 0) for uThreadColor in gauThreadColors]);
      for uThreadColor in guThreadColor_by_uThreadId.values():
        duCount_by_uThreadColor[uThreadColor] += 1;
      uLowestCount = min([uCount for uCount in duCount_by_uThreadColor.values()]);
      for uThreadColor in gauThreadColors:
        if duCount_by_uThreadColor[uThreadColor] == uLowestCount:
          guThreadColor_by_uThreadId[u0ThreadId] = uThreadColor;
          break;
      else:
        raise AssertionError("Stars are not alligned correctly.");
    for sActualOutputLine in asActualOutput:
      oConsole.fOutput(uThreadColor, sActualOutputLine);
  finally:
    oConsole.fUnlock();
  return True;