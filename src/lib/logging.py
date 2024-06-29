from enum import Enum
from timing import get_now_time

class LoggingMode(Enum):
    INFO = 1
    DEBUG = 2
    

class Logging:
    def __init__(self, file_path: str, default_mode: LoggingMode) -> None:
        self._file_path = file_path
        self._default_mode = default_mode
        
    def log(self, *text: str, sep: str = None, wf: bool = 0 , mode: LoggingMode = None):
        if (not mode):
            mode = self._default_mode
            
        match mode:
            case LoggingMode.INFO:
                pass
            
            case LoggingMode.DEBUG:
                pass
            
            
        prefix = get_now_time().strftime('[%Y/%m/%d %H:%M:%S]')     
        output = prefix
        for i in text:
            output += " "+i
            
        if (wf):
            with open("bot.log", "w+", encoding="utf-8") as f:
                f.writelines(output)
        
        print(prefix, *text, sep=sep)