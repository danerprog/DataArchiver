import os
import sys

absolutePath = os.path.abspath(__file__)
currentDirectoryName = os.path.dirname(__file__)
currentDirectoryStringIndex = absolutePath.rfind(currentDirectoryName)
parentDirectoryPath = absolutePath[:currentDirectoryStringIndex]
sys.path.append(parentDirectoryPath + "src")


from archivers.YoutubeArchiver import YoutubeArchiver
from environment.Environment import Environment

import glob
import unittest

class Validator(unittest.TestCase):
  
    def assertThatFolderExistsInManagedDirectory(self, folder_name, managed_directory_name):
        configuration = Environment.getEnvironment().configuration()
        managed_directory_path = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name)
        self.assertTrue(os.path.isdir(managed_directory_path + "/" + folder_name))
        
    def assertThatFolderDoesNotExistInManagedDirectory(self, folder_name, managed_directory_name):
        configuration = Environment.getEnvironment().configuration()
        managed_directory_path = configuration.getRoot() + "/" + configuration.getManagedDirectoryPath(managed_directory_name)
        self.assertFalse(os.path.isdir(managed_directory_path + "/" + folder_name))
        
        

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
         
    def download(self, youtube_video_id):
        self._archiver.download({
            "headers" : "video_id, managed_directory_name, subdirectory",
            "values" : youtube_video_id + ",,"
        })
        
    def _setUpEnvironment(self):
        Environment.setEnvironment({
            'config_file' : BaseFixture.CONFIGURATION_FILEPATH
        })
        
 

class TestClass(BaseFixture):
  
    def test_downloadNonExistentVideo(self):
        video_id = "aaaa"
        self.download(video_id)
        self.assertThatFolderDoesNotExistInManagedDirectory(video_id, "default")
        
    def test_downloadExistingVideo(self):
        video_id = "WS7kSlv9uKk"
        self.download(video_id)
        self.assertThatFolderExistsInManagedDirectory(video_id, "default")
        
    
if __name__ == '__main__':
    unittest.main()
    
    
    