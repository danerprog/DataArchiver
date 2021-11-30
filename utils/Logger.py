from utils.fileio.TextFileManager import TextFileManager

from datetime import datetime
from pathlib import Path

class Logger(object):
    
    LOGGER = {}
    TEXT_FILES = {}
    LOGGING_LEVEL = {
        "TRACE" : -1,
        "DEBUG" : 0,
        "INFO" : 1,
        "WARNING" : 2,
        "ERROR" : 3,
    }
    CURRENT_LOGGING_LEVEL = LOGGING_LEVEL["TRACE"]
    DEFAULT_OUTPUT_FILENAME = "log.txt"

    def __init__(self, name, outputFilename = DEFAULT_OUTPUT_FILENAME):
        self._loggername = name
        self._outputFilename = outputFilename
        self._changeOutputFile()
    
    def _changeOutputFile(self):
        self._file_manager = TextFileManager(self._outputFilename, "a+")
        self._output_file = self._file_manager.getFile()
    
    def setOutputFile(self, filename):
        if self._output_file.name() != filename:
            self._outputFilename = filename
            self._changeOutputFile()
            
    def trace(self, object):
        if Logger.CURRENT_LOGGING_LEVEL <= Logger.LOGGING_LEVEL["TRACE"]:
            self._write("[" + self._loggername + "][TRC]: " + str(object))
            
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
        timestamp = datetime.utcnow().strftime('%H:%M:%S:%f')[:-3]
        self._output_file.writeLine("[" + timestamp + "]" + string)
        self._output_file.flush()

    def getLogger(name):
        if name not in Logger.LOGGER:
            Logger.LOGGER[name] = Logger(name)
        return Logger.LOGGER[name]
