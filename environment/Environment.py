from environment.ConfigJsonFileManager import ConfigJsonFileManager
from utils.Logger import Logger

import ctypes
from pathlib import Path
import platform

class Environment(object):

    CURRENT_ENVIRONMENT = None
    DEFAULT_WORKING_DIRECTORY = ".youtubearchiver"

    def __init__(self, config_json_filename):
        self._config_file_manager = ConfigJsonFileManager(config_json_filename)
        self._working_directory = Path(self.getWorkingDirectory())
        self._prepareEnvironment()
        
    def _prepareEnvironment(self) :
        self._prepareLoggerEnvironment()
        self._createWorkingDirectory()
        
    def _prepareLoggerEnvironment(self):
        Logger.DEFAULT_OUTPUT_FILENAME = self.getWorkingDirectory() + "\\" + Logger.DEFAULT_OUTPUT_FILENAME
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
    
    def getRoot(self):
        root = self._config_file_manager.getRoot()
        if root == None:
            root = str(Path().resolve())
        return root
        
    def getManagedDirectoryPath(self, managed_directory_name):
        try:
            return self._config_file_manager.getManagedDirectoryPath(managed_directory_name)
        except KeyError as e:
            raise UndefinedManagedDirectoryNameException(str(e))
        
    def getWorkingDirectory(self):
        directory = self._config_file_manager.getWorkingDirectory()
        if directory == None:
            directory = Environment.DEFAULT_WORKING_DIRECTORY
        return directory
        
    def setEnvironment(args):
        Environment.CURRENT_ENVIRONMENT = Environment(args["config_file"])
        
    def getEnvironment():
        return Environment.CURRENT_ENVIRONMENT
        

class UndefinedManagedDirectoryNameException(Exception):

    def __init__(self, message):
        super().__init__(message)