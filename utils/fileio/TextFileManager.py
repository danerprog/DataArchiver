from utils.fileio.TextFile import TextFile


class TextFileManager:

    TEXT_FILE = {}
    
    def __init__(self, filename, mode):
        self._filename = filename
        self._mode = mode
        self._appendSelfToFilenameManagers()
        
    def __del__(self):
        if len(TextFileManager.TEXT_FILE[self._filename]['managers']) == 1:
            self.getFile().close()
        
    def _appendSelfToFilenameManagers(self):
        if self._filename not in TextFileManager.TEXT_FILE:
            TextFileManager.TEXT_FILE[self._filename] = {
                'file' : TextFile(self._filename, self._mode),
                'managers' : []
            }

        TextFileManager.TEXT_FILE[self._filename]['managers'].append(self)
        
    def getFile(self):
        return TextFileManager.TEXT_FILE[self._filename]['file']