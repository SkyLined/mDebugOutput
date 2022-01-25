guMaxNumberOfLocalVariablesToShow = 40;

def faasCreateConsoleOutputForException(oException, oTraceback, oStack):
  dxExceptionDetails = fdxExceptionDetails(oException, oTraceback);
  a0asConsoleOutputLines = dxExceptionDetails.get("aasConsoleOutputLines", None);
  dxHiddenProperties = dxExceptionDetails.get("dxHiddenProperties", {});
  bShowLocals = dxExceptionDetails.get("bShowLocals", True);
  
  if a0asConsoleOutputLines is None:
    dsAttributes = {};
    for sName in dir(oException):
      if sName[0] != "_":
        try:
          xAttribute = getattr(oException, sName);
        except:
          dsAttributes[sName] = "<inaccessible>";
        else:
          dsAttributes[sName] = fsToString(xAttribute);
    aasConsoleOutputLines = [
      [guExceptionInformationColor, "Exception attributes:"],
    ] + [
      [
        guExceptionInformationHighlightColor, sName,
        guExceptionInformationColor, " = ", 
        guExceptionInformationHighlightColor, sValue
      ]
      for (sName, sValue) in dsAttributes.items()
    ];
  else:
    aasConsoleOutputLines = a0asConsoleOutputLines;
    bAdditionalAttributes = False;
    for sName in sorted(dir(oException)):
      if sName[0] == "_":
        continue;
      try:
        xValue = getattr(oException, sName);
      except AttributeError:
        continue; # This is unexpected but happens for the 'characters_written' attribute of OSError objects.
      if sName in dxHiddenProperties and dxHiddenProperties[sName] == xValue:
        continue;
      if not bAdditionalAttributes:
        aasConsoleOutputLines += [
          [],
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
    if oStack.o0TopFrame:
      asLocalVariableNames = sorted(list(oStack.o0TopFrame.dxLocalVariables.keys()), key = str.lower);
    else:
      asLocalVariableNames = [];
    if len(asLocalVariableNames) > guMaxNumberOfLocalVariablesToShow:
      # Try to filter out constants by removing all variables whose names is IN_ALL_CAPS:
      asLocalVariableNames = [sLocalVariableName for sLocalVariableName in asLocalVariableNames if sLocalVariableName.upper() != sLocalVariableName];
    bTooManyLocalVariables = len(asLocalVariableNames) > guMaxNumberOfLocalVariablesToShow;
    for sName in asLocalVariableNames[:guMaxNumberOfLocalVariablesToShow]:
      xValue = oStack.o0TopFrame.dxLocalVariables[sName]; # This code is only execute if o0TopFrame is not None
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
  return aasConsoleOutputLines;
  
from .fdxExceptionDetails import fdxExceptionDetails;
from .fsToString import fsToString;
from .mColorsAndChars import *;

