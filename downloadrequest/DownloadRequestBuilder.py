from downloadrequest.DownloadRequestJsonFileManager import DownloadRequestJsonFileManager
from downloadrequest.DownloadRequestCsvFileManager import DownloadRequestCsvFileManager

class DownloadRequestBuilder(object) :
    
    def __init__(self, filename) :
        self._filename = filename
        self._download_request_file_manager = None
        self._download_requests = {}
        
        self._buildDownloadRequests()
        
    def _buildDownloadRequests(self) :
        self._constructDownloadRequestFileManager()
        self._fixAndRearrangeDownloadRequestsAccordingToRootDirectory()
        
    def _constructDownloadRequestFileManager(self):
        file_extension = self._filename.split(sep=".")[-1]
        
        if file_extension == "json" :
            self._download_request_file_manager = DownloadRequestJsonFileManager(self._filename)
        elif file_extension == "csv" :
            self._download_request_file_manager = DownloadRequestCsvFileManager(self._filename)
        else : 
            print("ERR: file extension " + file_extension + " is not supported!")

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