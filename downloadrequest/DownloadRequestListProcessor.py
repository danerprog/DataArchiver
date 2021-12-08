from downloadrequest.DownloadRequestCsvFileManager import DownloadRequestCsvFileManager
from environment.Environment import Environment
from environment.Exceptions import UndefinedManagedDirectoryNameException
from utils.Logger import Logger

import os
from pathlib import Path
import yt_dlp


class DownloadRequestListProcessor:
    
    TEMPLATE_FILENAME = "%(title)s.%(ext)s"
    
    def __init__(self, args):
        self._logger = Logger.getLogger("DownloadRequestListProcessor")
        self._configuration = Environment.getEnvironment().configuration()
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
            self._move_downloaded_file_to_own_folder_if_necessary(args['filename'])
            
            if args['info_dict']['ext'] == 'mp4':
                self._logger.trace("archiving and resetting download request.")
                self._move_extra_downloaded_files_to_own_folder(args['info_dict']['infojson_filename'])
                
                if "was_downloaded" in self._current_download_request_for_processing:
                    download_request = self._get_current_download_request_with_important_info(args['info_dict'])
                    self._logger.debug("Archived download request: " + str(download_request))
                    self._successful_download_request_archiver.archiveDownloadRequest(download_request)
                    
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
      
    def _downloading_hook(self, args):
        if args['status'] == "downloading":
            self._logger.trace("downloading...")
            self._current_download_request_for_processing["was_downloaded"] = True
                
    def _move_downloaded_file_to_own_folder_if_necessary(self, filepath):
        self._logger.trace("_move_downloaded_file_to_own_folder_if_necessary called")
        video_id = self._current_download_request_for_processing["video_id"]
        if filepath.find(video_id) == -1:
            fixed_filepath = filepath.replace("\\\\", "\\")
            index_of_last_backslash = fixed_filepath.rfind("\\")
            directory_path = fixed_filepath[:index_of_last_backslash] + "\\" + video_id
            new_filepath = directory_path + "\\" + fixed_filepath[index_of_last_backslash:]
            
            self._logger.debug("Moving file. filepath: " + filepath + ", new_filepath: " + new_filepath + ", video_id: " + video_id)
            os.makedirs(directory_path, exist_ok = True)
            Path(filepath).rename(new_filepath)
            
    def _move_extra_downloaded_files_to_own_folder(self, infojson_filepath):
        self._move_downloaded_file_to_own_folder_if_necessary(infojson_filepath)
        self._move_downloaded_file_to_own_folder_if_necessary(infojson_filepath.replace(".info.json", ".description"))
        
    def _get_current_download_request_with_important_info(self, info_dictionary):
        download_request = self._current_download_request_for_processing
        download_request["video_title"] = info_dictionary['fulltitle'].replace(",", "")
        download_request["video_duration_in_seconds"] = str(info_dictionary['duration'])
        download_request["channel_name"] = info_dictionary['uploader']
        download_request["channel_id"] = info_dictionary['channel_id']
        return download_request

    def _process_download_request(self):
        full_directory = self._configuration.getRoot() + "\\" + self._configuration.getManagedDirectoryPath(self._managed_directory_name) + "\\" + self._current_download_request_for_processing["subdirectory"]
        
        if self._doesPathExist(full_directory):
            self._create_needed_directories(full_directory)
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
            
    def _doesPathExist(self, directory):
        return Path(directory).is_dir()
            
    def _begin_download_for_download_request(self, full_directory):
        download_request = self._current_download_request_for_processing
        ydl_options = {
            "outtmpl" : self._get_outtmpl(full_directory),
            "writeinfojson" : "true", 
            "writesubtitles" : "true",
            "writedescription" : "true",
            "getcomments" : download_request["get_comments"],
            "ratelimit" : self._configuration.getRateLimit(),
            "retries" : self._configuration.getNumberOfRetries(),
            "progress_hooks": [self._success_hook, self._failed_hook, self._downloading_hook],
        }
        
        download_url = download_request["url"]
        self._logger.info("Processing new download request. download_url: " + download_url + ", ydl_options: " + str(ydl_options))
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
        
    def _create_needed_directories(self, full_directory):
        download_request = self._current_download_request_for_processing
        directory_path_with_video_id = full_directory + "\\" + download_request['video_id']
        os.makedirs(directory_path_with_video_id, exist_ok = True)
        self._logger.debug("_create_needed_directories called. directory_path_with_video_id: " + directory_path_with_video_id)
        
    def _get_outtmpl(self, full_directory):
        video_id = self._current_download_request_for_processing['video_id']
        full_directory_path_with_video_id = full_directory + "\\" + video_id
        
        outtmpl = full_directory
        if len(os.listdir(full_directory_path_with_video_id)) > 0:
            outtmpl = outtmpl + "\\" + video_id
        outtmpl = outtmpl + "\\" + DownloadRequestListProcessor.TEMPLATE_FILENAME
        
        return outtmpl

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
            
    