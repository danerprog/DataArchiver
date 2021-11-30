from utils.fileio.File import File

import os

class TextFile(File):

    def __init__(self, filename, mode="r+"):
        super().__init__(filename, mode)
        
    def writeLine(self, string):
        self.write(string.strip("\n") + "\n")
        
    def write(self, string):
        self.file().write(string)
        
    def readLine(self):
        return self.file().readline()
        
    def flush(self):
        self.file().flush()
        os.fsync(self.file())