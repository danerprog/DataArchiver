from archivers.YoutubeArchiver import YoutubeArchiver

import getopt

class ConsoleInterface:

    def __init__(self):
        self._youtube_archiver = YoutubeArchiver()
        self._should_program_continue = True
        
    def _extractOptionAndValuePairs(self, options):
        option_value_pairs = {}

        for option, value in options:
            option_value_pairs[option.strip('-')] = value
            
        return option_value_pairs
        
    def _extractOptionsAndArguments(self, command, possible_options):
        options = []
        arguments = []
        
        try:
            options, arguments = getopt.getopt(command.split(), "", possible_options)
        except getopt.GetoptError as e:
            pass

        return options, arguments

    def _displayMenu(self) :
        print("################## Data Archiver - Alpha v1.2.11 #################")
        print("Automatically archives and manages your scraped data")
        print()
        print("########################### Archivers ###########################")
        print("YoutubeArchiver: Archive batches of youtube videos.")
        
        print()
        print()
        
    def runYoutubeArchiver(self, option_value_pairs):
        print()
        print(">>>>>> Running Youtube Archiver...")
        numberOfDownloadRequestsFound = self._youtube_archiver.run(option_value_pairs)
        print(">>>>>> Archiving complete.")
        print(">>>>>> Number of download requests found: " + str(numberOfDownloadRequestsFound))
        
    def runApprorpiateArchiver(self, option_value_pairs):
        if "youtube_archiver" in option_value_pairs:
            self.runYoutubeArchiver(option_value_pairs)
        else:
            print("No appropriate archiver found.")
  
    def start(self) :
        while self._should_program_continue:
            self._displayMenu()
            command = input("Command: ")
            options, arguments = self._extractOptionsAndArguments(command, [
                "quit",
                "youtube_archiver",
                
                "filename=",
                "headers=",
                "values="])
            option_value_pairs = self._extractOptionAndValuePairs(options)
            self._should_program_continue = "quit" not in option_value_pairs
            
            if self._should_program_continue:
                self.runApprorpiateArchiver(option_value_pairs)
            
         