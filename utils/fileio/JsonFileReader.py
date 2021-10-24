from utils.fileio.File import File

import json

class JsonFileReader(File) :

    def __init__(self, filename) :
        super().__init__(filename, "r")
        self._content = None
    
    def _loadJson(self) :
        self._content = json.loads(self.file().read())
 
    def read(self) :
        if self._content == None :
            self._loadJson()
        return self._content
        