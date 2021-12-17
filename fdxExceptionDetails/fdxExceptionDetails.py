from .fdxExceptionDetailsForAssertionError import fdxExceptionDetailsForAssertionError;
from .fdxExceptionDetailsForAttributeError import fdxExceptionDetailsForAttributeError;
from .fdxExceptionDetailsForImportError import fdxExceptionDetailsForImportError;
from .fdxExceptionDetailsForKeyError import fdxExceptionDetailsForKeyError;
from .fdxExceptionDetailsForNameError import fdxExceptionDetailsForNameError;
from .fdxExceptionDetailsForSyntaxError import fdxExceptionDetailsForSyntaxError;
from .fdxExceptionDetailsForTypeError import fdxExceptionDetailsForTypeError;
from .fdxExceptionDetailsForUnicodeDecodeError import fdxExceptionDetailsForUnicodeDecodeError;
from .fdxExceptionDetailsForValueError import fdxExceptionDetailsForValueError;
from .fdxExceptionDetailsForWindowsError import fdxExceptionDetailsForWindowsError;
# Optional
try: 
  import json as m0json;
except:
  m0json = None;
else:
  from .fdxExceptionDetailsForJSONDecodeError import fdxExceptionDetailsForJSONDecodeError;
try:
  import mWindowsSDK as m0WindowsSDK;
except:
  m0WindowsSDK = None;
else:
  from .fdxExceptionDetailsFor_mWindowsSDK_cDLL_cInvalidFunctionArgumentsException import fdxExceptionDetailsFor_mWindowsSDK_cDLL_cInvalidFunctionArgumentsException;

def fdxExceptionDetails(oException, oTraceback):
  if isinstance(oException, AssertionError):
    return fdxExceptionDetailsForAssertionError(oException);
  elif isinstance(oException, AttributeError):
    return fdxExceptionDetailsForAttributeError(oException);
  elif isinstance(oException, ImportError):
    return fdxExceptionDetailsForImportError(oException);
  elif isinstance(oException, KeyError):
    return fdxExceptionDetailsForKeyError(oException);
  elif isinstance(oException, NameError):
    return fdxExceptionDetailsForNameError(oException);
  elif isinstance(oException, SyntaxError):
    return fdxExceptionDetailsForSyntaxError(oException);
  elif isinstance(oException, TypeError):
    return fdxExceptionDetailsForTypeError(oException, oTraceback);
  elif isinstance(oException, UnicodeDecodeError):
    return fdxExceptionDetailsForUnicodeDecodeError(oException);
  elif isinstance(oException, ValueError):
    return fdxExceptionDetailsForValueError(oException);
  elif isinstance(oException, WindowsError):
    return fdxExceptionDetailsForWindowsError(oException);
  elif m0json and isinstance(oException, m0json.decoder.JSONDecodeError):
    return fdxExceptionDetailsForJSONDecodeError(oException);
  elif m0WindowsSDK and isinstance(oException, m0WindowsSDK.cDLL.cInvalidFunctionArgumentsException):
    return fdxExceptionDetailsFor_mWindowsSDK_cDLL_cInvalidFunctionArgumentsException(oException);
  else:
    return {};
