from environment.Exceptions import UndefinedManagedDirectoryNameException
from utils.fileio.JsonFileReader import JsonFileReader
from utils.fileio.JsonFileWriter import JsonFileWriter
from utils.Logger import Logger

from pathlib import Path
import traceback

class ConfigJsonFileManager(object) :

    CONFIG_FILE_CONTENTS = {
        "root" : "[optional. if not provided, the current working directory will be used]",
        "working_directory" : "[optional. if not provided, the program will use a default value]",
        "managed_directories" : {
            "default" : "<required managed_directory_name. all downloads without a specified managed_directory_name will be placed in this directory>",
            "managed_directory_name" : "[optional. you can specify as many managed_directory_names as you like as long as they are valid directories]"
        },
        "logger" : {
            "log_printing_level" : "[optional int. if no value is provided then no logs will be printed]",
            "console_printing_level" : "[optional int. if no value is provided then no logs will be printed]"
        },
        "download" : {
            "rate_limit" : "[optional int. if no value is provided then the default value will be 100000 (100KBps)])",
            "number_of_retries" : "[optional int. if no value is provided then the default value will be 0]"
        }
    }
    
    SAMPLE_CONFIG_FILENAME = "sample_config.json"
    DEFAULT_WORKING_DIRECTORY = ".youtubearchiver"
    DEFAULT_LOGGING_LEVEL = Logger.LEVEL["NONE"]
    DEFAULT_RATE_LIMIT = 100000
    DEFAULT_NUMBER_OF_RETRIES = 0

    def __init__(self, filename):
        self._configuration = {}
    
        try :
            self._json_file = JsonFileReader(filename)
            self._json_dictionary = self._json_file.read()
            
            if self._areRequiredKeysNotPresent():
                self._generateConfigFile()
                self._throwValueError()
            else: 
                self._getConfigurationValues()
                
        except FileNotFoundError as e:
            self._generateConfigFile()
            raise FileNotFoundError("File " + filename + " is not found. See " + ConfigJsonFileManager.SAMPLE_CONFIG_FILENAME + " to guide you on how to create a config file.")

    def _getConfigurationValues(self):
        self._configuration["root"] = self._json_dictionary["root"] if "root" in self._json_dictionary else str(Path().resolve())
        self._configuration["working_directory"] = self._json_dictionary["working_directory"] if "working_directory" in self._json_dictionary else ConfigJsonFileManager.DEFAULT_WORKING_DIRECTORY
        self._configuration["managed_directories"] = self._json_dictionary["managed_directories"]
        self._getLoggerConfigurationValues()
        self._getDownloadConfigurationValues()
        
    def _getLoggerConfigurationValues(self):
        self._configuration["logger"] = self._json_dictionary["logger"] if "logger" in self._json_dictionary else {}
        
        try:
            self._configuration["logger"]["log_printing_level"] = int(self._configuration["logger"]["log_printing_level"])
        except ValueError as e:
            try:
                self._configuration["logger"]["log_printing_level"] = Logger.LEVEL[self._configuration["logger"]["log_printing_level"].upper()]
            except KeyError as e:
                self._configuration["logger"]["log_printing_level"] = ConfigJsonFileManager.DEFAULT_LOGGING_LEVEL
        except (NameError, KeyError) as e:
            self._configuration["logger"]["log_printing_level"] = ConfigJsonFileManager.DEFAULT_LOGGING_LEVEL

        try:
            self._configuration["logger"]["console_printing_level"] = int(self._configuration["logger"]["console_printing_level"])
        except ValueError as e:
            try:
                self._configuration["logger"]["console_printing_level"] = Logger.LEVEL[self._configuration["logger"]["console_printing_level"].upper()]
            except KeyError as e:
                self._configuration["logger"]["console_printing_level"] = ConfigJsonFileManager.DEFAULT_LOGGING_LEVEL
        except (NameError, KeyError) as e:
            self._configuration["logger"]["console_printing_level"] = ConfigJsonFileManager.DEFAULT_LOGGING_LEVEL
          
    def _getDownloadConfigurationValues(self):
        self._configuration["download"] = self._json_dictionary["download"] if "download" in self._json_dictionary else {}
        
        try:
            self._configuration["download"]["rate_limit"] = int(self._configuration["download"]["rate_limit"])
        except (ValueError, NameError, KeyError) as e:
            self._configuration["download"]["rate_limit"] = ConfigJsonFileManager.DEFAULT_RATE_LIMIT
            
        try:
            self._configuration["download"]["number_of_retries"] = int(self._configuration["download"]["number_of_retries"])
        except (ValueError, NameError, KeyError) as e:
            self._configuration["download"]["number_of_retries"] = ConfigJsonFileManager.DEFAULT_NUMBER_OF_RETRIES

    def _areRequiredKeysNotPresent(self) :
        return "managed_directories" not in self._json_dictionary or "default" not in self._json_dictionary["managed_directories"]
        
    def _throwValueError(self):
        message_to_throw = "The following keys are missing: \n\n"
        
        if "managed_directories" not in self._json_dictionary:
            message_to_throw += "Key 'managed_directories' is not found in json file!\n"
            
            if "default" not in self._json_dictionary["managed_directories"]:
                message_to_throw += "Key 'default' is not found under key 'managed_directories'!\n"
                
        message_to_throw += "\n See " + ConfigJsonFileManager.SAMPLE_CONFIG_FILENAME + " to guide you on how to create a config file."
            
        raise ValueError(message_to_throw)
            
    def _generateConfigFile(self):
        json_file_writer = JsonFileWriter("sample_config.json", ConfigJsonFileManager.CONFIG_FILE_CONTENTS)
        json_file_writer.write()

    def getRoot(self):
        return self._configuration["root"]
        
    def getManagedDirectoryPath(self, managed_directory_name):
        try:
            return self._configuration["managed_directories"][managed_directory_name]
        except KeyError as e:
            raise UndefinedManagedDirectoryNameException(str(e))
        
    def getWorkingDirectory(self):
        return self._configuration["working_directory"]
        
    def getLogPrintingLevel(self):
        return self._configuration["logger"]["log_printing_level"]
        
    def getConsolePrintingLevel(self):
        return self._configuration["logger"]["console_printing_level"]
        
    def getRateLimit(self):
        return self._configuration["download"]["rate_limit"]
        
    def getNumberOfRetries(self):
        return self._configuration["download"]["number_of_retries"]

    
    