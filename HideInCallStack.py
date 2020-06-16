from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;

def HideInCallStack(fxFunction):
  sBadDecorator = {
    classmethod: "@classmethod",
    property: "@property/@.setter/@.deleter",
    staticmethod: "@staticmethod",
  }.get(type(fxFunction));
  if sBadDecorator:
    raise AssertionError("@HideInCallStack must not be followed by %s!" % sBadDecorator);
  gaoHideFunctionsForPythonCodes.add(fxFunction.func_code);
  return fxFunction;
