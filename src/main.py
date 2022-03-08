from interfaces.ConsoleInterface import ConsoleInterface
from environment.Environment import Environment

import getopt
import sys

def extractOptionAndValuePairs(options):
    option_value_pairs = {}

    for option, value in options:
        option_value_pairs[option.strip('-')] = value
        
    return option_value_pairs
    
def setConfigFile(option_value_pairs):
    config_file = "config.json"
    if "config" in option_value_pairs:
        config_file = option_value_pairs["config"]
    Environment.setEnvironment({
        'config_file' : config_file
    })
        
def runAppropriateArchiverWithInterface(option_value_pairs, interface):
    if "youtube_archiver" in option_value_pairs:
        interface.runYoutubeArchiver(option_value_pairs)
    else:
        interface.start()
        

if __name__ == "__main__" :
    options, arguments = getopt.getopt((sys.argv[1:]),"",[
        "config=",
        
        "help",
        "youtube_archiver",
        
        "filename=",
        "headers=",
        "values="])
    
    option_value_pairs = extractOptionAndValuePairs(options)
    setConfigFile(option_value_pairs)
    runAppropriateArchiverWithInterface(option_value_pairs, ConsoleInterface())
  