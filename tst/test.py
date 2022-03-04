import os
import sys

absolutePath = os.path.abspath(__file__)
currentDirectoryName = os.path.dirname(__file__)
currentDirectoryStringIndex = absolutePath.rfind(currentDirectoryName)
parentDirectoryPath = absolutePath[:currentDirectoryStringIndex]
sys.path.append(parentDirectoryPath + "src")


from archivers.YoutubeArchiver import YoutubeArchiver
from environment.Environment import Environment
from environment.Exceptions import UndefinedManagedDirectoryNameException

import glob
import shutil
import unittest

class Validator(unittest.TestCase):
  
    def assertThatFolderNamedUsingVideoIdExistsInManagedDirectory(self, folder_name, managed_directory_name):
        configuration = Environment.getEnvironment().configuration()
        managed_directory_path = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name)
        self.assertTrue(os.path.isdir(managed_directory_path + "/" + folder_name))
        
    def assertThatFolderDoesNotExistInValidManagedDirectory(self, folder_name, managed_directory_name):
        configuration = Environment.getEnvironment().configuration()
        managed_directory_path = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name)
        self.assertFalse(os.path.isdir(managed_directory_path + "/" + folder_name))
        
    def assertThatExceptionIsRaisedInInvalidManagedDirectory(self, folder_name, managed_directory_name):
        configuration = Environment.getEnvironment().configuration()
        with self.assertRaises(UndefinedManagedDirectoryNameException):
            managed_directory_path = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name)
            
    def assertThatSubdirectoriesDoNotExist(self, folder_name, managed_directory_name, subdirectory_path):
        configuration = Environment.getEnvironment().configuration()
        managed_directory_path = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name)
        self.assertTrue(os.path.isdir(managed_directory_path))
        self.assertFalse(os.path.isdir(managed_directory_path + "/" + subdirectory_path))
        
    def assertThatDownloadedFilesExist(self, folder_name, managed_directory_name):
        configuration = Environment.getEnvironment().configuration()
        path_to_check = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name) + "/" + folder_name
        file_extensions_to_check = [".description", ".info.json", ".mp4"]
        
        for filename in os.listdir(path_to_check):
            filename_tokens = filename.split(".", maxsplit = 2)
            extension = filename_tokens[-1]
            for index in range(len(file_extensions_to_check) - 1, -1, -1):
                if extension == file_extensions_to_check[index]:
                    file_extensions_to_check.pop(index)
                    
        print("file_extensions_to_check: " + str(file_extensions_to_check))
        self.assertTrue(len(file_extensions_to_check), 0)
        
    def assertThatSubtitleFilesExist(self, folder_name, managed_directory_name, languages):
        configuration = Environment.getEnvironment().configuration()
        path_to_check = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name) + "/" + folder_name
        file_extensions_to_check = self._buildSubtitleFileExtensionsToCheck(languages)
        
        for filename in os.listdir(path_to_check):
            filename_tokens = filename.split(".", maxsplit = 2)
            extension = filename_tokens[-1]
            for index in range(len(file_extensions_to_check) - 1, -1, -1):
                if extension == file_extensions_to_check[index]:
                    file_extensions_to_check.pop(index)
                    
        print("file_extensions_to_check: " + str(file_extensions_to_check))
        self.assertTrue(len(file_extensions_to_check), 0)
        
    def assertThatFileInWorkingDirectoryExists(self, filename):
        configuration = Environment.getEnvironment().configuration()
        path_to_check = configuration.getWorkingDirectory() + "/" + filename
        print("path_to_check: " + str(path_to_check))
        self.assertTrue(os.path.isfile(path_to_check))
        
    def _buildSubtitleFileExtensionsToCheck(self, languages):
        completed_subtitle_file_extensions = []
        
        for language in languages:
            completed_subtitle_file_extensions.append("." + language + ".vtt")

        return completed_subtitle_file_extensions
        

class BaseFixture(Validator):

    ROOT_TEST_ENVIRONMENT_DIRECTORY = "tst/testenv/"
    
    CONFIGURATION_FILENAME = "config.json"
    CONFIGURATION_FILEPATH = ROOT_TEST_ENVIRONMENT_DIRECTORY + CONFIGURATION_FILENAME
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setUpEnvironment()
        self._cleanWorkingDirectory()
    
    def setUp(self):
        self._archiver = YoutubeArchiver()
        
    def tearDown(self):
        self._archiver = None
        self._cleanManagedDirectories()

    def archiver(self):
        return self._archiver
        
    def includeInDownloadRequest(self, video_id):
        self._download_request_file.write(video_id + ",default,\n")
         
    def download(self, youtube_video_id, subdirectory=""):
        self._archiver.download({
            "headers" : "video_id, managed_directory_name, subdirectory",
            "values" : youtube_video_id + ",," + subdirectory
        })
        
    def downloadFile(self, filename):
        self._archiver.download({
            "filename" : BaseFixture.ROOT_TEST_ENVIRONMENT_DIRECTORY + filename + ".csv"
        })
        
    def _setUpEnvironment(self):
        Environment.setEnvironment({
            'config_file' : BaseFixture.CONFIGURATION_FILEPATH
        })
        
    def _cleanManagedDirectories(self):
        configuration = Environment.getEnvironment().configuration()
        managed_directory_names = configuration.getManagedDirectoryNames()
        for managed_directory_name, managed_directory_folder in managed_directory_names:
            directory_path = configuration.getRoot() + "/" + managed_directory_folder
            self._cleanDirectory(directory_path)

    def _cleanWorkingDirectory(self):
        configuration = Environment.getEnvironment().configuration()
        self._cleanDirectory(configuration.getWorkingDirectory())
        
    def _cleanDirectory(self, directory_path):
        shutil.rmtree(directory_path, ignore_errors = True)
        os.makedirs(directory_path, exist_ok = True)
        

class TestClass(BaseFixture):   

    def test_downloadNonExistentVideo(self):
        video_id = "aaaa"
        self.download(video_id)
        self.assertThatFolderDoesNotExistInValidManagedDirectory(video_id, "default")
        
    def test_downloadExistingVideo(self):
        video_id = "WS7kSlv9uKk"
        self.download(video_id)
        self.assertThatFolderNamedUsingVideoIdExistsInManagedDirectory(video_id, "default")
        self.assertThatDownloadedFilesExist(video_id, "default")
        
    def test_downloadFailsIfManagedDirectoryNameDoesNotExist(self):
        video_id = "WS7kSlv9uKk"
        self.download(video_id)
        self.assertThatExceptionIsRaisedInInvalidManagedDirectory(video_id, "aaaaa")
        
    def test_downloadFailsIfSubdirectoryDoesNotExist(self):
        video_id = "WS7kSlv9uKk"
        subdirectory_to_use = "samplesubdirectory"
        self.download(video_id, subdirectory = subdirectory_to_use)
        self.assertThatSubdirectoriesDoNotExist(video_id, "default", subdirectory_to_use)
        
    def test_downloadVideoWithSubtitles(self):
        video_id = "0Rbz_PZOZ54"
        self.download(video_id)
        self.assertThatDownloadedFilesExist(video_id, "default")
        self.assertThatSubtitleFilesExist(video_id, "default", ["en-US"])
        
    def test_downloadVideoWithCommnets(self):
        video_id = "ZMndxzfj5Js"
        self.download(video_id)
        self.assertThatDownloadedFilesExist(video_id, "default")

    def test_downloadingFileWillGenerateDownloadStatus(self):
        filename = "1successful1failingdownloadrequest"
        self.downloadFile(filename)
        self.assertThatFileInWorkingDirectoryExists(filename + "_status.txt")
      
    def test_downloadFileWithInvalidCharactersInUrl(self):
        video_id = "https://www.youtube.com/watch?v=WS7kSlv9uKk"
        self.download(video_id)
        self.assertThatFolderDoesNotExistInValidManagedDirectory("WS7kSlv9uKk", "default")
        

if __name__ == '__main__':
    unittest.main()
    
    
    