"""
COCHONUT

"""

from sys import argv
from sys import exit
import logging.handlers

from parser import parse_file
from partitioner import partition_score
from chord_identifier import identify_chords

LOG_FILE = '../log/mylog.log'

# chord templates
templates = [{'name': 'major triad', 'template': [0, 4, 7]},
             {'name': 'minor triad', 'template': [0, 3, 7]},
             {'name': 'diminished triad', 'template': [0, 3, 6]},
             {'name': 'augmented triad', 'template': [0, 4, 8]}]

# the main pitch classes without alternating steps
PITCH_CLASSES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
PITCHES = 12

# note-attacks required to start a new segment
REQUIRED_ATTACKS = 3

# 
MIN_SCORE = 0.85

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
        largest_divisor = 1
        intervals = []
        try:
            largest_divisor, intervals = parse_file(file, PITCH_CLASSES)
        except Exception as e:
            msg = 'Failed to parse file: ' + e.args[0]
            myLogger.error(msg)
            exit(msg)
            
        # partitioning
        if len(intervals) > 0:
            segments = []
            try:
                segments = partition_score(intervals, myLogger, REQUIRED_ATTACKS)
            except Exception as e:
                msg = 'Failed to partition: ' + e.args[0]
                myLogger.error(msg)
                exit(msg)
                
            # chord identifiyng
            if len(segments) > 0:
                identify_chords(segments, templates,
                                REQUIRED_ATTACKS, PITCHES, MIN_SCORE)

