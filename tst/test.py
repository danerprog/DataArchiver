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

class BaseFixture(unittest.TestCase):

    ROOT_TEST_ENVIRONMENT_DIRECTORY = "tst/testenv/"
    
    DOWNLOAD_REQUEST_FILENAME = "dr.csv"
    DOWNLOAD_REQUEST_FILEPATH = ROOT_TEST_ENVIRONMENT_DIRECTORY + DOWNLOAD_REQUEST_FILENAME
    
    CONFIGURATION_FILENAME = "config.json"
    CONFIGURATION_FILEPATH = ROOT_TEST_ENVIRONMENT_DIRECTORY + CONFIGURATION_FILENAME
    
    
    def setUp(self):
        self._setUpEnvironment()
        self._setUpDownloadRequestFile()
        self._archiver = YoutubeArchiver()
        
    def tearDown(self):
        self._tearDownDownloadRequestFile()
        self._archiver = None

    def archiver(self):
        return self._archiver
        
    def includeInDownloadRequest(self, video_id):
        self._download_request_file.write(video_id + ",default,\n")
        
    def startDownload(self):
        self.archiver().download(BaseFixture.DOWNLOAD_REQUEST_FILEPATH)
        
    def _setUpEnvironment(self):
        Environment.setEnvironment({
            'config_file' : BaseFixture.CONFIGURATION_FILEPATH
        })
     
    def _setUpDownloadRequestFile(self):
        self._download_request_file = open(BaseFixture.DOWNLOAD_REQUEST_FILEPATH, "w")
        self._download_request_file.write("video_id, managed_directory_name, subdirectory\n")
        
    def _tearDownDownloadRequestFile(self):
        self._download_request_file.close()
        #os.remove(BaseFixture.DOWNLOAD_REQUEST_FILEPATH)
  

class TestClass(BaseFixture):
  
    def test_downloadNonExistentVideo(self):
        self.includeInDownloadRequest("aaaa")
        self.startDownload()
        pass
        
    def test_downloadExistingVideo(self):
        self.includeInDownloadRequest("WS7kSlv9uKk")
        self.startDownload()
        
    
if __name__ == '__main__':
    unittest.main()
    
    
    