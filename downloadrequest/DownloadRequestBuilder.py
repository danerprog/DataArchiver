from downloadrequest.DownloadRequestJsonFileManager import DownloadRequestJsonFileManager
from downloadrequest.DownloadRequestCsvFileManager import DownloadRequestCsvFileManager
from utils.Logger import Logger

import os.path

class DownloadRequestBuilder(object) :
    
    def __init__(self, filename) :
        self._logger = Logger.getLogger("DownloadRequestBuilder - " + filename)
        self._filename = filename
        self._download_request_file_manager = None
        self._download_requests = {}
        
        self._buildDownloadRequestsIfFileExists()
        
    def _buildDownloadRequestsIfFileExists(self):
        if os.path.isfile(self._filename):
            self._buildDownloadRequests()
        else:
            self._logger.warning("File not found. filename: " + self._filename)
        
    def _buildDownloadRequests(self) :
        self._constructDownloadRequestFileManager()
        
        if self._download_request_file_manager is not None:
            self._fixAndRearrangeDownloadRequestsAccordingToRootDirectory()
        
    def _constructDownloadRequestFileManager(self):
        file_extension = self._filename.split(sep=".")[-1]
        
        if file_extension == "json" :
            self._download_request_file_manager = DownloadRequestJsonFileManager(self._filename)
        elif file_extension == "csv" :
            self._download_request_file_manager = DownloadRequestCsvFileManager(self._filename)
        else : 
            message = "WRN: file extension " + file_extension + " is not supported!"
            self._logger.warning(message)

    def _fixAndRearrangeDownloadRequestsAccordingToRootDirectory(self) :
        for download_request in self._download_request_file_manager.getAcceptableDownloadRequests():
            if "managed_directory_name" not in download_request :
                download_request["managed_directory_name"] = "default"
            
            if "subdirectory" not in download_request :
                download_request["subdirectory"] = ""
                
            self._addDownloadRequest(download_request, download_request["managed_directory_name"])
            
    def _addDownloadRequest(self, download_request_dict, managed_directory_name) :
        if managed_directory_name not in self._download_requests:
            self._download_requests[managed_directory_name] = []

        self._download_requests[managed_directory_name].append(download_request_dict)
  
    def getDownloadRequests(self) :
        return self._download_requests