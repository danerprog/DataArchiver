from archivers.YoutubeArchiver import YoutubeArchiver

import getopt

class ConsoleInterface:

    def __init__(self):
        self._youtubeArchiver = YoutubeArchiver()
        
    def _extractOptionsAndArguments(self, command, possible_options):
        options = []
        arguments = []
        
        try:
            options, arguments = getopt.getopt(command.split(), "", possible_options)
        except getopt.GetoptError as e:
            pass

        return options, arguments

    def _displayMenu(self) :
        print("################## Data Archiver - Alpha v1.0.0 #################")
        print("Automatically archives and manages your scraped data")
        print()
        print("########################### Archivers ###########################")
        print("YoutubeArchiver: Archive batches of youtube videos. Usage --youtube_archiver <download_request_file>")
        
        print()
        print()

    def runYoutubeArchiver(self, options):
        print()
        print(">>>>>> Running Youtube Archiver...")
        numberOfDownloadRequestsFound = self._runYoutubeArchiverUsingOptions(options)
        print(">>>>>> Archiving complete.")
        print(">>>>>> Number of download requests found: " + str(numberOfDownloadRequestsFound))
        
        
    def _runYoutubeArchiverUsingOptions(self, options_string):
        numberOfDownloadRequestsFound = 0
        headers = None
        values = None
        options, arguments = self._extractOptionsAndArguments(options_string, ["filename=", "headers=", "values="])
        
        for option, value in options:
            if option == "--filename":
                if headers is None and values is None:
                    numberOfDownloadRequestsFound = self._youtubeArchiver.download({
                        "filename" : value
                    })
                    print(">>>>>> File processed: " + value)
                else:
                    print(">>> Tried to combine filename option with headers and values. Aborting.")
            elif option == "--headers":
                headers = value
                if values is not None:
                    self._runYoutubeArchiverUsingHeadersAndValues(headers, values)
            elif option == "--values":
                values = value
                if headers is not None:
                    self._runYoutubeArchiverUsingHeadersAndValues(headers, values)
                    
        if headers is None and values is not None:
            print(">>>>>> Missing value for option --headers")
        elif headers is not None and values is None:
            print(">>>>>> Missing value for option --values")
    
    def _runYoutubeArchiverUsingHeadersAndValues(self, headers, values):
        return self._youtubeArchiver.download({
            "headers" : headers,
            "values" : values
        })
  
    def start() :
        while True:
            self._displayMenu()
            command = input("Command: ")
            options, arguments = self._extractOptionsAndArguments(command, ["youtube_archiver=","quit"])
            
            if len(options) > 0:
                option, value = options[0]
                
                if option == "--youtube_archiver" :
                    self.runYoutubeArchiver(value)
                elif option == "--quit" :
                    break
                    
            print()
            print()