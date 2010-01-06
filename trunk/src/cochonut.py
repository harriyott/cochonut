from sys import argv
from sys import exit

from parser import parse_file
from partitioner import partition_score
from chord_identifier import identify_chords
from contextanalyzer import analyse_segments

# chord templates
# TODO: More chords from http://www.looknohands.com/chordhouse/piano/ and Re-naming of chords
templates = [{'name': 'maj', 'template': [0, 4, 7]},
             {'name': 'minor', 'template': [0, 3, 7]},
             {'name': 'diminished', 'template': [0, 3, 6]},
             {'name': 'augmented', 'template': [0, 4, 8]},
             {'name': 'sus4', 'template': [0, 5, 7]},
             {'name': 'sus2', 'template': [0, 2, 7]},
             
             {'name': 'maj7', 'template': [0, 4, 7, 11]},
             {'name': 'dom', 'template': [0, 4, 7, 10]},
             {'name': 'half diminished', 'template': [0, 3, 6, 10]},
             {'name': 'fully diminished', 'template': [0, 3, 6, 9]},
             {'name': 'minor 7th', 'template': [0, 3, 7, 10]},
             {'name': 'minor-maj7', 'template': [0, 3, 7, 11]},
             {'name': '+7', 'template': [0, 4, 8, 10]},
             {'name': '7sus4', 'template': [0, 5, 7, 10]},
             {'name': 'maj6', 'template': [0, 4, 7, 9]},
             {'name': 'm6', 'template': [0, 3, 7, 9]},
             
             {'name': '9', 'template': [0, 4, 7, 10, 2]},
             {'name': '9b', 'template': [0, 4, 7, 10, 1]},
             {'name': '9#', 'template': [0, 4, 7, 10, 3]},
             {'name': 'maj9', 'template': [0, 4, 7, 11, 2]},
             {'name': '11', 'template': [0, 4, 7, 10, 2, 5]},
             {'name': '11#', 'template': [0, 4, 7, 10, 2, 6]},
             {'name': '13', 'template': [0, 4, 7, 10, 2, 5, 9]},
             {'name': '13b', 'template': [0, 4, 7, 10, 2, 5, 8]},
             {'name': '7add6', 'template': [0, 4, 7, 10, 9]}]

# the main pitch classes without alternating steps
PITCH_CLASSES = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}

map = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

# no. of pitch classes
NO_OF_PITCH_CLASSES = 12

# note-attacks required to start a new segment
REQUIRED_ATTACKS = 3

# 
MIN_SCORE = 0.85

# the timeframe in which the required attacks must occur for chord change
# TODO: Should be based on beat?
TIME_FRAME = 1.0/16

VERBOSE = True

if __name__ == '__main__':
    
    if VERBOSE:
        print 'Starting cochonut....'
        print 'Time-frame is ', TIME_FRAME
    
    # get file to parse from command-line arguments
    file = ''
    try:
        file = argv[1]
    except IndexError:
        exit('No file specified')
    
    # parsing
    if file:
        largest_divisor = 1
        intervals = []
        try:
            if VERBOSE:
                print 'Starting parser....'
            largest_divisor, intervals, key = parse_file(file, PITCH_CLASSES)
        except Exception as e:
            exit('Failed to parse file: ' + e.args[0])
            
        # partitioning
        if len(intervals) > 0:
            
            frame_length = TIME_FRAME/(1/(4.0*largest_divisor))
            #print 'frame_length:', frame_length
            
            segments = []
            try:
                if VERBOSE:
                    print 'Starting partitioner....'
                segments = partition_score(intervals, REQUIRED_ATTACKS, frame_length)
            except Exception as e:
                exit('Failed to partition: ' + e.args[0])
                
            # chord identifiyng
            if len(segments) > 0:
                if VERBOSE:
                    print 'Starting chord-identifier....'
                identify_chords(segments, templates,
                                REQUIRED_ATTACKS, NO_OF_PITCH_CLASSES, MIN_SCORE)
                
                # context analyzing
                if VERBOSE:
                    print 'Starting context-analyzer....'
                analyse_segments(key, segments)
                
                # TODO: from cochonut: 'a post-processing step is made to merge consecutive segments with identical chords.'
                
                # print results
                if VERBOSE:
                    print 'Segments with chords:'
                    for s in range(len(segments)):
                        if segments[s].has_key('chord'):
                            print 'Segment ' + str(s) + ', chord: ' + \
                            map[segments[s]['chord']['root']] + '-' + \
                            segments[s]['chord']['template']['name']

