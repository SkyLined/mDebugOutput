def fdxExceptionDetailsFor_mWindowsSDK_cDLL_cInvalidFunctionArgumentsException(oException):
  uNumberOfProvidedArguments = oException.uNumberOfProvidedArguments;
  uNumberOfExpectedArguments = oException.uNumberOfExpectedArguments;
  u0WrongArgumentIndex = oException.u0WrongArgumentIndex;
  aoArgumentDetails = oException.aoArgumentDetails;
  if uNumberOfProvidedArguments < uNumberOfExpectedArguments:
    axMessage = [
      guExceptionInformationColor, "There are ",
      guExceptionInformationHighlightColor, str(uNumberOfExpectedArguments - uNumberOfProvidedArguments),
      guExceptionInformationColor, " arguments missing",
    ];
  elif uNumberOfProvidedArguments > uNumberOfExpectedArguments:
    axMessage = [
      guExceptionInformationColor, "There are ",
      guExceptionInformationHighlightColor, str(uNumberOfProvidedArguments - uNumberOfExpectedArguments),
      guExceptionInformationColor, " superfluous arguments",
    ];
  elif u0WrongArgumentIndex is not None:
    axMessage = [
      guExceptionInformationColor, "Argument #",
      guExceptionInformationHighlightColor, str(u0WrongArgumentIndex + 1),
      guExceptionInformationColor, " is invalid",
    ];
  else:
    axMessage = [guExceptionInformationColor, "There is/are invalid argument(s)"];
  axMessage += [
    guExceptionInformationColor, " in a DLL function call:",
  ];
  aasConsoleOutputLines = [
    axMessage,
    [
    ], [
      guExceptionInformationHighlightColor, oException.sDLLName,
      guExceptionInformationColor, ":",
      guExceptionInformationHighlightColor, oException.sFunctionName,
      guExceptionInformationColor, "(",
    ],
  ];
  for oArgumentDetails in aoArgumentDetails:
    sStatusChar = " ";
    uArgumentIndex = oArgumentDetails.uIndex;
    xProvidedArgumentValue = oArgumentDetails.xProvidedValue;
    cProvidedArgumentType = xProvidedArgumentValue.__class__;
    cExpectedArgumentType = oArgumentDetails.cExpectedType;
    sHeaderChar = "•";
    uHeaderColor = guExceptionInformationColor;
    if uArgumentIndex < uNumberOfProvidedArguments:
      sProvided = "%s:%s (%s)" % (cProvidedArgumentType.__module__, cProvidedArgumentType.__name__, repr(xProvidedArgumentValue));
      uProvidedColor = guExceptionInformationColor;
    else:
      sProvided = "<missing>";
      uProvidedColor = guExceptionInformationErrorColor;
      sHeaderChar = "×";
      uHeaderColor = guExceptionInformationErrorColor;
    if uArgumentIndex < uNumberOfExpectedArguments:
      sExpected = "%s:%s" % (cExpectedArgumentType.__module__, cExpectedArgumentType.__name__);
      if u0WrongArgumentIndex is None:
        # We do not know which argument is wrong, so flag anything not matching
        # the exact expected type as suspicious:
        if cProvidedArgumentType != cExpectedArgumentType:
          sHeaderChar = "?";
          uProvidedColor = guExceptionInformationHighlightColor;
      elif uArgumentIndex == u0WrongArgumentIndex:
        sHeaderChar = "×";
        uHeaderColor = guExceptionInformationErrorColor;
        uProvidedColor = guExceptionInformationErrorColor;
    else:
      sExpected = "<no argument>";
      sHeaderChar = "×";
      uHeaderColor = guExceptionInformationErrorColor;
      uProvidedColor = guExceptionInformationErrorColor;
    aasConsoleOutputLines += [
      [
        guExceptionInformationColor, "  ",
        uHeaderColor, sHeaderChar,
        guExceptionInformationColor, " ",
        uProvidedColor, sProvided,
        guExceptionInformationColor, ",",
      ],
    ];
    if sHeaderChar != "•":
      aasConsoleOutputLines += [
        [
          guExceptionInformationColor, "    ▲ Expected type: ",
          guExceptionInformationHighlightColor, sExpected,
        ]
      ];
  aasConsoleOutputLines += [
    [
      guExceptionInformationColor, ")",
    ]
  ];
  return {
    "aasConsoleOutputLines": aasConsoleOutputLines,
    "dxHiddenProperties": {
      "args": (oException.sMessage,),
      "with_traceback": oException.with_traceback,
      "add_note": oException.add_note,
      "sMessage": oException.sMessage,
      "sDLLName": oException.sDLLName,
      "sFunctionName": oException.sFunctionName,
      "uNumberOfProvidedArguments": oException.uNumberOfProvidedArguments,
      "uNumberOfExpectedArguments": oException.uNumberOfExpectedArguments,
      "u0WrongArgumentIndex": oException.u0WrongArgumentIndex,
      "aoArgumentDetails": oException.aoArgumentDetails,
    },
  };

from ..mColorsAndChars import *;
