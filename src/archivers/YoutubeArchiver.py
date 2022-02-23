from downloadrequest.DownloadRequestArchiver import FailedDownloadRequestArchiver
from downloadrequest.DownloadRequestArchiver import SuccessfulDownloadRequestArchiver
from downloadrequest.DownloadRequestBuilder import FileDownloadRequestBuilder
from downloadrequest.DownloadRequestBuilder import SingleDownloadRequestBuilder
from downloadrequest.DownloadRequestListProcessor import DownloadRequestListProcessor
from utils.Logger import Logger


class YoutubeArchiver(object):

    TEMPLATE_FILENAME = "%(title)s.%(ext)s"
    
    def __init__(self):
        self._logger = Logger.getLogger("YoutubeArchiver")
        self._download_request_list_processors = []
        
    def _create_download_request_list_processors(self, download_request_file, download_requests):
        self._logger.trace("_create_download_request_list_processors called")
        for (managed_directory_name, download_request_list) in download_requests.items():
            args = {
                'successful_download_request_archiver' : SuccessfulDownloadRequestArchiver("successful_downloads"),
                'failed_download_request_archiver' : FailedDownloadRequestArchiver("failed_downloads"),
                'managed_directory_name' : managed_directory_name,
                'download_request_list' : download_request_list,
                'download_request_filename' : download_request_file
            }
            self._download_request_list_processors.append(DownloadRequestListProcessor(args))
            
    def _run_download_request_lists(self):
        self._logger.trace("_run_download_request_lists called")
        for download_request_list_processor in self._download_request_list_processors:
            try:
                self._logger.trace("running download request list.")
                download_request_list_processor.run()
            except KeyboardInterrupt as e:
                self._logger.info("KeyboardInterrupt exception caught. Initiating shutdown procedure.")
                download_request_list_processor.save_unprocessed_download_requests_to_file()
                self._trigger_list_processors_to_save_remaining_download_requests()
                break
                
    def _trigger_list_processors_to_save_remaining_download_requests(self):
        self._logger.trace("_trigger_list_processors_to_save_remaining_download_requests called")
        self._download_request_list_processors = None
        
    def _downloadUsingFilename(self, filename):
        self._logger.trace("_downloadUsingFilename called")
        download_requests = FileDownloadRequestBuilder(filename).getDownloadRequests()
        self._create_download_request_list_processors(filename, download_requests)
        self._run_download_request_lists()
        return len(download_requests)
        
    def _downloadUsingHeadersAndValues(self, headers, values):
        self._logger.trace("_downloadUsingHeadersAndValues called")
        download_requests = SingleDownloadRequestBuilder(headers, values).getDownloadRequests()
        self._create_download_request_list_processors("header_and_value_request", download_requests)
        self._run_download_request_lists()
        return len(download_requests)
    
    def download(self, args):
        self._logger.trace("download called")
        number_of_download_requests = 0
        if "filename" in args:
            number_of_download_requests = self._downloadUsingFilename(args["filename"])
        elif "headers" in args and "values" in args:
            number_of_download_requests = self._downloadUsingHeadersAndValues(args["headers"], args["values"])

        return number_of_download_requests
        
    
