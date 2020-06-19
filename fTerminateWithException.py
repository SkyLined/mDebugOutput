import inspect, os, re, threading;

from .HideInCallStack import HideInCallStack;
from .cCallStack import cCallStack;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fsToString import fsToString;
from .fTerminateWithConsoleOutput import fTerminateWithConsoleOutput;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .mColors import *;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;

from oConsole import oConsole;
guMaxNumberOfLocalVariablesToShow = 40;

@HideInCallStack
def fTerminateWithException(oException, aasAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  import sys;
  if sys.exc_info()[2].tb_frame.f_code in gaoHideFunctionsForPythonCodes:
    import traceback
    traceback.print_exc();
    sys.exit(1);
  oStack = cCallStack.foFromLastException();
    
  sBoxTitle = "Fatal %s.%s Exception" % (oException.__class__.__module__, oException.__class__.__name__);
  aasConsoleOutputLines = None;
  bShowLocals = True;
  if isinstance(oException, SyntaxError):
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "Syntax error in ", guExceptionInformationHighlightColor, str(oException.filename),
        guExceptionInformationColor, " on line ", guExceptionInformationHighlightColor, str(oException.lineno),
        guExceptionInformationColor, ", column ", guExceptionInformationHighlightColor, str(oException.offset),
        guExceptionInformationColor, ".",
      ],
    ];
    dxHiddenProperties = {
      "args": ('invalid syntax', (oException.filename, oException.lineno, oException.offset, oException.text)),
      "filename": oException.filename,
      "lineno": oException.lineno,
      "message": '',
      "msg": 'invalid syntax',
      "offset": oException.offset,
      "print_file_and_line": None,
      "text": oException.text,
    };
    bShowLocals = False;
  elif isinstance(oException, AttributeError):
    oErrorMessageMatch = re.match(r"^'(\w+)' object has no attribute '(\w+)'$", oException.message);
    if oErrorMessageMatch:
      aasConsoleOutputLines = [
        [
          guExceptionInformationHighlightColor, oErrorMessageMatch.group(1),
          guExceptionInformationColor, " instance has no attribute ",
          guExceptionInformationHighlightColor, oErrorMessageMatch.group(2),
          guExceptionInformationColor, ":"
        ],
      ];
      dxHiddenProperties = {
        "message": oException.message,
        "args": (oException.message,),
      }; 
  elif isinstance(oException, AssertionError):
    aasConsoleOutputLines = [
      [
        guExceptionInformationHighlightColor, oException.message,
      ],
    ];
    dxHiddenProperties = {
      "message": oException.message,
      "args": (oException.message,),
    };
  elif isinstance(oException, ImportError):
    oErrorMessageMatch = re.match(r"^cannot import name (\w+)$", oException.message);
    if oErrorMessageMatch:
      aasConsoleOutputLines = [
        [
          guExceptionInformationColor, "An import failed because the module does not have a member named ",
          guExceptionInformationHighlightColor, oErrorMessageMatch.group(1),
          guExceptionInformationColor, ".",
        ],
      ];
      dxHiddenProperties = {
        "message": oException.message,
        "args": (oException.message,),
      }; 
    bShowLocals = False;
  elif isinstance(oException, TypeError):
    oBadKeywordArgumentErrorMessageMatch = re.match(r"^([_\w]+)\(\) got an unexpected keyword argument '([_\w]+)'$", oException.message);
    oBadNumberOfArgumentsErrorMessageMatch = re.match(r"^([\_\w]+)\(\) takes (?:at least|at most|exactly) \d+ arguments? \((\d+) given\)$", oException.message);
    if oBadKeywordArgumentErrorMessageMatch or oBadNumberOfArgumentsErrorMessageMatch:
      if oBadKeywordArgumentErrorMessageMatch:
        sFunctionName, sArgumentName = oBadKeywordArgumentErrorMessageMatch.groups();
      else:
        sFunctionName, sNumberOfArgumentsGiven = oBadNumberOfArgumentsErrorMessageMatch.groups();
      oTraceback = sys.exc_info()[2];
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
        sCallDescription = ".".join([s for s in [
          cClass.__name__ if cClass else None,
          oPythonCode.co_name,
        ] if s]);
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
      dxHiddenProperties = {
        "message": oException.message,
        "args": (oException.message,),
      }; 
  elif isinstance(oException, NameError):
    oUnknownVariableErrorMessageMatch = re.match(r"^(?:global )?name '([_\w]+)' is not defined$", oException.message);
    if oUnknownVariableErrorMessageMatch:
      sVariableName = oUnknownVariableErrorMessageMatch.group(1);
      aasConsoleOutputLines = [
        [
          guExceptionInformationColor, "Undefined variable ",
          guExceptionInformationHighlightColor, sVariableName, 
          guExceptionInformationColor, ".",
        ],
      ];
      dxHiddenProperties = {
        "message": oException.message,
        "args": (oException.message,),
      }; 
  elif isinstance(oException, UnboundLocalError):
    oUninitializedVariableErrorMessageMatch = re.match(r"^local variable '([_\w]+)' referenced before assignment$", oException.message);
    if oUninitializedVariableErrorMessageMatch:
      sVariableName = oUninitializedVariableErrorMessageMatch.group(1);
      aasConsoleOutputLines = [
        [
          guExceptionInformationColor, "Use of uninitialized variable ",
          guExceptionInformationHighlightColor, sVariableName, 
          guExceptionInformationColor, ".",
        ],
      ];
      dxHiddenProperties = {
        "message": oException.message,
        "args": (oException.message,),
      }; 
  elif isinstance(oException, UnicodeDecodeError):
    sInputString = oException.object;
    sOffensiveChars = sInputString[oException.start: oException.end];
    bInputIsUnicode = isinstance(sInputString, unicode);
    aasConsoleOutputLines = [
      [
        guExceptionInformationColor, "Cannot decode characters in string at offset ",
        guExceptionInformationHighlightColor, str(oException.start),
        guExceptionInformationColor, " because ",
        guExceptionInformationHighlightColor, fsToString(oException.reason),
        guExceptionInformationColor, ".",
      ], [
        guExceptionInformationColor, "The offensive character", " is" if len(sOffensiveChars) == 1 else "s are", ":",
      ], [
        guExceptionInformationHighlightColor, "  ", fsToString(sOffensiveChars),
      ], [
        guExceptionInformationColor, "  (Hex: ",
        guExceptionInformationHighlightColor, " ".join([
          ("%04X" if bInputIsUnicode else "%02X") % ord(sChar)
          for sChar in sOffensiveChars
        ]),
        guExceptionInformationColor, ")",
      ], [
        guExceptionInformationColor, "The input string was:",
      ],
    ];
    # Put a caret under the location of the error.
    sHumanReadbleInputString = fsToString(sInputString, uMaxLength = 200);
    sHumanReadbleInputStringUpToOffensiveCharacters = fsToString(sInputString[:oException.start], uMaxLength = 200)[:-1];
    if len(sHumanReadbleInputStringUpToOffensiveCharacters) < 1000:
      sHumanReadbleOffensiveCharacters = fsToString(sOffensiveChars, uMaxLength = 200)[1:-1];
      sHumanReadbleInputStringAfterOffensiveCharacters = fsToString(sInputString[oException.end:], uMaxLength = 200)[1:];
      # Show input string with offensive characters highlighted.
      aasConsoleOutputLines.append(
        [
          guExceptionInformationColor, "  ", sHumanReadbleInputStringUpToOffensiveCharacters,
          guExceptionInformationErrorColor, sHumanReadbleOffensiveCharacters,
          guExceptionInformationColor, sHumanReadbleInputStringAfterOffensiveCharacters,
        ],
      );
    else:
      # String is too large to show additional useful information:
      aasConsoleOutputLines.append(
        [
          guExceptionInformationColor, "  ", fsToString(sInputString, 1000),
       ],
      );
    
    dxHiddenProperties = {
      "args": (oException.encoding, oException.object, oException.start, oException.end, oException.reason),
      "encoding": oException.encoding,
      "end": oException.end,
      "message": "",
      "object": oException.object,
      "reason": oException.reason,
      "start": oException.start,
    };
  if not aasConsoleOutputLines:
    aasConsoleOutputLines = [
      [guExceptionInformationColor, "Exception attributes:"],
    ] + [
      [
        guExceptionInformationHighlightColor, str(sName),
        guExceptionInformationColor, " = ", 
        guExceptionInformationHighlightColor, fsToString(getattr(oException, sName))
      ]
      for sName in dir(oException)
      if sName[0] != "_"
    ];
  else:
    bAdditionalAttributes = False;
    for sName in sorted(dir(oException)):
      if sName[0] == "_":
        continue;
      xValue = getattr(oException, sName);
      if sName in dxHiddenProperties and dxHiddenProperties[sName] == xValue:
        continue;
      if not bAdditionalAttributes:
        aasConsoleOutputLines += [
          [guExceptionInformationColor, "Additional exception attributes:"],
        ];
        bAdditionalAttributes = True;
      aasConsoleOutputLines += [
        [
          guExceptionInformationHighlightColor, str(sName),
          guExceptionInformationColor, " = ", 
          guExceptionInformationHighlightColor, fsToString(xValue),
        ] + ([
          guExceptionInformationColor, " (expected ", 
          guExceptionInformationHighlightColor, fsToString(dxHiddenProperties[sName]),
          guExceptionInformationColor, ")", 
        ] if (sName in dxHiddenProperties) else [])
      ];
  
  if bShowLocals:
    aasConsoleOutputLines += [
      [],
      [guExceptionInformationColor, "Local variables:"],
    ]
    asLocalVariableNames = sorted(oStack.oTopFrame.dxLocalVariables.keys(), key = str.lower);
    if len(asLocalVariableNames) > guMaxNumberOfLocalVariablesToShow:
      # Try to filter out constants by removing all variables whose names is IN_ALL_CAPS:
      asLocalVariableNames = [sLocalVariableName for sLocalVariableName in asLocalVariableNames if sLocalVariableName.upper() != sLocalVariableName];
    bTooManyLocalVariables = len(asLocalVariableNames) > guMaxNumberOfLocalVariablesToShow;
    for sName in asLocalVariableNames[:guMaxNumberOfLocalVariablesToShow]:
      xValue = oStack.oTopFrame.dxLocalVariables[sName];
      aasConsoleOutputLines += [
        ["  ", guExceptionInformationHighlightColor, sName, guExceptionInformationColor, " = ", fsToString(xValue)],
      ];
    if bTooManyLocalVariables:
      aasConsoleOutputLines += [
        [
          guExceptionInformationColor, "  (... ", 
          guExceptionInformationHighlightColor, str(len(asLocalVariableNames) - guMaxNumberOfLocalVariablesToShow),
          guExceptionInformationColor, " variables not shown...)",
        ],
      ];
  if aasAdditionalConsoleOutputLines is not None:
    aasConsoleOutputLines += [
      [],
    ];
    aasConsoleOutputLines += aasAdditionalConsoleOutputLines;
  
  aasConsoleOutputLines += [
    [],
  ];
  aasConsoleOutputLines += faasCreateConsoleOutputForStack(oStack, oException);
  if bShowStacksForAllThread:
    oPythonThread = threading.currentThread();
    doStack_by_uThreadId = dict([
      (oStack.uThreadId, oStack)
      for oStack in cCallStack.faoForAllThreads()
    ]);
    if len(doStack_by_uThreadId) != 1:
      aasConsoleOutputLines += [
        [],
        [guExceptionInformationColor, "The following additional threads were running:"],
        [],
      ]
      for uThreadId in sorted(doStack_by_uThreadId.keys()):
        if uThreadId != oPythonThread.ident:
          aasConsoleOutputLines += faasCreateConsoleOutputForStack(doStack_by_uThreadId[uThreadId]);
  fTerminateWithConsoleOutput(sBoxTitle, aasConsoleOutputLines);
  
from ShowDebugOutput import ShowDebugOutput;

