gu0MaxNumberOfLocalVariablesToShow = None;

def faasCreateConsoleOutputForException(oException, oTraceback, oStack):
  dxExceptionDetails = fdxExceptionDetails(oException, oTraceback);
  a0asConsoleOutputLines = dxExceptionDetails.get("aasConsoleOutputLines", None);
  dxHiddenProperties = dxExceptionDetails.get("dxHiddenProperties", {});
  bShowLocals = dxExceptionDetails.get("bShowLocals", True);
  
  dsAttributes = {};
  for sName in sorted(dir(oException)):
    # You'd expect `dir()` to return a list of existing attributes, but it
    # somehow returns some attributes that do not. So we have to check and
    # ignore those that don't exist.
    if sName[0] != "_" and hasattr(oException, sName):
      try:
        xValue = getattr(oException, sName);
      except:
        dsAttributes[sName] = "<inaccessible>";
      else:
        if sName in dxHiddenProperties and dxHiddenProperties[sName] == xValue:
          continue;
        dsAttributes[sName] = fsToString(xValue);
  if a0asConsoleOutputLines is None:
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
    for (sName, xValue) in dsAttributes.items():
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
    bTooManyLocalVariables = gu0MaxNumberOfLocalVariablesToShow is not None and len(asLocalVariableNames) > gu0MaxNumberOfLocalVariablesToShow;
    if bTooManyLocalVariables:
      asLocalVariableNames = asLocalVariableNames[:gu0MaxNumberOfLocalVariablesToShow];
    for sName in asLocalVariableNames:
      xValue = oStack.o0TopFrame.dxLocalVariables[sName]; # This code is only execute if o0TopFrame is not None
      aasConsoleOutputLines += [
        ["  ", guExceptionInformationHighlightColor, sName, guExceptionInformationColor, " = ", fsToString(xValue)],
      ];
    if bTooManyLocalVariables:
      aasConsoleOutputLines += [
        [
          guExceptionInformationColor, "  (... ", 
          guExceptionInformationHighlightColor, str(len(asLocalVariableNames) - gu0MaxNumberOfLocalVariablesToShow),
          guExceptionInformationColor, " variables not shown...)",
        ],
      ];
  return aasConsoleOutputLines;
  
from .fdxExceptionDetails import fdxExceptionDetails;
from .fsToString import fsToString;
from .mColorsAndChars import *;

