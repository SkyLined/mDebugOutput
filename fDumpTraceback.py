def fDumpTraceback(oTraceback, sPrefix = "", bExpand = True):
  if oTraceback.tb_frame:
    print "%s%s @ %s/%d" % (sPrefix, oTraceback.tb_frame.f_code.co_name, oTraceback.tb_frame.f_code.co_filename, oTraceback.tb_lineno);
  else:
    print "%s???/%d" % (sPrefix, oTraceback.tb_lineno);
  if oTraceback.tb_next:
    fDumpTraceback(oTraceback.tb_next, sPrefix, bExpand = True);
