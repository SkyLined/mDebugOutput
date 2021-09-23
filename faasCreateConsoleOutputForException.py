from .HideInCallStack import HideInCallStack;

guMaxNumberOfLocalVariablesToShow = 40;

@HideInCallStack
def faasCreateConsoleOutputForException(oException, oTraceback, oStack):
  dxExceptionDetails = fdxExceptionDetails(oException, oTraceback);
  a0asConsoleOutputLines = dxExceptionDetails.get("aasConsoleOutputLines", None);
  dxHiddenProperties = dxExceptionDetails.get("dxHiddenProperties", {});
  bShowLocals = dxExceptionDetails.get("bShowLocals", True);
  
  if a0asConsoleOutputLines is None:
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
    asLocalVariableNames = sorted(list(oStack.oTopFrame.dxLocalVariables.keys()), key = str.lower);
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
  return aasConsoleOutputLines;
  
from .fdxExceptionDetails import fdxExceptionDetails;
from .fsToString import fsToString;
from .mColorsAndChars import *;

