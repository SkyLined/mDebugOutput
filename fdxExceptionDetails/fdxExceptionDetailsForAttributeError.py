import re;

def fdxExceptionDetailsForAttributeError(oException):
  if len(oException.args) != 1:
    return {};
  dxHiddenProperties = {
    "args": oException.args,
    "with_traceback": oException.with_traceback,
    "add_note": oException.add_note,
    "name": oException.name,
    "obj": oException.obj,
  };
  oClassErrorMessageMatch = re.match(r"^type object '(\w+)' has no attribute '(\w+)'$", oException.args[0]);
  if oClassErrorMessageMatch:
    (sObjectName, sAttributeName) = oClassErrorMessageMatch.groups();
    sObjectType = "class";
  else:
    oInstanceErrorMessageMatch = re.match(r"^'(\w+)' object has no attribute '(\w+)'$", oException.args[0]);
    if oInstanceErrorMessageMatch:
      (sObjectName, sAttributeName) = oInstanceErrorMessageMatch.groups();
      sObjectType = "instance";
    else:
      oModuleErrorMessageMatch = re.match(r"^module '(\w+)' has no attribute '(\w+)'$", oException.args[0]);
      if not oModuleErrorMessageMatch:
        return {};
      (sObjectName, sAttributeName) = oModuleErrorMessageMatch.groups();
      sObjectType = "module";
  try:
    sException = repr(oException.obj);
  except:
    sException = "".join([
      "<",
      oException.__class__.__module__,
      ".",
      oException.__class__.__name__,
      " ",
      "<details not available>"
    ]);
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationHighlightColor, sObjectName,
        guExceptionInformationColor, " ", sObjectType, " has no attribute ",
        guExceptionInformationHighlightColor, sAttributeName,
        guExceptionInformationColor, "."
      ], [
        guExceptionInformationHighlightColor, sObjectType, ": ",
        guExceptionInformationHighlightColor, sException,
        guExceptionInformationColor, "."
      ],
    ],
    "dxHiddenProperties": dxHiddenProperties,
  };

from ..mColorsAndChars import *;

