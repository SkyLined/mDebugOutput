import threading;

from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;

oOutputLock = threading.RLock();

def fDumpPythonFrame(oPythonFrame, sPrefix = "", sSuffix = "", bExpand = True):
  oOutputLock.acquire();
  try:
    uIndex = 0;
    if bExpand:
      print(("%s--[ Stack frames ]" % sPrefix).ljust(80, "-"));
    while oPythonFrame:
      uIndex += 1;
      print("%sF#%d%s %s @ %s/%d%s" % (
        sPrefix, uIndex, "*" if oPythonFrame.f_code in gaoHideFunctionsForPythonCodes else " ",
        oPythonFrame.f_code.co_name,
        oPythonFrame.f_code.co_filename, oPythonFrame.f_lineno,
        " (%s)" % sSuffix if sSuffix else ""
      ));
      if not bExpand:
        return;
      oPythonFrame = oPythonFrame.f_back;
    print(sPrefix.ljust(80, "-"));
  finally:
    oOutputLock.release();