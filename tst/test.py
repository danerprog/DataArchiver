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
        
        

class BaseFixture(Validator):

    ROOT_TEST_ENVIRONMENT_DIRECTORY = "tst/testenv/"
    
    CONFIGURATION_FILENAME = "config.json"
    CONFIGURATION_FILEPATH = ROOT_TEST_ENVIRONMENT_DIRECTORY + CONFIGURATION_FILENAME
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setUpEnvironment()
    
    def setUp(self):
        self._archiver = YoutubeArchiver()
        
    def tearDown(self):
        self._archiver = None

    def archiver(self):
        return self._archiver
        
    def includeInDownloadRequest(self, video_id):
        self._download_request_file.write(video_id + ",default,\n")
         
    def download(self, youtube_video_id, subdirectory=""):
        self._archiver.download({
            "headers" : "video_id, managed_directory_name, subdirectory",
            "values" : youtube_video_id + ",," + subdirectory
        })
        
    def _setUpEnvironment(self):
        Environment.setEnvironment({
            'config_file' : BaseFixture.CONFIGURATION_FILEPATH
        })
        

class TestClass(BaseFixture):
  
    def test_downloadNonExistentVideo(self):
        video_id = "aaaa"
        self.download(video_id)
        self.assertThatFolderDoesNotExistInValidManagedDirectory(video_id, "default")
        
    def test_downloadExistingVideo(self):
        video_id = "WS7kSlv9uKk"
        self.download(video_id)
        self.assertThatFolderNamedUsingVideoIdExistsInManagedDirectory(video_id, "default")
        
    def test_downloadFailsIfManagedDirectoryNameDoesNotExist(self):
        video_id = "WS7kSlv9uKk"
        self.download(video_id)
        self.assertThatExceptionIsRaisedInInvalidManagedDirectory(video_id, "aaaaa")
        
    def test_downloadFailsIfSubdirectoryDoesNotExist(self):
        video_id = "WS7kSlv9uKk"
        subdirectory_to_use = "samplesubdirectory"
        self.download(video_id, subdirectory = subdirectory_to_use)
        self.assertThatSubdirectoriesDoNotExist(video_id, "default", subdirectory_to_use)

    
if __name__ == '__main__':
    unittest.main()
    
    
    