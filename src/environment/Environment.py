from environment.ConfigJsonFileManager import ConfigJsonFileManager
from utils.Logger import Logger

import ctypes
from pathlib import Path
import platform

class Environment(object):

    CURRENT_ENVIRONMENT = None

    def __init__(self, config_json_filename):
        self._config_file_manager = ConfigJsonFileManager(config_json_filename)
        self._working_directory = Path(self.configuration().getWorkingDirectory())
        self._prepareEnvironment()
        
    def _prepareEnvironment(self) :
        self._prepareLoggerEnvironment()
        self._createWorkingDirectory()
        
    def _prepareLoggerEnvironment(self):
        configuration = self.configuration()
        Logger.DEFAULT_OUTPUT_FILENAME = configuration.getWorkingDirectory() + "\\log.txt"
        Logger.CURRENT_LOGGING_LEVEL = configuration.getLogPrintingLevel()
        Logger.CURRENT_PRINTING_LEVEL = configuration.getConsolePrintingLevel()
        self._logger = Logger.getLogger("Environment")
      
    def _createWorkingDirectory(self) :
        if not self._working_directory.is_dir():
            self._logger.info("Creating working directory: " + str(self._working_directory))
            self._working_directory.mkdir(exist_ok=True)
            self._hideWorkingDirectoryForWindows()

    def _hideWorkingDirectoryForWindows(self) : 
        if platform.system() == "Windows":
            self._logger.info("Hiding working directory for Windows")
            ctypes.windll.kernel32.SetFileAttributesW(str(self._working_directory.resolve()), 0x02)
    
    def configuration(self):
        return self._config_file_manager

    def setEnvironment(args):
        Environment.CURRENT_ENVIRONMENT = Environment(args["config_file"])
        
    def getEnvironment():
        return Environment.CURRENT_ENVIRONMENT
        

