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

def fDebugOutputHelper(u0ThreadId, s0ThreadName, sSourceFilePath, u0LineNumber, xOutputLines, uIndentationChange = 0, bAlwaysShow = False, bIsReturnAddress = False):
  global guThreadColor_by_uThreadId, gauThreadColors;
  oConsole = foConsoleLoader();
  
  asOutputLines = xOutputLines if isinstance(xOutputLines, list) else [xOutputLines];
  sTime = "%8.4f" % (time.time() - gnStartTime);
  sThreadIdHeader = "%5X" % u0ThreadId if u0ThreadId is not None else "?????";
  uIndex = 0;
  uIndentation = guIndentation_by_uThreadId.setdefault(u0ThreadId, 0) if u0ThreadId is not None else 0;
  if uIndentationChange == 1:
    if u0ThreadId is not None:
      guIndentation_by_uThreadId[u0ThreadId] += 1;
    sSingleIndentationHeader = sFirstIndentationHeader = (" :" * (uIndentation - 1)) + (" ├" if uIndentation else "") + "─╮";
    uIndentation += 1;
    sMiddleIndentationHeader = sLastIndentationHeader = (" :" * (uIndentation - 1)) + " │";
  elif uIndentationChange != -1:
    assert uIndentationChange == 0, \
        "Invalid uIndentationChange value %d" % uIndentationChange;
    sSingleIndentationHeader = sFirstIndentationHeader = \
        sMiddleIndentationHeader = sLastIndentationHeader = (" :" * (uIndentation - 1)) + " │";
  else:
    if u0ThreadId is not None:
      if guIndentation_by_uThreadId[u0ThreadId] == 1:
        del guIndentation_by_uThreadId[u0ThreadId];
      else:
        guIndentation_by_uThreadId[u0ThreadId] -= 1;
    sFirstIndentationHeader = sMiddleIndentationHeader = " :" * uIndentation;
    uIndentation -= 1;
    sSingleIndentationHeader = sLastIndentationHeader = (
      (
        (( (" :" * (uIndentation - 1)) + " ├") if uIndentation else "") +
        "─╯"
      ) if bIsReturnAddress else (
        (" :" * uIndentation) + "←✘"
      )
    );
  sSourceCodeHeader = (
    "%s%s%-5s" % (
      os.path.basename(sSourceFilePath),
      dxConfig["sLineNumberAfterPathPrefix"] if u0LineNumber is not None else " " * len(dxConfig["sLineNumberAfterPathPrefix"]),
      str(u0LineNumber) if u0LineNumber is not None else "",
    )
  ).rjust(50)[-50:];
  # Add headers to all output lines:
  asActualOutput = [];
  for sOutputLine in asOutputLines:
    if len(asOutputLines) == 1:
      sIndentationHeader = sSingleIndentationHeader;
      sMessageHeader = " ";
    elif uIndex == 0:
      sIndentationHeader = sFirstIndentationHeader;
      sMessageHeader = " ┌";
    elif uIndex != len(asOutputLines) - 1:
      sIndentationHeader = sMiddleIndentationHeader;
      sMessageHeader = " │";
      # blank out the first 3 columns
      sTime = " " * len(sTime);
      sThreadIdHeader = " " * len(sThreadIdHeader);
      sSourceCodeHeader = " " * len(sSourceCodeHeader);
    else:
      sIndentationHeader = sLastIndentationHeader;
      sMessageHeader = " └";
      # blank out the first 3 columns
      sTime = " " * len(sTime);
      sThreadIdHeader = " " * len(sThreadIdHeader);
      sSourceCodeHeader = " " * len(sSourceCodeHeader);
    uIndex += 1;
    asActualOutput.append("│".join([
      sTime,
      sThreadIdHeader,
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