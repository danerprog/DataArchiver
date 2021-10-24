from utils.fileio.File import File

import json

class JsonFileWriter(File) :

    def __init__(self, filename, content={}) :
        super().__init__(filename, "w+")
        self._content = content
        
    def appendContent(self, content) :
        self._content.append(content)
        
    def extendContent(self, content) :
        self._content.extend(content)
        
    def write(self) :
        json.dump(self._content, self.file(), indent = 4)
        