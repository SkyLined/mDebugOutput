import threading;

from .dxConfig import dxConfig;
from .fDumpPythonFrame import fDumpPythonFrame;

oOutputLock = threading.RLock();

def fDumpTraceback(oTraceback, sPrefix = "", bExpand = True):
  oOutputLock.acquire();
  try:
    uIndex = 0;
    if bExpand:
      print("--[ Traceback ]".ljust(80, "-"));
    while oTraceback:
      uIndex += 1;
      if oTraceback.tb_frame:
        print("%sTB#%d %s @ %s%s%d" % (
          sPrefix, uIndex,
          oTraceback.tb_frame.f_code.co_name,
          oTraceback.tb_frame.f_code.co_filename,
          dxConfig["sLineNumberAfterPathPrefix"],
          oTraceback.tb_lineno
        ));
        fDumpPythonFrame(oTraceback.tb_frame, sPrefix = sPrefix + "  ", bExpand = bExpand);
      else:
        print("%sTB#%d ???/%d" % (sPrefix, oTraceback.tb_lineno));
      if not bExpand:
        return;
      oTraceback = oTraceback.tb_next;
    print("-" * 80);
  finally:
    oOutputLock.release();