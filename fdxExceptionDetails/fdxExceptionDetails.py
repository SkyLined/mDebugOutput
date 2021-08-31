try: 
  import json as m0json;
except:
  m0json = None;

from .fdxExceptionDetailsForAssertionError import fdxExceptionDetailsForAssertionError;
from .fdxExceptionDetailsForAttributeError import fdxExceptionDetailsForAttributeError;
from .fdxExceptionDetailsForImportError import fdxExceptionDetailsForImportError;
if m0json:
  from .fdxExceptionDetailsForJSONDecodeError import fdxExceptionDetailsForJSONDecodeError;
from .fdxExceptionDetailsForKeyError import fdxExceptionDetailsForKeyError;
from .fdxExceptionDetailsForNameError import fdxExceptionDetailsForNameError;
from .fdxExceptionDetailsForSyntaxError import fdxExceptionDetailsForSyntaxError;
from .fdxExceptionDetailsForTypeError import fdxExceptionDetailsForTypeError;
from .fdxExceptionDetailsForUnboundLocalError import fdxExceptionDetailsForUnboundLocalError;
from .fdxExceptionDetailsForUnicodeDecodeError import fdxExceptionDetailsForUnicodeDecodeError;
from .fdxExceptionDetailsForValueError import fdxExceptionDetailsForValueError;
from .fdxExceptionDetailsForWindowsError import fdxExceptionDetailsForWindowsError;

def fdxExceptionDetails(oException, oTraceback):
  if isinstance(oException, AssertionError):
    return fdxExceptionDetailsForAssertionError(oException);
  elif isinstance(oException, AttributeError):
    return fdxExceptionDetailsForAttributeError(oException);
  elif isinstance(oException, ImportError):
    return fdxExceptionDetailsForImportError(oException);
  elif m0json and isinstance(oException, m0json.decoder.JSONDecodeError):
    return fdxExceptionDetailsForJSONDecodeError(oException);
  elif isinstance(oException, KeyError):
    return fdxExceptionDetailsForKeyError(oException);
  elif isinstance(oException, NameError):
    return fdxExceptionDetailsForNameError(oException);
  elif isinstance(oException, SyntaxError):
    return fdxExceptionDetailsForSyntaxError(oException);
  elif isinstance(oException, TypeError):
    return fdxExceptionDetailsForTypeError(oException, oTraceback);
  elif isinstance(oException, UnboundLocalError):
    return fdxExceptionDetailsForUnboundLocalError(oException);
  elif isinstance(oException, UnicodeDecodeError):
    return fdxExceptionDetailsForUnicodeDecodeError(oException);
  elif isinstance(oException, ValueError):
    return fdxExceptionDetailsForValueError(oException);
  elif isinstance(oException, WindowsError):
    return fdxExceptionDetailsForWindowsError(oException);
  else:
    return {};
