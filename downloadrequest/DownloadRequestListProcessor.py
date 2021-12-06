from downloadrequest.DownloadRequestCsvFileManager import DownloadRequestCsvFileManager
from environment.Environment import Environment
from environment.Environment import UndefinedManagedDirectoryNameException
from utils.Logger import Logger

from pathlib import Path
import yt_dlp


class DownloadRequestListProcessor:
    
    TEMPLATE_FILENAME = "%(title)s.%(ext)s"
    
    def __init__(self, args):
        self._logger = Logger.getLogger("DownloadRequestListProcessor")
        self._environment_manager = Environment.getEnvironment()
        self._successful_download_request_archiver = args['successful_download_request_archiver']
        self._failed_download_request_archiver = args['failed_download_request_archiver']
        self._managed_directory_name = args['managed_directory_name']
        self._download_request_list = args['download_request_list']
        self._download_request_filename = args['download_request_filename'].replace(".", "_unprocessed.")
        self._reset_current_download_request()
        
    def __del__(self):
        self._logger.trace("__del__ called")
        self.save_unprocessed_download_requests_to_file()
   
    def _success_hook(self, args):
        if args['status'] == 'finished':
            self._logger.info("Download finished. args['filename']: " + args['filename'])
            if args['info_dict']['ext'] == 'mp4':
                self._logger.trace("archiving and reseting download request.")
                self._successful_download_request_archiver.archiveDownloadRequest(self._current_download_request_for_processing)
                self._reset_current_download_request()
            else:
                self._logger.trace("skipping archiving process.")

    def _failed_hook(self, args):
        if args['status'] == "error":
            failure_reason = "Download failed. args['filename']: " + args['filename']
            self._logger.info(failure_reason)
            
            if args['info_dict']['ext'] == 'mp4':
                self._logger.trace("archiving and reseting download request.")
                self._process_failed_download(failure_reason)
            else:
                self._logger.trace("skipping archiving process.")
   
    def _process_download_request(self):
        full_directory = self._environment_manager.getRoot() + "\\" + self._environment_manager.getManagedDirectoryPath(self._managed_directory_name) + "\\" + self._current_download_request_for_processing["subdirectory"]
        
        if self._doesPathExist(full_directory):
            self._begin_download_for_download_request(full_directory)
        else:
            failure_reason = "Path does not exist. Stopping download. full_directory: " + full_directory + ", download_url: " + self._current_download_request_for_processing["url"]
            self._logger.warning(failure_reason)
            self._process_failed_download(failure_reason)
            
    def _try_to_process_download_request(self):
        try:
            self._process_download_request()
        except yt_dlp.utils.DownloadError as e:
            failure_reason = str(e).replace("\n", ". ")
            self._logger.info("DownloadError caught. failure_reason: " + failure_reason)
            self._process_failed_download(failure_reason)
        except UndefinedManagedDirectoryNameException as e:
            message = "UndefinedManagedDirectoryNameException caught. managed_directory_name: " + str(e)
            self._logger.info(message)
            self._process_failed_download(message)

    def _doesPathExist(self, directory):
        return Path(directory).is_dir()
            
    def _begin_download_for_download_request(self, full_directory):
        download_request = self._current_download_request_for_processing
        ydl_options = {
            "outtmpl" : full_directory + "\\" + DownloadRequestListProcessor.TEMPLATE_FILENAME,
            "writeinfojson" : "true", 
            "writesubtitles" : "true",
            "writedescription" : "true",
            "get_comments" : download_request["get_comments"],
            "ratelimit" : 480000,
            "retries" : 3,
            "progress_hooks": [self._success_hook, self._failed_hook],
        }
        
        download_url = download_request["url"]
        self._logger.info("Processing new download request. download_url: " + download_url + "ydl_options: " + str(ydl_options))
        ydl = yt_dlp.YoutubeDL(ydl_options)
        ydl.download([download_url])
        
    def _process_failed_download(self, failure_reason):
        failed_download_request = self._current_download_request_for_processing
        failed_download_request["failure_reason"] = failure_reason
        self._failed_download_request_archiver.archiveDownloadRequest(self._current_download_request_for_processing)
        self._reset_current_download_request()
        
    def _save_download_request_to_file(self, download_request, file_manager):
        file_manager.addDownloadRequest(download_request)
        message = "Saving download request: " + str(download_request)
        self._logger.info(message)
        
    def _reset_current_download_request(self):
        self._current_download_request_for_processing = None

    def run(self):
        while len(self._download_request_list) > 0:
            self._current_download_request_for_processing = self._download_request_list.pop(0)
            self._logger.debug("queue: "  + str(self._current_download_request_for_processing))
            self._try_to_process_download_request()
            
    def save_unprocessed_download_requests_to_file(self):
        self._logger.trace("save_unprocessed_download_requests_to_file called")
        download_request_csv_file_manager = DownloadRequestCsvFileManager(self._download_request_filename)
        
        if self._current_download_request_for_processing is not None:
            self._save_download_request_to_file(self._current_download_request_for_processing, download_request_csv_file_manager)
        
        while len(self._download_request_list) > 0:
            self._save_download_request_to_file(self._download_request_list.pop(0), download_request_csv_file_manager)
            
    