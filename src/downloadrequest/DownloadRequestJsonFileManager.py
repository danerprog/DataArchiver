from utils.fileio.JsonFileReader import JsonFileReader

class DownloadRequestJsonFileManager(object) :

    _original_json_file = None
    _acceptable_download_requests = []
    _number_of_download_requests_found = 0

    def __init__(self, filename):
        self._original_json_file = self.JsonFileReader(filename).read()
        self._getAcceptableDownloadRequestsFromJsonFile()
        
    def _getAcceptableDownloadRequestsFromJsonFile(self): 
        for download_request in self._original_json_file:
            self._number_of_download_requests_found += 1
            self._printWarningMessageIfRequiredKeysAreNotPresentElseAddToAcceptableDownloadRequests(download_request)
            
    def _printWarningMessageIfRequiredKeysAreNotPresentElseAddToAcceptableDownloadRequests(self, download_request):
        if "url" not in download_request:
            print("WRN: index " + str(self._number_of_download_requests_found) + " has no key 'url'!")
        else:
            self._acceptable_download_requests.append(download_request)
            
    def getAcceptableDownloadRequests(self):
        return self._acceptable_download_requests
        