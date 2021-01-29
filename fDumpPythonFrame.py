from .fDumpTraceback import fDumpTraceback;

def fDumpPythonFrame(oPythonFrame, sPrefix = "", sSuffix = "", bExpand = True):
  sFlags = " ".join([s for s in [
    repr(oPythonFrame.f_exc_type) if oPythonFrame.f_exc_type else None,
    repr(oPythonFrame.f_exc_value) if oPythonFrame.f_exc_value else None,
  ] if s]);
  print "%s%s @ %s/%d%s" % (
    sPrefix, oPythonFrame.f_code.co_name,
    oPythonFrame.f_code.co_filename, oPythonFrame.f_lineno,
    " (%s)" % sSuffix if sSuffix else ""
  );
  sPrefix = " " * len(sPrefix);
  if bExpand:
    if oPythonFrame.f_back:
      fDumpPythonFrame(oPythonFrame.f_back, sPrefix + "  <-", bExpand = False);
    if oPythonFrame.f_exc_type is not None or oPythonFrame.f_exc_value is not None:
      print "%s  E>%s: %s" % (sPrefix, repr(oPythonFrame.f_exc_type), repr(oPythonFrame.f_exc_value));
    if oPythonFrame.f_exc_traceback is not None:
      fDumpTraceback(oPythonFrame.f_exc_traceback, sPrefix + "  T>", bExpand = False);
