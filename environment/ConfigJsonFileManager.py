from utils.fileio.JsonFileReader import JsonFileReader
from utils.fileio.JsonFileWriter import JsonFileWriter
from utils.Logger import Logger

import traceback

class ConfigJsonFileManager(object) :

    CONFIG_FILE_CONTENTS = {
        "root" : "[optional. if not provided, the current working directory will be used]",
        "working_directory" : "[optional. if not provided, the program will use a default value]",
        "managed_directories" : {
            "default" : "<required managed_directory_name. all downloads without a specified managed_directory_name will be placed in this directory>",
            "managed_directory_name" : "[optional. you can specify as many managed_directory_names as you like as long as they are valid directories]"
        }
    }
    
    SAMPLE_CONFIG_FILENAME = "sample_config.json"

    def __init__(self, filename):
        self._logger = Logger.getLogger("ConfigJsonFileManager")
    
        try :
            self._jsonfile = JsonFileReader(filename)
            self._jsondict = self._jsonfile.read()
            
            if self._areRequiredKeysNotPresent():
                self._generateConfigFile()
                self._throwValueError()
                
        except FileNotFoundError as e:
            self._generateConfigFile()
            self._logger.error(traceback.format_exc())
            raise FileNotFoundError("File " + filename + " is not found. See " + ConfigJsonFileManager.SAMPLE_CONFIG_FILENAME + " to guide you on how to create a config file.")


    def _areRequiredKeysNotPresent(self) :
        return "managed_directories" not in self._jsondict or "default" not in self._jsondict["managed_directories"]
        
    def _throwValueError(self):
        message_to_throw = "The following keys are missing: \n\n"
        
        if "managed_directories" not in self._jsondict:
            message_to_throw += "Key 'managed_directories' is not found in json file!\n"
            
            if "default" not in self._jsondict["managed_directories"]:
                message_to_throw += "Key 'default' is not found under key 'managed_directories'!\n"
                
        message_to_throw += "\n See " + ConfigJsonFileManager.SAMPLE_CONFIG_FILENAME + " to guide you on how to create a config file."
            
        raise ValueError(message_to_throw)
            
    def _generateConfigFile(self):
        json_file_writer = JsonFileWriter("sample_config.json", ConfigJsonFileManager.CONFIG_FILE_CONTENTS)
        json_file_writer.write()

    def getRoot(self):
        root = None
        if "root" in self._jsondict:
            root = self._jsondict["root"]
        return root
        
    def getManagedDirectoryPath(self, managed_directory_name):
        return self._jsondict["managed_directories"][managed_directory_name]
        
    def getWorkingDirectory(self):
        directory = None
        if "working_directory" in self._jsondict:
            directory = self._jsondict["working_directory"]
        return directory
        
    
        