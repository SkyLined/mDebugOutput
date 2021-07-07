gdasSourceCode_by_sFilePath = {};

def fasGetSourceCode(sSourceFilePath):
  asModuleSourceCode = gdasSourceCode_by_sFilePath.get(sSourceFilePath);
  if asModuleSourceCode is None:
    # Try to read all lines using various encodings until one works:
    for sEncoding in ["utf-8", "latin1"]:
      try:
        oSourceFile = open(sSourceFilePath, encoding = sEncoding);
        try:
          asRawLines = oSourceFile.readlines();
        finally:
          oSourceFile.close();
      except IOError:
        asRawLines = []; # Unable to read file -> no lines
      except UnicodeDecodeError as oException:
        continue;
      break;
    asModuleSourceCode = gdasSourceCode_by_sFilePath[sSourceFilePath] = [
      sLine.rstrip("\n").rstrip("\r")
      for sLine in asRawLines
    ];
  return asModuleSourceCode;
