from .mGlobals import *;

gbShowInternalDebugOutput = False;

def fbIsDebugOutputEnabledForSourceFilePathAndClass(sSourceFilePath, cClass):
  if gbShowInternalDebugOutput:
    print "Show debug output for %s @ %s?" % (cClass, sSourceFilePath);
  for sModuleFilePathHeader in gasModulesWithDebugOutputEnabledFilePathHeaders:
    if sSourceFilePath.startswith(sModuleFilePathHeader):
      if gbShowInternalDebugOutput:
        print "  YES! Location starts with %s..." % repr(sModuleFilePathHeader);
      return True;
    if gbShowInternalDebugOutput:
      print "  Location does not start with %s..." % repr(sModuleFilePathHeader);
  if cClass is None or cClass not in gacClassesWithDebugOutputEnabled:
    if gbShowInternalDebugOutput:
      for cClass in gacClassesWithDebugOutputEnabled:
        print "  Class is not %s..." % repr(cClass);
      print "  NO.";
    return False;
  if gbShowInternalDebugOutput:
    print "  YES! Class is %s..." % repr(cClass);
  return True;
