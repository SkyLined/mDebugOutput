
def fsToString(xData, uMaxLength = None):
  if isinstance(xData, cWithDebugOutput):
    sData = xData.fsToString();
    assert isinstance(sData, str), \
        "%s.fsToString() returns %s" % (repr(xData), repr(sData));
  elif isinstance(xData, tuple):
    sData = "(%s)" % ", ".join([fsToString(xComponent, uMaxLength and uMaxLength >> 1) for xComponent in xData]);
  elif isinstance(xData, list):
    sData = "[%s]" % ", ".join([fsToString(xComponent, uMaxLength and uMaxLength >> 1) for xComponent in xData]);
  else:
    sData = repr(xData);
  if uMaxLength is not None and len(sData) > uMaxLength:
    sData = sData[:uMaxLength - 6] + "\xFA\xFA\xFA" + sData[-3:];
  return sData;

from .cWithDebugOutput import cWithDebugOutput;
