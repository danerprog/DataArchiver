from utils.fileio.TextFile import TextFile

from pathlib import Path

class Logger(object):
    
    LOGGER = {}
    LOGGING_LEVEL = {
        "DEBUG" : 0,
        "INFO" : 1,
        "WARNING" : 2,
        "ERROR" : 3,
    }
    CURRENT_LOGGING_LEVEL = LOGGING_LEVEL["DEBUG"]
    DEFAULT_OUTPUT_FILENAME = "log.txt"

    def __init__(self, name):
        self._loggername = name
        self._changeOutputFile()
    
    def _changeOutputFile(self):
        self._output_file = TextFile(Logger.DEFAULT_OUTPUT_FILENAME, "a+")
    
    def setOutputFile(filename):
        if self._output_file.name() != filename:
            self._changeOutputFile()
            
    def debug(self, object):
        if Logger.CURRENT_LOGGING_LEVEL <= Logger.LOGGING_LEVEL["DEBUG"]:
            self._write("[" + self._loggername + "][DBG]: " + str(object))
        
    def info(self, object):
        if Logger.CURRENT_LOGGING_LEVEL <= Logger.LOGGING_LEVEL["INFO"]:
            self._write("[" + self._loggername + "][INF]: " + str(object))
        
    def warning(self, object):
        if Logger.CURRENT_LOGGING_LEVEL <= Logger.LOGGING_LEVEL["WARNING"]:
            self._write("[" + self._loggername + "][WRN]: " + str(object))
        
    def error(self, object):
        if Logger.CURRENT_LOGGING_LEVEL <= Logger.LOGGING_LEVEL["ERROR"]:
            self._write("[" + self._loggername + "][ERR]: " + str(object))
            
    def _write(self, string):
        self._output_file.writeLine(string)

    def getLogger(name):
        if name not in Logger.LOGGER:
            Logger.LOGGER[name] = Logger(name)
        return Logger.LOGGER[name]