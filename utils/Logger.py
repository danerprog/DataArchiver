from utils.fileio.TextFileManager import TextFileManager

from datetime import datetime
from pathlib import Path

class Logger(object):
    
    LOGGER = {}
    TEXT_FILES = {}
    LEVEL = {
        "TRACE" : -1,
        "DEBUG" : 0,
        "INFO" : 1,
        "WARNING" : 2,
        "ERROR" : 3,
    }
    CURRENT_LOGGING_LEVEL = LEVEL["TRACE"]
    CURRENT_PRINTING_LEVEL = LEVEL["INFO"]
    DEFAULT_OUTPUT_FILENAME = "log.txt"

    def __init__(self, name, outputFilename = None):
        self._loggerName = name
        self._outputFilename = outputFilename if outputFilename is not None else Logger.DEFAULT_OUTPUT_FILENAME
        self._changeOutputFile()
    
    def _changeOutputFile(self):
        self._file_manager = TextFileManager(self._outputFilename, "a+")
        self._output_file = self._file_manager.getFile()
    
    def setOutputFile(self, filename):
        if self._output_file.name() != filename:
            self._outputFilename = filename
            self._changeOutputFile()
            
    def trace(self, object):
        message = self._buildStringToPrint("TRC", object)
        self._writeIfAllowed(message, Logger.LEVEL["TRACE"])
            
    def debug(self, object):
        message = self._buildStringToPrint("DBG", object)
        self._writeIfAllowed(message, Logger.LEVEL["DEBUG"])

    def info(self, object):
        message = self._buildStringToPrint("INF", object)
        self._writeIfAllowed(message, Logger.LEVEL["INFO"])

    def warning(self, object):
        message = self._buildStringToPrint("WRN", object)
        self._writeIfAllowed(message, Logger.LEVEL["WARNING"])
        
    def error(self, object):
        message = self._buildStringToPrint("ERR", object)
        self._writeIfAllowed(message, Logger.LEVEL["ERROR"])
            
    def _writeIfAllowed(self, message, loggerLevel):
        if Logger.CURRENT_LOGGING_LEVEL <= loggerLevel:
            self._writeToFile(message)
            
        if Logger.CURRENT_PRINTING_LEVEL <= loggerLevel:
            print(message)
            
    def _writeToFile(self, string):
        timestamp = datetime.utcnow().strftime('%H:%M:%S:%f')[:-3]
        self._output_file.writeLine("[" + timestamp + "]" + string)
        self._output_file.flush()
        
    def _buildStringToPrint(self, shorthandStringForLevel, object):
        return "[" + self._loggerName + "][" + shorthandStringForLevel + "]: " + str(object)

    def getLogger(name):
        if name not in Logger.LOGGER:
            Logger.LOGGER[name] = Logger(name)
        return Logger.LOGGER[name]
