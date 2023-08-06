#Used to print out messages server side, and make them pretty
import datetime
from os import environ

useColor = environ.get("FLASK_LOG_COLOR") == 'True' if environ.get("FLASK_LOG_COLOR") is not None else True
dateFormat = environ.get("FLASK_LOG_DATE_FORMAT") if environ.get("FLASK_LOG_DATE_FORMAT") is not None else "%d/%b/%Y %H:%M:%S"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class log:
    def __init__(self,*messages):
        emptystring = ''
        for msg in messages:
            emptystring += str(msg)
        self.string = emptystring
        self.main = '[LOG] '
        self.timestamp = str(get_current_time())
        
    def success(self):        
        print(bcolors.OKGREEN,self.main,self.timestamp,'[**Success**]',self.string,bcolors.ENDC) if useColor else print(self.main,self.timestamp,'[**Success**]',self.string)
        
    def info(self):
        print(bcolors.OKBLUE,self.main,self.timestamp,'[**Info**]',self.string,bcolors.ENDC) if useColor else print(self.main,self.timestamp,'[**Info**]',self.string)
                
    def warning(self):
        print (bcolors.FAIL,self.main,self.timestamp,'[**Warning**]',self.string,bcolors.ENDC) if useColor else print(self.main,self.timestamp,'[**Warning**]',self.string)
        
    def error(self):
        print (bcolors.WARNING,self.main,self.timestamp,'[**Error**]',self.string,bcolors.ENDC) if useColor else print(self.main,self.timestamp,'[**Error**]',self.string)

def get_current_time():
    return datetime.datetime.now().strftime("["+dateFormat+"]")