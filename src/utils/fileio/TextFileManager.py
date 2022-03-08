from utils.fileio.TextFile import TextFile
from utils.resourcemanagement.Cleanable import Cleanable
from utils.resourcemanagement.Cleaner import Cleaner

from datetime import datetime
from pathlib import Path

import json

class TextFileManager(Cleanable):

    TEXT_FILE = {}
    
    def __init__(self, filename, mode):
        self._filename = filename
        self._mode = mode
        self._appendSelfToFilenameManagers()
        Cleaner.getCleaner().register(self)
    
    def _appendSelfToFilenameManagers(self):
        if self._filename not in TextFileManager.TEXT_FILE:
            TextFileManager.TEXT_FILE[self._filename] = {
                'file' : TextFile(self._filename, self._mode),
                'managers' : []
            }
        
        TextFileManager.TEXT_FILE[self._filename]['managers'].append(self)

    def _removeSelfFromTextFileManagerArray(self):
        try:
            index = TextFileManager.TEXT_FILE[self._filename]['managers'].index(self)
            TextFileManager.TEXT_FILE[self._filename]['managers'].pop(index)
        except ValueError as e:
            pass
            
    def _triggerObjectDeletionProcedures(self):
        pass
    
    def getFile(self):
        return TextFileManager.TEXT_FILE[self._filename]['file']
        
    def clean(self):
        self._removeSelfFromTextFileManagerArray()

        if len(TextFileManager.TEXT_FILE[self._filename]['managers']) == 0:
            self.getFile().close()
            self._triggerObjectDeletionProcedures()
       
       
class TimestampedTextFileManager(TextFileManager):
    
    def __init__(self, filename, mode):
        super().__init__(filename, mode)
        self._appendTimeInstantiatedToFilenameManagerIfNeeded()
        
    def _appendTimeInstantiatedToFilenameManagerIfNeeded(self):
        if self._filename in TextFileManager.TEXT_FILE and 'time_instantiated' not in TextFileManager.TEXT_FILE[self._filename]:
            TextFileManager.TEXT_FILE[self._filename]['time_instantiated'] = self._getCurrentTimestampInString()
    
    def _getCurrentTimestampInString(self):
        timestamp = datetime.now()
        seconds = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
        return timestamp.strftime("%Y-%m-%d-" + str(seconds))
        
    def _getFileExtension(self):
        return self._filename.split(".")[-1]
        
    def _renameLogFile(self):
        fileExtension = "." + self._getFileExtension()
        timeInstantiated = TextFileManager.TEXT_FILE[self._filename]['time_instantiated']
        newFilename = self._filename.replace(fileExtension, "_" + timeInstantiated + fileExtension)
        Path(self._filename).rename(newFilename)
        
    def _triggerObjectDeletionProcedures(self):
        self._renameLogFile()
        