from .mGlobals import *;

gbShowInternalDebugOutput = False;

def fbIsDebugOutputEnabledForSourceFilePathAndClass(sSourceFilePath, cClass):
  if gbShowInternalDebugOutput:
    print("Show debug output for %s @ %s?" % (cClass, sSourceFilePath), end=' ')
  if gabAllDebugOutputEnabled[0]:
    if gbShowInternalDebugOutput:
      print(" YES! All debug output is enabled.");
    return True;
  for sModuleFilePathHeader in gasModulesWithDebugOutputEnabledFilePathHeaders:
    if sSourceFilePath.startswith(sModuleFilePathHeader):
      if gbShowInternalDebugOutput:
        print(" YES! Location starts with %s." % repr(sModuleFilePathHeader));
      return True;
    if gbShowInternalDebugOutput:
      print(" Location does not start with %s." % repr(sModuleFilePathHeader), end=' ')
  if cClass is None or cClass not in gacClassesWithDebugOutputEnabled:
    if gbShowInternalDebugOutput:
      for cClass in gacClassesWithDebugOutputEnabled:
        print(" Class is not %s." % repr(cClass), end=' ')
      print(" NO.");
    return False;
  if gbShowInternalDebugOutput:
    print(" YES! Class is %s." % repr(cClass));
  return True;
