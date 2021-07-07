import re;

from ..mColors import *;

def fdxExceptionDetailsForAttributeError(oException):
  if len(oException.args) != 1:
    return {};
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
  return {
    "aasConsoleOutputLines": [
      [
        guExceptionInformationHighlightColor, sObjectName,
        guExceptionInformationColor, " ", sObjectType, " has no attribute ",
        guExceptionInformationHighlightColor, sAttributeName,
        guExceptionInformationColor, ":"
      ],
    ],
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
    },
  };
