import inspect, sys, threading;

from .cFrame import cFrame;
from .faasCreateConsoleOutputForStack import faasCreateConsoleOutputForStack;
from .fDumpPythonFrame import fDumpPythonFrame;

gbDebugDumpRawStacksAndTracebacks = False;

class cCallStack():
  # NOTE: functions that have a local variable named `mDebugOutput_HideInCallStack` will be excluded from the stack!
  # This can be used by utility functions that make it easy to perform an operation that would normally be done inline.
  # For instance, a function "B" that is called for each argument passed to a function "A" in order to check if the
  # argument is of the correct type and which throws an exception if it is not: this exception makes more sense if it
  # was thrown function function "A", so function "B" should define this local variable to hide it in the stack.
  @classmethod
  def __foFromPythonFramesAndExceptionLineAndCharacterNumbers(cClass, atxPythonFramesAndExceptionLineAndCharacterNumbers, o0PythonThread = None):
    if o0PythonThread is None:
      try: # This can fail during shutdown, so we catch any exceptions and ignore them.
        o0PythonThread = threading.current_thread();
      except:
        pass;
    return cClass(
      [
        cFrame.foFromPythonFrameThreadAndExceptionLineAndCharacterNumber(oPythonFrame, o0PythonThread, u0ExceptionLineNumber, None)
        for (oPythonFrame, u0ExceptionLineNumber, u0ExceptionCharacterNumber) in atxPythonFramesAndExceptionLineAndCharacterNumbers
      ],
      o0PythonThread.ident if o0PythonThread else None,
      o0PythonThread.name if o0PythonThread else None,
    );
  @classmethod
  def foForThisFunction(cClass):
    return cClass.foForCurrentThread();
  @classmethod
  def foForThisFunctionsCaller(cClass):
    return cClass.foForCurrentThread(uEndIndex = 2);
  @classmethod
  def foForCurrentThread(cClass, uStartIndex = None, uEndIndex = None):
    return cClass.foFromPythonFrameAndThread(inspect.currentframe(), threading.current_thread(), uStartIndex, uEndIndex);
  @classmethod
  def foFromPythonFrameAndThread(cClass, oPythonFrame, o0PythonThread, uStartIndex = 0, uEndIndex = 0):
    # Create a list of all PythonFrames on the stack in the current thread.
    aoPythonFrames = [];
    # We are ignoring frames with hidden functions in our indices, so we need to
    # take that into account when determining the end index for this first frame:
    uCurrentEndIndex = -1;
    while oPythonFrame:
      aoPythonFrames.insert(0, oPythonFrame);
      if "mDebugOutput_HideInCallStack" not in oPythonFrame.f_code.co_varnames:
        uCurrentEndIndex += 1;
      oPythonFrame = oPythonFrame.f_back;
    if gbDebugDumpRawStacksAndTracebacks:
      print("--[ cCallStack.foFromPythonFrameAndThread ]".ljust(80, "-"));
      if uStartIndex:
        print("uStartIndex: %d" % uStartIndex);
      if uEndIndex:
        print("uEndIndex: %d" % uEndIndex);
    uIndex = 0;
    atxPythonFramesAndExceptionLineAndCharacterNumbers = [];
    for oPythonFrame in aoPythonFrames:
      if "mDebugOutput_HideInCallStack" in oPythonFrame.f_code.co_varnames:
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
      print("-" * 80);
    return cClass.__foFromPythonFramesAndExceptionLineAndCharacterNumbers(
      atxPythonFramesAndExceptionLineAndCharacterNumbers,
      o0PythonThread,
    );
  
  @classmethod
  def faoForAllThreads(cClass, uCurrentThreadEndIndex = 0):
     doPythonThread_by_uThreadId = dict([
      (oPythonThread.ident, oPythonThread)
      for oPythonThread in threading.enumerate()
     ])
     uCurrentThreadId = threading.current_thread().ident;
     return [
       cClass.foFromPythonFrameAndThread(
         oTopPythonFrame,
         doPythonThread_by_uThreadId[uThreadId],
         uEndIndex = None if uThreadId != uCurrentThreadId else uCurrentThreadEndIndex,
       )
       for (uThreadId, oTopPythonFrame) in sys._current_frames().items()
     ];
  
  @classmethod
  def foFromTraceback(cClass, oTraceback, o0PythonThread = None):
    assert oTraceback, \
        "A traceback is required!";
    if gbDebugDumpRawStacksAndTracebacks:
      print("--[ cCallStack.foFromTraceback ]".ljust(80, "-"));
    atxPythonFramesAndExceptionLineAndCharacterNumbers = [];
    uIndex = 0;
    while oTraceback:
      oPythonFrame = oTraceback.tb_frame;
      if "mDebugOutput_HideInCallStack" in oPythonFrame.f_code.co_varnames:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "  - ", "Hidden code");
      else:
        if gbDebugDumpRawStacksAndTracebacks:
          fDumpPythonFrame(oPythonFrame, "%2d+ " % uIndex);
        atxPythonFramesAndExceptionLineAndCharacterNumbers.append((oPythonFrame, oTraceback.tb_lineno, None));
        uIndex += 1;
      oTraceback = oTraceback.tb_next;
    if gbDebugDumpRawStacksAndTracebacks:
      print("-" * 80);
    oStack = cClass.__foFromPythonFramesAndExceptionLineAndCharacterNumbers(
      atxPythonFramesAndExceptionLineAndCharacterNumbers,
      o0PythonThread,
    );
    return oStack;
  
  def __init__(oSelf, aoFrames, u0ThreadId, s0ThreadName):
# Since frames can be hidden, there may be 0 in the stack
#    assert len(aoFrames) > 0, \
#        "A stack must have at least one frame!";
    oSelf.aoFrames = aoFrames; # frame 0 is the top frame.
    oSelf.u0ThreadId = u0ThreadId;
    oSelf.s0ThreadName = s0ThreadName;
    
    for uIndex in range(len(oSelf.aoFrames)):
      oFrame = oSelf.aoFrames[uIndex];
      oFrame.oStack = oSelf;
      oFrame.uIndex = uIndex;
      oFrame.oParentFrame = oSelf.aoFrames[uIndex - 1] if uIndex > 0 else None;
      oFrame.oChildFrame = oSelf.aoFrames[uIndex + 1] if uIndex < len(oSelf.aoFrames) - 1 else None;
  
  @property
  def o0TopFrame(oSelf):
    return oSelf.aoFrames[-1] if oSelf.aoFrames else None;
  
  def faasCreateConsoleOutput(oSelf, *txArguments, **dxArguments):
    return faasCreateConsoleOutputForStack(oSelf, *txArguments, **dxArguments);
  
  def fsToString(oSelf):
    return "<%s#%X thread %s, %d frames @ %s>" % (
      oSelf.__class__.__name__, id(oSelf),
      "%d/0x%X (%s)" % (oSelf.u0ThreadId, oSelf.u0ThreadId, oSelf.s0ThreadName) if oSelf.u0ThreadId is not None else "unknown",
      len(oSelf.aoFrames),
      oSelf.aoFrames[-1].sCallDescription
    );
