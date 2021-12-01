from downloadrequest.DownloadRequestBuilder import DownloadRequestBuilder
from downloadrequest.DownloadRequestListProcessor import DownloadRequestListProcessor
from environment.Environment import Environment
from utils.Logger import Logger

  
class YoutubeArchiver(object):

    TEMPLATE_FILENAME = "%(title)s.%(ext)s"
    
    def __init__(self, args):
        self._logger = Logger.getLogger("YoutubeDownloader")
        self._successful_download_request_archiver = args['successful_download_request_archiver']
        self._failed_download_request_archiver = args['failed_download_request_archiver']
        self._download_request_list_processors = []
        
    def _create_download_request_list_processors(self, download_request_file, download_requests):
        self._logger.trace("_create_download_request_list_processors called")
        for (managed_directory_name, download_request_list) in download_requests.items():
            args = {
                'successful_download_request_archiver' : self._successful_download_request_archiver,
                'failed_download_request_archiver' : self._failed_download_request_archiver,
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
        
    def download(self, download_request_file):
        self._logger.trace("download called")
        download_requests = DownloadRequestBuilder(download_request_file).getDownloadRequests()
        self._create_download_request_list_processors(download_request_file, download_requests)
        self._run_download_request_lists()

