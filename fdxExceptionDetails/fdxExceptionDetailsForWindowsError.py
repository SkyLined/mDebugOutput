try:
  from mWindowsSDK import *;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mWindowsSDK'":
    raise;
  bWindowsSDKAvailable = False;
else:
  bWindowsSDKAvailable = True;

def fdxExceptionDetailsForWindowsError(oException):
  u0Win32ErrorNumber = oException.errno;
  asWin32ErrorDescriptionConsoleOutputLines = [
    guExceptionInformationColor, "Windows Error ",
    guExceptionInformationHighlightColor, str(u0Win32ErrorNumber), 
  ];
  aasConsoleOutputLines = [
    asWin32ErrorDescriptionConsoleOutputLines
  ];
  if u0Win32ErrorNumber is not None:
    if u0Win32ErrorNumber > 10:
      asWin32ErrorDescriptionConsoleOutputLines += [
        guExceptionInformationColor, " / ", guExceptionInformationHighlightColor, "0x%X" % u0Win32ErrorNumber, 
      ];
    if bWindowsSDKAvailable:
      s0Win32ErrorDefineName = fs0GetWin32ErrorCodeDefineName(u0Win32ErrorNumber);
      if s0Win32ErrorDefineName:
        asWin32ErrorDescriptionConsoleOutputLines += [
          guExceptionInformationColor, " (", guExceptionInformationHighlightColor, s0Win32ErrorDefineName, guExceptionInformationColor, ")",
        ];
  aasConsoleOutputLines.append([
    guExceptionInformationColor, "Error description: \"",
    guExceptionInformationHighlightColor, str(oException.strerror), guExceptionInformationColor, "\".",
  ]);
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": (oException.errno, oException.strerror) if oException.winerror is None else (oException.errno, oException.strerror, None, oException.winerror, None),
      "with_traceback": oException.with_traceback,
      "errno": oException.errno if oException.winerror is None else oException.winerror,
      "filename": None,
      "filename2": None,
      "strerror": oException.strerror,
      "winerror": oException.winerror,
    },
  };

from ..mColorsAndChars import *;

