import inspect, os, re, threading;

from .HideInCallStack import HideInCallStack;

@HideInCallStack
def fTerminateWithException(oException, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False):
  fConsoleOutputExceptionDetails(oException, a0asAdditionalConsoleOutputLines = None, bShowStacksForAllThread = False)
  os._exit(3);

from .cCallStack import cCallStack;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fConsoleOutputExceptionDetails import fConsoleOutputExceptionDetails;
from .fsToString import fsToString;
from .fTerminateWithConsoleOutput import fTerminateWithConsoleOutput;
from .ftxGetFunctionsMethodInstanceAndClassForPythonCode import ftxGetFunctionsMethodInstanceAndClassForPythonCode;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .mColors import *;
