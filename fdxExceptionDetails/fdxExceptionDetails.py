import re;

from .fdxExceptionDetailsForAssertionError import fdxExceptionDetailsForAssertionError;
from .fdxExceptionDetailsForAttributeError import fdxExceptionDetailsForAttributeError;
from .fdxExceptionDetailsForImportError import fdxExceptionDetailsForImportError;
from .fdxExceptionDetailsForKeyError import fdxExceptionDetailsForKeyError;
from .fdxExceptionDetailsForModuleNotFoundError import fdxExceptionDetailsForModuleNotFoundError;
from .fdxExceptionDetailsForNameError import fdxExceptionDetailsForNameError;
from .fdxExceptionDetailsForReError import fdxExceptionDetailsForReError;
from .fdxExceptionDetailsForSyntaxError import fdxExceptionDetailsForSyntaxError;
from .fdxExceptionDetailsForTypeError import fdxExceptionDetailsForTypeError;
from .fdxExceptionDetailsForUnboundLocalError import fdxExceptionDetailsForUnboundLocalError;
from .fdxExceptionDetailsForUnicodeDecodeError import fdxExceptionDetailsForUnicodeDecodeError;
from .fdxExceptionDetailsForUnicodeEncodeError import fdxExceptionDetailsForUnicodeEncodeError;
from .fdxExceptionDetailsForValueError import fdxExceptionDetailsForValueError;
from .fdxExceptionDetailsForWindowsError import fdxExceptionDetailsForWindowsError;
# Optional
try: 
  from json.decoder import JSONDecodeError as JSONDecodeError;
except:
  bJSONSupportEnabled = False;
else:
  bJSONSupportEnabled = True;
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
    if isinstance(oException, ModuleNotFoundError):
      return fdxExceptionDetailsForModuleNotFoundError(oException);
    else:
      return fdxExceptionDetailsForImportError(oException);
  elif isinstance(oException, KeyError):
    return fdxExceptionDetailsForKeyError(oException);
  elif isinstance(oException, NameError):
    if isinstance(oException, UnboundLocalError):
      return fdxExceptionDetailsForUnboundLocalError(oException);
    else:
      return fdxExceptionDetailsForNameError(oException);
  elif isinstance(oException, re.error):
    return fdxExceptionDetailsForReError(oException);
  elif isinstance(oException, SyntaxError):
    return fdxExceptionDetailsForSyntaxError(oException);
  elif isinstance(oException, TypeError):
    return fdxExceptionDetailsForTypeError(oException, oTraceback);
  elif isinstance(oException, UnicodeDecodeError):
    return fdxExceptionDetailsForUnicodeDecodeError(oException);
  elif isinstance(oException, UnicodeEncodeError):
    return fdxExceptionDetailsForUnicodeEncodeError(oException);
  elif isinstance(oException, ValueError):
    if bJSONSupportEnabled and isinstance(oException, JSONDecodeError):
      return fdxExceptionDetailsForJSONDecodeError(oException);
    else:
      return fdxExceptionDetailsForValueError(oException);
  elif isinstance(oException, WindowsError):
    return fdxExceptionDetailsForWindowsError(oException);
  elif m0WindowsSDK and isinstance(oException, m0WindowsSDK.cDLL.cInvalidFunctionArgumentsException):
    return fdxExceptionDetailsFor_mWindowsSDK_cDLL_cInvalidFunctionArgumentsException(oException);
  else:
    return {};
