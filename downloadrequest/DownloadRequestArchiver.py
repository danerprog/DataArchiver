from downloadrequest.DownloadRequestCsvFileManager import DownloadRequestCsvFileManager
from downloadrequest.DownloadRequestCsvFileManager import FailedDownloadRequestCsvFileManager
from downloadrequest.DownloadRequestCsvFileManager import SuccessfulDownloadRequestCsvFileManager
from environment.Environment import Environment

from datetime import date
from pathlib import Path

class DownloadRequestArchiver(object):

    def __init__(self, directory):
        self._environment = Environment.getEnvironment()
        self._directory =  self._environment.configuration().getWorkingDirectory() + "\\" + directory
        self._csv_file_manager = None
        self._date_since_last_opened_file = date.today()
        self._filename = ""
        
        self._createDirectoryIfItDoesNotExist()
        self._openCsvFileWhereDownloadRequestsWillBeArchived()
        
    def _createDirectoryIfItDoesNotExist(self):
        path = Path(self._directory)
        path.mkdir(parents=True, exist_ok=True)
              
    def _openCsvFileWhereDownloadRequestsWillBeArchived(self):
        filename = self._date_since_last_opened_file.strftime("%b-%d-%Y") + ".csv"
        
        if self._filename == "" or filename != self._csv_file_manager.getFilename():
            self._filename = filename
            self._csv_file_manager = self._get_csv_file_manager(self._directory + "\\" + filename)
            
    def _get_csv_file_manager(self, filepath):
        return DownloadRequestCsvFileManager(filepath)
        
    def archiveDownloadRequests(self, download_requests):
        for download_request in download_requests:
            self.archiveDownloadRequest(download_request)
    
    def archiveDownloadRequest(self, download_request):
        self._csv_file_manager.addDownloadRequest(download_request)
        

class FailedDownloadRequestArchiver(DownloadRequestArchiver):
    
    def _get_csv_file_manager(self, filepath):
        return FailedDownloadRequestCsvFileManager(filepath)
        
        
class SuccessfulDownloadRequestArchiver(DownloadRequestArchiver):
    
    def _get_csv_file_manager(self, filepath):
        return SuccessfulDownloadRequestCsvFileManager(filepath)