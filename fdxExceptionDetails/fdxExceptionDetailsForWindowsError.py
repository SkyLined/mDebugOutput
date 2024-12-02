try:
  import mWindowsSDK;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mWindowsSDK'":
    raise;
  bWindowsSDKSupportEnabled = False;
else:
  bWindowsSDKSupportEnabled = True;

def fdxExceptionDetailsForWindowsError(oException):
  if oException.winerror is None:
    aasConsoleOutputLines = [
      [
        guExceptionInformationHighlightColor, str(oException.strerror),
        guExceptionInformationColor, ".",
      ], [
        guExceptionInformationColor, "Error number ",
        guExceptionInformationHighlightColor, str(oException.errno), 
        [
          guExceptionInformationColor, " / ",
          guExceptionInformationHighlightColor, "0x%X" % oException.errno, 
        ] if oException.errno is not None and oException.errno > 10 else [],
        guExceptionInformationColor, ".",
      ],
    ];
  else:
    s0Win32ErrorDefineName = mWindowsSDK.fs0GetWin32ErrorCodeDefineName(oException.winerror) \
        if bWindowsSDKSupportEnabled else None;
    aasConsoleOutputLines = [
      [
        guExceptionInformationHighlightColor, str(oException.strerror),
        guExceptionInformationColor, ".",
      ], [
        guExceptionInformationColor, "Error number ",
        guExceptionInformationHighlightColor, str(oException.winerror), 
        [
          guExceptionInformationColor, " / ",
          guExceptionInformationHighlightColor, "0x%X" % oException.winerror, 
        ] if oException.winerror > 10 else [],
        [
          guExceptionInformationColor, " (",
          guExceptionInformationHighlightColor, s0Win32ErrorDefineName,
          guExceptionInformationColor, ")",
        ] if s0Win32ErrorDefineName else [],
        [ 
          guExceptionInformationColor, ", additional error code: ",
          guExceptionInformationHighlightColor, str(oException.errno), 
          [
            guExceptionInformationColor, " / ",
            guExceptionInformationHighlightColor, "0x%X" % oException.errno, 
          ] if oException.errno > 10 else [],
        ] if oException.errno != oException.winerror else [],
      ],
    ];
  if oException.filename is not None:
    aasConsoleOutputLines.append([
      guExceptionInformationColor, "File name: \"",
      guExceptionInformationHighlightColor, str(oException.filename), guExceptionInformationColor, "\".",
    ]);
  if oException.filename2 is not None:
    aasConsoleOutputLines.append([
      guExceptionInformationColor, "Second file name: \"",
      guExceptionInformationHighlightColor, str(oException.filename2), guExceptionInformationColor, "\".",
    ]);
    
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": (
        (oException.errno, oException.strerror) if len(oException.args) == 2 else
        (oException.errno, oException.strerror, None, oException.winerror, None)
      ),
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
      "errno": oException.errno,
      "filename": oException.filename,
      "filename2": oException.filename2,
      "strerror": oException.strerror,
      "winerror": oException.winerror,
    },
  };

from ..mColorsAndChars import *;

