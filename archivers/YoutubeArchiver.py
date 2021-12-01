from downloadrequest.DownloadRequestBuilder import DownloadRequestBuilder
from environment.Environment import Environment
from utils.Logger import Logger

from pathlib import Path
import youtube_dl

  
class YoutubeArchiver(object):

    TEMPLATE_FILENAME = "%(title)s.%(ext)s"
    
    def __init__(self, args):
        self._logger = Logger.getLogger("YoutubeDownloader")
        self._environment_manager = Environment.getEnvironment()
        self._successful_download_request_archiver = args['successful_download_request_archiver']
        self._failed_download_request_archiver = args['failed_download_request_archiver']
        self._current_download_request = {}
        
    def _success_hook(self, args):
        if args['status'] == 'finished':
            self._logger.info("Download finished. args['filename']: " + args['filename'])
            self._successful_download_request_archiver.archiveDownloadRequest(self._current_download_request)
            print(args)

    def _failed_hook(self, args):
        if args['status'] == "error":
            failure_reason = "Download failed. args['filename']: " + args['filename']
            self._logger.info(failure_reason)
            self._process_failed_download(failure_reason)

            
    def _process_download_request_array(self, managed_directory_name, download_request_array):
        for download_request in download_request_array:
            self._try_to_process_download_request(managed_directory_name, download_request)
                
    def _process_download_request(self, managed_directory_name, download_request):
        self._current_download_request = download_request
        full_directory = self._environment_manager.getRoot() + "\\" + self._environment_manager.getManagedDirectoryPath(managed_directory_name) + "\\" + download_request["subdirectory"]
        
        if self._doesPathExist(full_directory):
            self._begin_download_for_download_request(download_request, full_directory)
        else:
            self._logger.warning("Path does not exist. Stopping download. full_directory: " + full_directory + ", download_url: " + download_request["url"])
            self._failed_download_request_archiver.archiveDownloadRequest(download_request)
            
    def _try_to_process_download_request(self, managed_directory_name, download_request):
        try:
            self._process_download_request(managed_directory_name, download_request)
        except youtube_dl.utils.DownloadError as e:
            failure_reason = str(e).replace("\n", ". ")
            self._logger.info("DownloadError caught. failure_reason: " + failure_reason)
            self._process_failed_download(failure_reason)
        except KeyError as e:
            failure_reason = "KeyError caught. Possible malformed csv entry. "
            self._logger.info(failure_reason + "download_request: " + str(download_request))
            self._process_failed_download(failure_reason)

    def _doesPathExist(self, directory):
        return Path(directory).is_dir()
            
    def _begin_download_for_download_request(self, download_request, full_directory):
        ydl_options = {
            "outtmpl" : full_directory + "\\" + YoutubeArchiver.TEMPLATE_FILENAME,
            "writeinfojson" : "true", 
            "writesubtitles" : "true",
            "ratelimit" : 480000,
            "retries" : 3,
            "progress_hooks": [self._success_hook, self._failed_hook],
        }
        
        self._logger.info("Processing new download request. download_url: " + download_url + "ydl_options: " + str(ydl_options))
        ydl = youtube_dl.YoutubeDL(ydl_options)
        ydl.download([download_request["url"]])
        
    def _process_failed_download(self, failure_reason):
        failed_download_request = self._current_download_request
        failed_download_request["failure_reason"] = failure_reason
        self._failed_download_request_archiver.archiveDownloadRequest(self._current_download_request)

    def download(self, download_request_file):
        download_requests = DownloadRequestBuilder(download_request_file).getDownloadRequests()

        for (managed_directory_name, download_request_array) in download_requests.items():
            self._process_download_request_array(managed_directory_name, download_request_array)




