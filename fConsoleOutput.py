from .mColors import *;

try:
  from oConsole import oConsole;
except:
  class oConsole(object):
    @staticmethod
    def fLock():
      pass;
    @staticmethod
    def fOutput(*axMessage, **dxIgnored):
      print "".join([ str(x) for x in axMessage if isinstance(x, (str, unicode)) ]);
    @staticmethod
    def fUnlock():
      pass;

def fConsoleOutput(sTitle, aasConsoleOutputLines):
  oConsole.fLock();
  try:
    oConsole.fOutput(guBoxColor, "\xDA\xC4\xC4[ ", guBoxTitleColor, sTitle, guBoxColor, " ]", sPadding = "\xC4");
    for asConsoleOutputLine in aasConsoleOutputLines:
      oConsole.fOutput(guBoxColor, "\xB3 ", *asConsoleOutputLine);
    oConsole.fOutput(guBoxColor, "\xC0", sPadding = "\xC4");
  finally:
    oConsole.fUnlock();
  

