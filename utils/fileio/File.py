
class File(object):
    
    def __init__(self, filename, mode="r+") :
        self._openedFile = open(filename, mode)
        self._filename = filename
        
    def file(self) :
        return self._openedFile
        
    def seek(self, index) :
        self._openedFile.seek(index)
        
    def name(self) :
        return self._filename
        
    def close(self) :
        self._openedFile.close()
        
    def __del__(self) :
        self.close()