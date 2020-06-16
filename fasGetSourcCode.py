import inspect;

gdasSourceCode_by_sFilePath = {};

def fasGetSourceCode(sSourceFilePath):
  asModuleSourceCode = gdasSourceCode_by_sFilePath.get(sSourceFilePath);
  if asModuleSourceCode is None:
    sOpenMode = inspect.getmoduleinfo(sSourceFilePath)[2];
    try:
      oSourceFile = open(sSourceFilePath, sOpenMode);
      try:
        asModuleSourceCode = gdasSourceCode_by_sFilePath[sSourceFilePath] = [
          sLine.rstrip("\n").rstrip("\r")
          for sLine in oSourceFile.readlines()
        ];
      finally:
        oSourceFile.close();
    except IOError:
      asModuleSourceCode = gdasSourceCode_by_sFilePath[sSourceFilePath] = [];
  return asModuleSourceCode;
