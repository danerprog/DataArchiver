from utils.fileio.File import File
from utils.Logger import Logger

from utils.fileio.TextFile import TextFile

from pathlib import Path

class DownloadRequestCsvFileManager(object):

    def __init__(self, filename):
        self._logger = Logger.getLogger("DownloadRequestCsvFileManager - " + filename)
        self._filename = filename
        self._createAndOpenFile()
        
        self._csv_keys = []
        self._extractCsvKeys()
     
    def _extractCsvKeys(self):
        self._logger.debug("_extractCsvKeys() called")
        first_line = self._csv_file.readLine()
        
        self._logger.debug("Line read from file: " + first_line)
        tokens = first_line.split(sep=",")
        
        for token in tokens:
            self._logger.debug("token: " + token)
            self._csv_keys.append(token.strip())
            
    def _createAndOpenFile(self):
        self._logger.debug("_createAndOpenFile() called")
        self._createNewCsvFileIfItDoesNotExist()
        self._csv_file = TextFile(self._filename, "r+")
       
    def _createNewCsvFileIfItDoesNotExist(self):
        path = Path(self._filename)
        if not path.is_file():
            self._csv_file = TextFile(self._filename, "a")
            self._writeDownloadRequestKeys()
        
    def getAcceptableDownloadRequests(self):
        acceptable_download_requests = []
        for line in self._csv_file.file():
            if line.replace(' ', '').replace('\n', '').replace('\r', '') != "" :
                self._logger.debug("Line is not empty. Processing...")
                download_request = {}
                self._logger.debug(line)
                tokens = line.split(sep=",")
                
                for index in range(0, len(self._csv_keys)):
                    csv_key = self._csv_keys[index]
                    value = ""
                    
                    try :
                        value = tokens[index].strip()
                    except IndexError :
                        pass
                    
                    download_request[csv_key] = value
                    
                self._logger.debug(str(download_request))
                acceptable_download_requests.append(download_request)
            
        return acceptable_download_requests
            
    def getFilename(self):
        return self._filename
        
    def addDownloadRequest(self, download_request_dictionary):
        self._logger.debug("addDownloadRequest() called. download_request_dictionary: " + str(download_request_dictionary))
        line_to_write = ""
        
        for key in self._csv_keys:
            value_to_write = ""
            if key in download_request_dictionary:
                value_to_write = download_request_dictionary[key]
            self._logger.debug("key: " + key + ", value_to_write: " + value_to_write)
            line_to_write += value_to_write + ","

        self._logger.debug("line_to_write: " + line_to_write)
        self._csv_file.writeLine(line_to_write[:-1])
        
    def _writeDownloadRequestKeys(self):
        self._logger.info("Writing download request keys to csv file")
        self._csv_file.writeLine("url, managed_directory_name, subdirectory")
    