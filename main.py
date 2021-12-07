from interfaces.ConsoleInterface import ConsoleInterface

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
            filename = value

    interface = ConsoleInterface({
        'config_file' : config_file
    })
    
    if is_command_line_mode_enabled:
        interface.runYoutubeArchiver(filename)
    else:
        interface.start()
        