from utils.fileio.TextFile import TextFile

from datetime import datetime
from pathlib import Path

import json

class TextFileManager:

    TEXT_FILE = {}
    
    def __init__(self, filename, mode):
        self._filename = filename
        self._mode = mode
        self._appendSelfToFilenameManagers()
        
    def __del__(self):
        self._removeSelfFromTextFileManagerArray()

        if len(TextFileManager.TEXT_FILE[self._filename]['managers']) == 0:
            self.getFile().close()
            self._renameLogFile()
            
    def _appendSelfToFilenameManagers(self):
        if self._filename not in TextFileManager.TEXT_FILE:
            TextFileManager.TEXT_FILE[self._filename] = {
                'file' : TextFile(self._filename, self._mode),
                'managers' : [],
                'time_instantiated' : self._getCurrentTimestampInString()
            }
        
        TextFileManager.TEXT_FILE[self._filename]['managers'].append(self)

    def _removeSelfFromTextFileManagerArray(self):
        try:
            index = TextFileManager.TEXT_FILE[self._filename]['managers'].index(self)
            TextFileManager.TEXT_FILE[self._filename]['managers'].pop(index)
        except ValueError as e:
            pass
        
    def _getCurrentTimestampInString(self):
        timestamp = datetime.now()
        seconds = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
        return timestamp.strftime("%Y-%m-%d-" + str(seconds))
        
    def _renameLogFile(self):
        fileExtension = "." + self._getFileExtension()
        timeInstantiated = TextFileManager.TEXT_FILE[self._filename]['time_instantiated']
        newFilename = self._filename.replace(fileExtension, "_" + timeInstantiated + fileExtension)
        Path(self._filename).rename(newFilename)
        
    def _getFileExtension(self):
        return self._filename.split(".")[-1]
        
    def getFile(self):
        return TextFileManager.TEXT_FILE[self._filename]['file']