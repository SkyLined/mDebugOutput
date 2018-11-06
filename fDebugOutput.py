import threading, time;

try:
  from oConsole import oConsole;
except Exception as oException:
  print repr(Exception);
  oConsole = None;
  goOutputLock = threading.Lock();
else:
  guThreadColor_by_uThreadId = {};
  auThreadColors = [0x0F07, 0x0F0C, 0x0F0E, 0x0F0A, 0x0F0B, 0x0F09, 0x0F0D];

gnStartTime = time.clock();

def fDebugOutput(*asOutputLines):
  uThreadId = threading.currentThread().ident;
  if oConsole:
    oConsole.fLock();
  else:
    goOutputLock.acquire();
  try:
    sHeader =  "%7.3f %8s" % (time.clock() - gnStartTime, uThreadId);
    for sOutputLine in asOutputLines:
      if oConsole:
        uThreadColor = guThreadColor_by_uThreadId.get(uThreadId);
        if uThreadColor is None:
          duCount_by_uThreadColor = dict([(uThreadColor, 0) for uThreadColor in auThreadColors]);
          for uThreadColor in guThreadColor_by_uThreadId.values():
            duCount_by_uThreadColor[uThreadColor] += 1;
          uLowestCount = min([uCount for uCount in duCount_by_uThreadColor.values()]);
          for uThreadColor in auThreadColors:
            if duCount_by_uThreadColor[uThreadColor] == uLowestCount:
              guThreadColor_by_uThreadId[uThreadId] = uThreadColor;
              break;
          else:
            raise AssertionError("Stars are not alligned correctly.");
        oConsole.fPrint(uThreadColor, "%s %s" % (sHeader, sOutputLine));
      else:
        print "%s %s" % (sHeader, sOutputLine);
  finally:
    if oConsole:
      oConsole.fUnlock();
    else:
      goOutputLock.release();
