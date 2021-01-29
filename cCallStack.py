import inspect, os, sys, threading;

from .cFrame import cFrame;
from .fasGetSourceCode import fasGetSourceCode;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fDumpPythonFrame import fDumpPythonFrame;
from .fsGetClassAndFunctionForClassAndCode import fsGetClassAndFunctionForClassAndCode;
from .gaoHideFunctionsForPythonCodes import gaoHideFunctionsForPythonCodes;
from .HideInCallStack import HideInCallStack;

gbDebugDumpRawStacksAndTracebacks = False;

class cCallStack():
  @classmethod
  @HideInCallStack
  def __foFromPythonFramesAndExceptionLineAndCharacterNumbers(cClass, atxPythonFramesAndExceptionLineAndCharacterNumbers, oPythonThread = None):
    oPythonThread = oPythonThread or threading.currentThread();
    return cClass([
      cFrame.foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(oPythonFrame, oPythonThread, u0ExceptionLineNumber, None)
      for (oPythonFrame, u0ExceptionLineNumber, u0ExceptionCharacterNumber) in atxPythonFramesAndExceptionLineAndCharacterNumbers
    ]);
  @classmethod
  @HideInCallStack
  def foFromThisFunction(cClass):
    return cClass.foForCurrentThread();
  @classmethod
  @HideInCallStack
  def foFromThisFunctionsCaller(cClass):
    return cClass.foForCurrentThread(uEndIndex = 1);
  @classmethod
  @HideInCallStack
  def foForCurrentThread(cClass, uStartIndex = None, uEndIndex = None):
    return cClass.foFromPythonFrameAndThread(inspect.currentframe(), threading.currentThread(), uStartIndex, uEndIndex);
  @classmethod
  @HideInCallStack
  def foFromPythonFrameAndThread(cClass, oPythonFrame, oPythonThread, uStartIndex = 0, uEndIndex = 0):
    # Create a list of all PythonFrames on the stack in the current thread.
    aoPythonFrames = [];
    # We are ignoring frames with hidden functions in our indices, so we need to
    # take that into account when determining the end index for this first frame:
    uCurrentEndIndex = -1;
    while oPythonFrame:
      aoPythonFrames.insert(0, oPythonFrame);
      if oPythonFrame.f_code not in gaoHideFunctionsForPythonCodes:
        uCurrentEndIndex += 1;
      oPythonFrame = oPythonFrame.f_back;
    if gbDebugDumpRawStacksAndTracebacks:
      print "--[ cCallStack.foFromPythonFrameAndThread ]".ljust(80, "-");
      if uStartIndex:
        print "uStartIndex: %d" % uStartIndex;
      if uEndIndex:
        print "uEndIndex: %d" % uEndIndex;
    uIndex = 0;
    atxPythonFramesAndExceptionLineAndCharacterNumbers = [];
    for oPythonFrame in aoPythonFrames:
      if oPythonFrame.f_code in gaoHideFunctionsForPythonCodes:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
      else:
        if uStartIndex and uIndex < uStartIndex:
          if gbDebugDumpRawStacksAndTracebacks:
            fDumpPythonFrame(oPythonFrame, "%2d- " % uIndex, "uStartIndex = %d" % uStartIndex);
        elif uEndIndex and uCurrentEndIndex < uEndIndex:
          # Taking into account that calling this function added another frame ------^
          if gbDebugDumpRawStacksAndTracebacks:
            fDumpPythonFrame(oPythonFrame, "%2d- " % uIndex, "uEndIndex = %d" % uCurrentEndIndex);
        else:
          if gbDebugDumpRawStacksAndTracebacks:
            fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex);
          atxPythonFramesAndExceptionLineAndCharacterNumbers.append((oPythonFrame, None, None));
        uIndex += 1;
        uCurrentEndIndex -= 1;
    if gbDebugDumpRawStacksAndTracebacks:
      print "-" * 80;
    return cClass.__foFromPythonFramesAndExceptionLineAndCharacterNumbers(atxPythonFramesAndExceptionLineAndCharacterNumbers, oPythonThread);
  
  @classmethod
  @HideInCallStack
  def faoForAllThreads(cClass, uCurrentThreadEndIndex = 0):
     doPythonThread_by_uThreadId = dict([
      (oPythonThread.ident, oPythonThread)
      for oPythonThread in threading.enumerate()
     ])
     uCurrentThreadId = threading.currentThread().ident;
     return [
       cClass.foFromPythonFrameAndThread(
         oTopPythonFrame,
         doPythonThread_by_uThreadId[uThreadId],
         uEndIndex = None if uThreadId != uCurrentThreadId else uCurrentThreadEndIndex,
       )
       for (uThreadId, oTopPythonFrame) in sys._current_frames().items()
     ];
  
  @classmethod
  def foFromTraceback(cClass, oTraceback, oPythonThread = None):
    assert oTraceback, \
        "A traceback is required!";
    if gbDebugDumpRawStacksAndTracebacks:
      print "--[ cCallStack.foFromTraceback ]".ljust(80, "-");
    atxPythonFramesAndExceptionLineAndCharacterNumbers = [];
    uIndex = 0;
    while oTraceback:
      oPythonFrame = oTraceback.tb_frame;
      if oPythonFrame.f_code in gaoHideFunctionsForPythonCodes:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
      else:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex);
        atxPythonFramesAndExceptionLineAndCharacterNumbers.append((oPythonFrame, oTraceback.tb_lineno, None));
        uIndex += 1;
      oTraceback = oTraceback.tb_next;
    if gbDebugDumpRawStacksAndTracebacks:
      print "-" * 80;
    oStack = cClass.__foFromPythonFramesAndExceptionLineAndCharacterNumbers(atxPythonFramesAndExceptionLineAndCharacterNumbers, oPythonThread);
    return oStack;
  
  @classmethod
  def foFromLastException(cClass):
    return cClass.foFromTraceback(sys.exc_info()[2]);
  
  def __init__(oSelf, aoFrames):
    assert len(aoFrames) > 0, \
        "A stack must have at least one frame!";
    oSelf.aoFrames = aoFrames; # frame 0 is the top frame.
    
    for uIndex in xrange(len(oSelf.aoFrames)):
      oFrame = oSelf.aoFrames[uIndex];
      oFrame.oStack = oSelf;
      oFrame.uIndex = uIndex;
      oFrame.oParentFrame = oSelf.aoFrames[uIndex - 1] if uIndex > 0 else None;
      oFrame.oChildFrame = oSelf.aoFrames[uIndex + 1] if uIndex < len(oSelf.aoFrames) - 1 else None;
  
  @property
  def uThreadId(oSelf):
    return oSelf.aoFrames[0].uThreadId;
  
  @property
  def sThreadName(oSelf):
    return oSelf.aoFrames[0].sThreadName;
  
  @property
  def oTopFrame(oSelf):
    return oSelf.aoFrames[-1];
  
  def faasCreateConsoleOutput(oSelf, *txArguments, **dxArguments):
    return faasCreateConsoleOutputForStack(oSelf, *txArguments, **dxArguments);
  
  def fsToString(oSelf):
    return "<%s#%X thread = %d/0x%X (%s), %d frames @ %s>" % (
      oSelf.__class__.__name__, id(oSelf),
      oSelf.uThreadId, oSelf.uThreadId, oSelf.sThreadName,
      len(oSelf.aoFrames),
      oSelf.aoFrames[-1].sCallDescription
    );
