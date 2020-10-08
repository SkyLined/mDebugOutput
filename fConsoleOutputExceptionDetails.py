import re, sys, threading;

from .HideInCallStack import HideInCallStack;

guMaxNumberOfLocalVariablesToShow = 40;

@HideInCallStack
def fConsoleOutputExceptionDetails(oException, o0Traceback = None, o0PythonThread = None, aasAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  if o0Traceback:
    oTraceback = o0Traceback;
  else:
    oTraceback = sys.exc_info()[2];
  if oTraceback.tb_frame.f_code in gaoHideFunctionsForPythonCodes:
    # Not sure why I am added this code but I believe it may be a special handler for internal errors.
    import os, traceback
    traceback.print_exception(oException.__class__, oException, oTraceback);
    os._exit(3);
  oStack = cCallStack.foFromTraceback(oTraceback, o0PythonThread);
    
  sBoxTitle = "Fatal %s.%s Exception" % (oException.__class__.__module__, oException.__class__.__name__);
  if isinstance(oException, AssertionError):
    dxExceptionDetails = fdxExceptionDetailsForAssertionError(oException);
  elif isinstance(oException, AttributeError):
    dxExceptionDetails = fdxExceptionDetailsForAttributeError(oException);
  elif isinstance(oException, ImportError):
    dxExceptionDetails = fdxExceptionDetailsForImportError(oException);
  elif isinstance(oException, NameError):
    dxExceptionDetails = fdxExceptionDetailsForNameError(oException);
  elif isinstance(oException, SyntaxError):
    dxExceptionDetails = fdxExceptionDetailsForSyntaxError(oException);
  elif isinstance(oException, TypeError):
    dxExceptionDetails = fdxExceptionDetailsForTypeError(oException, oTraceback);
  elif isinstance(oException, UnboundLocalError):
    dxExceptionDetails = fdxExceptionDetailsForUnboundLocalError(oException);
  elif isinstance(oException, UnicodeDecodeError):
    dxExceptionDetails = fdxExceptionDetailsForUnicodeDecodeError(oException);
  elif isinstance(oException, WindowsError):
    dxExceptionDetails = fdxExceptionDetailsForWindowsError(oException);
  else:
    dxExceptionDetails = {};
  aasConsoleOutputLines = dxExceptionDetails.get("aasConsoleOutputLines", None);
  dxHiddenProperties = dxExceptionDetails.get("dxHiddenProperties", {});
  bShowLocals = dxExceptionDetails.get("bShowLocals", True);

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
  fConsoleOutput(sBoxTitle, aasConsoleOutputLines);
  
from .cCallStack import cCallStack;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fdxExceptionDetailsForAssertionError import fdxExceptionDetailsForAssertionError;
from .fdxExceptionDetailsForAttributeError import fdxExceptionDetailsForAttributeError;
from .fdxExceptionDetailsForImportError import fdxExceptionDetailsForImportError;
from .fdxExceptionDetailsForNameError import fdxExceptionDetailsForNameError;
from .fdxExceptionDetailsForSyntaxError import fdxExceptionDetailsForSyntaxError;
from .fdxExceptionDetailsForTypeError import fdxExceptionDetailsForTypeError;
from .fdxExceptionDetailsForUnboundLocalError import fdxExceptionDetailsForUnboundLocalError;
from .fdxExceptionDetailsForUnicodeDecodeError import fdxExceptionDetailsForUnicodeDecodeError;
from .fdxExceptionDetailsForWindowsError import fdxExceptionDetailsForWindowsError;
from .fConsoleOutput import fConsoleOutput;
from .fsToString import fsToString;
from .fTerminateWithConsoleOutput import fTerminateWithConsoleOutput;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .mColors import *;
from .ShowDebugOutput import ShowDebugOutput;

