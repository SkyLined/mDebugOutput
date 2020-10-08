from .mColors import *;

try:
  from mWindowsSDK import HRESULT_FROM_WIN32, mErrorDefines;
except:
  bWindowsSDKAvailable = False;
else:
  bWindowsSDKAvailable = True;

def fdxExceptionDetailsForWindowsError(oException):
  asExceptionDescriptionConsoleOutput = [
    guExceptionInformationColor, "Windows Error ",
    guExceptionInformationHighlightColor, str(oException.winerror), guExceptionInformationColor,
  ];
  if bWindowsSDKAvailable:
    hResult = HRESULT_FROM_WIN32(oException.winerror);
    asExceptionDescriptionConsoleOutput += [
      "/0x",
      guExceptionInformationHighlightColor, "%08X" % (hResult.value,), guExceptionInformationColor
    ];
    for sErrorDefineName in dir(mErrorDefines):
      if getattr(mErrorDefines, sErrorDefineName) == hResult.value:
        asExceptionDescriptionConsoleOutput += [
          " (",
          guExceptionInformationHighlightColor, sErrorDefineName, guExceptionInformationColor,
          ")"
        ];
        break;
    asExceptionDescriptionConsoleOutput += [
      ": ",
      guExceptionInformationHighlightColor, str(oException.strerror), guExceptionInformationColor,
      ".",
    ];
  return {
    "aasConsoleOutputLines": [
      asExceptionDescriptionConsoleOutput,
    ],
    "dxHiddenProperties": {
      "args": (oException.winerror, oException.strerror),
      "errno": oException.errno,
      "filename": None,
      "message": "",
      "strerror": oException.strerror,
      "winerror": oException.winerror,
    },
  };

