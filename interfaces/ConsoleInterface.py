from archivers.YoutubeArchiver import YoutubeArchiver

class ConsoleInterface:

    def __init__(self):
        self._youtubeArchiver = YoutubeArchiver()
        
    def _extractOptionsAndArguments(command):
        options = []
        arguments = []
        
        try:
            options, arguments = getopt.getopt(command.split(),"",["youtube_archiver=","quit"])
        except getopt.GetoptError as e:
            pass
    
        return options, arguments

    def _displayMenu() :
        print("################## Data Archiver - Alpha v1.0.0 #################")
        print("Automatically archives and manages your scraped data")
        print()
        print("########################### Archivers ###########################")
        print("YoutubeArchiver: Archive batches of youtube videos. Usage --youtube_archiver <download_request_file>")
        
        print()
        print()
        
    def runYoutubeArchiver(self, filename):
        print()
        print(">>>>>> Running Youtube Archiver...")
        numberOfDownloadRequestsFound = self._youtubeArchiver.download(filename)
        print(">>>>>> Archiving complete.")
        print(">>>>>> File processed: " + filename)
        print(">>>>>> Number of download requests found: " + str(numberOfDownloadRequestsFound))
  
    def start() :
        while True:
            self._displayMenu()
            command = input("Command: ")
            options, arguments = self._extractOptionsAndArguments(command)
            
            if len(options) > 0:
                option, value = options[0]
                
                if option == "--youtube_archiver" :
                    self.runYoutubeArchiver(value)
                elif option == "--quit" :
                    break
                    
            print()
            print()