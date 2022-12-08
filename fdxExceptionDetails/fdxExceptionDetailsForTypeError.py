import re, sys;

def fdxExceptionDetailsForTypeError(oException, oTraceback):
  if len(oException.args) != 1:
    return {};
  oBadKeywordArgumentErrorMessageMatch = re.match(r"^([_\w]+)\(\) got an unexpected keyword argument '([_\w]+)'$", oException.args[0]);
  if oBadKeywordArgumentErrorMessageMatch:
    sFunctionName, sArgumentName = oBadKeywordArgumentErrorMessageMatch.groups();
  else:
    oBadNumberOfArgumentsErrorMessageMatch = re.match(r"^([\_\w]+)\(\) takes (?:at least|at most|exactly) \d+ arguments? \((\d+) given\)$", oException.args[0]);
    if not oBadNumberOfArgumentsErrorMessageMatch:
      return {
        "aasConsoleOutputLines": [
            [guExceptionInformationColor, oException.args[0]],
        ],
        "dxHiddenProperties": {
          "args": oException.args,
          "with_traceback": oException.with_traceback,
          "add_note": oException.add_note,
        },
      };
    sFunctionName, sNumberOfArgumentsGiven = oBadNumberOfArgumentsErrorMessageMatch.groups();
  while oTraceback.tb_next:
    oTraceback = oTraceback.tb_next;
  oPythonFrame = oTraceback.tb_frame;
  oPythonCode = oPythonFrame.f_code;
  # If the function being called is wrapped by ShowDebugOutput, we can
  # output more information about the actual call and the arguments
  # provided:
  sCallDescription = None;
  if oPythonCode == ShowDebugOutput.oFunctionWrapperCode:
    dxLocals = oPythonFrame.f_locals;
    oFunction = dxLocals.get("fxFunction");
    if oFunction and getattr(oFunction, "__name__", None) == sFunctionName:
      sCallDescription = dxLocals.get("sCallDescription", sFunctionName);
      sSourceFilePath = dxLocals.get("sSourceFilePath", "???");
      sLineNumber = str(dxLocals.get("uLineNumber", "???"));
      asCallArguments = dxLocals.get("asCallArguments");
  if sCallDescription is None:
    (afxFunctions, fInstanceMethod, oInstance, cClass) = ftxGetFunctionsMethodInstanceAndClassForPythonCode(oPythonCode);
    if sFunctionName == oPythonCode.co_name:
      sCallDescription = ".".join([s for s in [
        cClass.__name__ if cClass else None,
        oPythonCode.co_name,
      ] if s]);
    else:
      sCallDescription = sFunctionName;
    sSourceFilePath = None;
    asCallArguments = None;
  if oBadKeywordArgumentErrorMessageMatch:
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "A call to ",
        guExceptionInformationHighlightColor, sCallDescription, 
        guExceptionInformationColor, " failed because the code does not have an argument named ",
        guExceptionInformationHighlightColor, sArgumentName,
        guExceptionInformationColor, ".",
      ],
    ];
  else:
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "A call to ",
        guExceptionInformationHighlightColor, sCallDescription, 
        guExceptionInformationColor, " failed because the code does not accept ",
        guExceptionInformationHighlightColor, sNumberOfArgumentsGiven,
        guExceptionInformationColor, " arguments.",
      ],
    ];
  if sSourceFilePath:
    aasConsoleOutputLines += [
      [
      ], [
        guExceptionInformationColor, "This function can be found in the following file:"
      ], [
        guExceptionInformationColor, "  ",
        guExceptionInformationHighlightColor, sSourceFilePath, 
        guExceptionInformationColor, "/",
        guExceptionInformationHighlightColor, sLineNumber, 
      ],
    ];
  if asCallArguments is not None:
    aasConsoleOutputLines += [
      [
      ], [
        guExceptionInformationColor, "Call arguments",
      ]
    ] + [
      [
        guExceptionInformationColor, "  ",
        guExceptionInformationHighlightColor, sCallArgument
      ]
      for sCallArgument in asCallArguments
    ];
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": oException.args,
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
    },
  };

from ..ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;
from ..ShowDebugOutput import ShowDebugOutput;
from ..mColorsAndChars import *;

