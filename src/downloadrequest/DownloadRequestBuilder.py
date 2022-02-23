from downloadrequest.DownloadRequestJsonFileManager import DownloadRequestJsonFileManager
from downloadrequest.DownloadRequestCsvFileManager import DownloadRequestCsvFileManager
from utils.Logger import Logger

import os.path

class DownloadRequestBuilder(object) :

    YOUTUBE_URL_PREFIX = "https://www.youtube.com/watch?v="
    
    def __init__(self, logger):
        self._logger = logger
        self._download_requests = {}
        
    def _fixDownloadRequest(self, download_request):
        download_request = self._fixManagedDirectoryName(download_request)
        download_request = self._fixSubdirectory(download_request)
        download_request = self._fixUrl(download_request)
        download_request = self._fixVideoId(download_request)
        download_request = self._fixGetComments(download_request)
        return download_request
            
    def _fixManagedDirectoryName(self, download_request):
        if "managed_directory_name" not in download_request or download_request["managed_directory_name"].strip() == "":
            download_request["managed_directory_name"] = "default"
        return download_request
        
    def _fixSubdirectory(self, download_request):
        if "subdirectory" not in download_request :
            download_request["subdirectory"] = ""
        return download_request
        
    def _fixUrl(self, download_request):
        if "video_id" in download_request and "url" not in download_request:
            download_request["url"] = DownloadRequestBuilder.YOUTUBE_URL_PREFIX + download_request["video_id"]
        return download_request
    
    def _fixVideoId(self, download_request):
        if "video_id" not in download_request or download_request["video_id"].strip() == "":
            download_request["video_id"] = self._getVideoIdFromYoutubeUrl(download_request["url"])  
        return download_request
    
    def _fixGetComments(self, download_request):
        download_request["get_comments"] = "get_comments" in download_request and download_request["get_comments"].lower() == "true"
        return download_request
            
    def _getVideoIdFromYoutubeUrl(self, url):
        return url[url.find("=") + 1:]
            
    def _addDownloadRequest(self, download_request_dict, managed_directory_name) :
        if managed_directory_name not in self._download_requests:
            self._download_requests[managed_directory_name] = []

        self._download_requests[managed_directory_name].append(download_request_dict)
  
    def getDownloadRequests(self) :
        return self._download_requests
        
        
class FileDownloadRequestBuilder(DownloadRequestBuilder):

    def __init__(self, filename) :
        super().__init__(Logger.getLogger("FileDownloadRequestBuilder - " + filename))
        self._filename = filename
        self._download_request_file_manager = None

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
            download_request = self._fixDownloadRequest(download_request)
            self._addDownloadRequest(download_request, download_request["managed_directory_name"])

class SingleDownloadRequestBuilder(DownloadRequestBuilder):
    
    def __init__(self, headers, values):
        super().__init__(Logger.getLogger("SingleDownloadRequestBuilder"))
        self._headers = headers
        self._values = values
        self._logger.info("headers: " + headers + ", values: " + values)
        
        download_request = self._buildDownloadRequest()
        self._addDownloadRequest(download_request, download_request["managed_directory_name"])
        
    def _buildDownloadRequest(self):
        download_request = {}
        header_tokens = self._headers.split(sep=",")
        value_tokens = self._values.split(sep=",")
        
        for index in range(0, len(header_tokens)):
            try:
                download_request[header_tokens[index].strip()] = value_tokens[index].strip()
            except IndexError:
                pass
                
        return self._fixDownloadRequest(download_request)
    
        