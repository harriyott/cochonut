"""
COCHONUT

"""

from sys import argv
from sys import exit
import logging.handlers

from parser import parse_file
from partitioner import partitionScore

LOG_FILE = '../log/mylog.log'

def set_up_logging():
    global myLogger
    myLogger = logging.getLogger('myLogger')
    myLogger.setLevel(logging.INFO) #handler = logging.FileHandler(LOG_FILE)
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s: %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    myLogger.addHandler(handler)

if __name__ == '__main__':
    
    set_up_logging()
    
    myLogger.info('---------------- Starting cochonut ----------------')
    
    # get file to parse
    file = ''
    try:
        file = argv[1]
    except IndexError:
        msg = 'No file specified'
        myLogger.error(msg)
        exit(msg)
    
    # parsing
    if file:
        shortestNote = 1
        mSegments = []
        try:
            shortestNote, mSegments = parse_file(file, myLogger)
        except Exception as e:
            msg = 'Failed to parse file: ' + e.args[0]
            myLogger.error(msg)
            exit(msg)
            
        # partitioning
        if len(mSegments) > 0:
            segments = []
            try:
                segments = partitionScore(mSegments, myLogger)
            except Exception as e:
                msg = 'Failed to partition: ' + e.args[0]
                myLogger.error(msg)
                exit(msg)                    

