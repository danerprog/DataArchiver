from interfaces.ConsoleInterface import ConsoleInterface
from environment.Environment import Environment

import getopt
import sys

if __name__ == "__main__" :
    options, arguments = getopt.getopt((sys.argv[1:]),"",["config=","help","youtube_archiver="])
    is_command_line_mode_enabled = False
    filename = None
    config_file = "config.json"
    
    for option, value in options:
        if option == "--help" :
            print("Usage: <executable_name> [--config config_file]")
            print("If config file is not provided, the default 'config.json' will be used")
            sys.exit()
        elif option == "--config" :
            config_file = value
        elif option == "--youtube_archiver" :
            is_command_line_mode_enabled = True
            archiver_options = value
    
    Environment.setEnvironment({
        'config_file' : config_file
    })
    
    interface = ConsoleInterface()
    
    if is_command_line_mode_enabled:
        interface.runYoutubeArchiver(archiver_options)
    else:
        interface.start()
        