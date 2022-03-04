from downloadrequest.FailureReason import FailureReason
from environment.Environment import Environment
from utils.fileio.TextFileManager import TextFileManager
from utils.Logger import Logger


class DownloadSessionStatus:

    def __init__(self, download_request_filename, managed_directory_name):
        self._logger = Logger.getLogger("DownloadSessionStatus")
        self._initializeOutputFile(download_request_filename)
        self._managed_directory_name = managed_directory_name
        
        self._number_of_successful_downloads = 0
        self._number_of_failed_downloads_for_error = {
            "101" : 0,
            "102" : 0,
            "103" : 0,
            "104" : 0,
            "105" : 0
        }
        
    def incrementNumberOfSuccessfulDownloads(self, numberToAdd = 1):
        self._logger.debug("incrementNumberOfSuccessfulDownloads called. numberToAdd: " + str(numberToAdd))
        self._number_of_successful_downloads += numberToAdd
        
    def incrementNumberOfFailedDownloadsForError(self, error, numberToAdd = 1):
        self._logger.debug("incrementNumberOfFailedDownloadsForError called. numberToAdd: " + str(numberToAdd))
        self._number_of_failed_downloads_for_error[str(error)] += numberToAdd
        
    def getNumberOfSuccessfulDownloads(self):
        self._logger.trace("getNumberOfSuccessfulDownloads called")
        return self._number_of_successful_downloads
        
    def getNumberOfFailedDownloadsForError(self, error_code):
        self._logger.debug("getNumberOfFailedDownloadsForError called. error_code: " + str(error_code))
        return self._number_of_failed_downloads_for_error[str(error_code)]
        
    def generateStatusReport(self):
        self._logger.trace("generateStatusReport called")
        self._output_file.writeLine("Managed Directory Name: " + self._managed_directory_name)
        self._output_file.writeLine("    # of successful downloads: " + str(self.getNumberOfSuccessfulDownloads()))
        self._output_file.writeLine("    # of failed downloads: " + str(self._getTotalNumberOfFailedDownloads()))
        self._printReportForFailedDownloadsForErrorIfNeeded("101")
        self._printReportForFailedDownloadsForErrorIfNeeded("102")
        self._printReportForFailedDownloadsForErrorIfNeeded("103")
        self._printReportForFailedDownloadsForErrorIfNeeded("104")
        self._printReportForFailedDownloadsForErrorIfNeeded("105")
        self._output_file.writeLine("")
        self._output_file.writeLine("")
        
    def _getTotalNumberOfFailedDownloads(self):
        self._logger.trace("_getTotalNumberOfFailedDownloads called")
        total_number_of_failed_downloads = 0
    
        for k, v in self._number_of_failed_downloads_for_error.items():
            total_number_of_failed_downloads += v
            
        return total_number_of_failed_downloads
        
    def _getReportForFailedDownloadsForError(self, error_code):
        self._logger.debug("_getReportForFailedDownloadsForError called. error_code: " + str(error_code))
        
        return "        [" + str(error_code) + "] " + FailureReason.YOUTUBE_ARCHIVER[error_code] + ": " + str(self.getNumberOfFailedDownloadsForError(error_code))
        
    def _printReportForFailedDownloadsForErrorIfNeeded(self, error_code):
        self._logger.debug("_printReportForFailedDownloadsForErrorIfNeeded called. error_code: " + str(error_code))
        
        if self._number_of_failed_downloads_for_error[error_code] > 0:
            self._output_file.writeLine(self._getReportForFailedDownloadsForError(error_code))
            
    def _initializeOutputFile(self, download_request_filename):
        self._logger.trace("_initializeOutputFile called")
        configuration = Environment.getEnvironment().configuration()
        full_file_path = configuration.getWorkingDirectory() + "\\" + download_request_filename + "_status.txt"
        self._file_manager = TextFileManager(full_file_path, "a+")
        self._output_file = self._file_manager.getFile()