from environment.Environment import Environment
from downloadrequest.DownloadRequestArchiver import DownloadRequestArchiver
from downloadrequest.DownloadRequestArchiver import FailedDownloadRequestArchiver
from archivers.YoutubeArchiver import YoutubeArchiver

import getopt
import sys

def extract_options_and_arguments(command):
    options = []
    arguments = []
    
    try:
        options, arguments = getopt.getopt(command.split(),"",["youtube_archiver=","quit"])
    except getopt.GetoptError as e:
        pass
    
    return options, arguments

def display_menu() :
    print("################## Data Archiver - Alpha v0.1.0 #################")
    print("Automatically archives and manages your scraped data")
    print()
    print("########################### Archivers ###########################")
    print("YoutubeArchiver: Archive batches of youtube videos. Usage --youtube_archiver <download_request_file>")
    
    print()
    print()

def run(config_file) :
    Environment.setEnvironment({
        "config_file" : config_file
    })
    youtube_archiver = YoutubeArchiver({
        "successful_download_request_archiver" : DownloadRequestArchiver("successful_downloads"),
        "failed_download_request_archiver" : FailedDownloadRequestArchiver("failed_downloads")
    })

    while True:
        display_menu()
        command = input("Command: ")
        options, arguments = extract_options_and_arguments(command)
        
        if len(options) > 0:
            option, value = options[0]
            
            if option == "--youtube_archiver" :
                youtube_archiver.download(value)
            elif option == "--quit" :
                break
                
        print()
        print()

if __name__ == "__main__" :
    config_file = "config.json"
    
    options, arguments = getopt.getopt((sys.argv[1:]),"",["config=","help"])
    
    for option, value in options:
        if option == "--help" :
            print("Usage: <executable_name> [--config config_file]")
            print("If config file is not provided, the default 'config.json' will be used")
            sys.exit()
        elif option == "--config" :
            config_file = value

    run(config_file)
        