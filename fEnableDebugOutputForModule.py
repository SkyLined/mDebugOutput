from .mGlobals import *;

def fEnableDebugOutputForModule(mModule):
  sModuleFilePathHeader = (
    mModule.__file__[:-len("__init__.py")] if mModule.__file__.lower().endswith("__init__.py") else
    mModule.__file__
  );
  gasModulesWithDebugOutputEnabledFilePathHeaders.add(sModuleFilePathHeader);