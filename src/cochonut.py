from sys import argv
from sys import exit

from parser import parse_file
from partitioner import partition_score
from chord_identifier import identify_chords
from contextanalyzer import analyse_segments

# chord templates
# important that the pitch-classes in the patterns are given in an
# incremental order, as the context analyzer may need to check the
# sizes of the intervals used in a template
# furthermore important that no pitches are left out, as the context
# analyzer might use them as well
templates = [{'name': 'maj', 'pattern': [0, 4, 7]},
             {'name': 'minor', 'pattern': [0, 3, 7]},
             {'name': 'diminished', 'pattern': [0, 3, 6]},
             {'name': '-5', 'pattern': [0, 4, 6]},
             {'name': 'aug', 'pattern': [0, 4, 8]},
             {'name': 'sus4', 'pattern': [0, 5, 7]},
             {'name': 'sus2', 'pattern': [0, 2, 7]},
             {'name': 'maj7', 'pattern': [0, 4, 7, 11]},
             {'name': 'maj7+5', 'pattern': [0, 4, 8, 11]},
             {'name': 'dom', 'pattern': [0, 4, 7, 10]},
             {'name': 'add9', 'pattern': [0, 4, 7, 14]},
             {'name': '1/2dim', 'pattern': [0, 3, 6, 10]},
             {'name': 'dim7', 'pattern': [0, 3, 6, 9]},
             {'name': 'min7', 'pattern': [0, 3, 7, 10]},
             {'name': 'min/maj7', 'pattern': [0, 3, 7, 11]},
             {'name': '7+5', 'pattern': [0, 4, 8, 10]},
             {'name': '7-5', 'pattern': [0, 4, 6, 10]},
             {'name': '7sus4', 'pattern': [0, 5, 7, 10]},
             {'name': 'maj6', 'pattern': [0, 4, 7, 9]},
             {'name': 'minor6', 'pattern': [0, 3, 7, 9]},
             {'name': 'madd9', 'pattern': [0, 3, 7, 14]},
             {'name': 'm6/9', 'pattern': [0, 3, 7, 9, 14]},
             {'name': '6add9', 'pattern': [0, 4, 7, 9, 14]},
             {'name': '7/6', 'pattern': [0, 4, 7, 9, 10]},
             {'name': '9', 'pattern': [0, 4, 7, 10, 14]},
             {'name': '7/13', 'pattern': [0, 4, 7, 10, 21]},
             {'name': '9-5', 'pattern': [0, 4, 6, 10, 14]},
             {'name': '9+5', 'pattern': [0, 4, 8, 10, 14]},
             {'name': 'min9', 'pattern': [0, 3, 7, 10, 14]},
             {'name': '7-9', 'pattern': [0, 4, 7, 10, 13]},
             {'name': '7+9', 'pattern': [0, 4, 7, 10, 15]},
             {'name': 'maj9', 'pattern': [0, 4, 7, 11, 14]},
             {'name': 'min/maj9', 'pattern': [0, 3, 7, 11, 14]},
             {'name': '9/6', 'pattern': [0, 4, 7, 9, 10, 14]},
             {'name': 'maj11', 'pattern': [0, 4, 7, 11, 14, 17]},
             {'name': '9+11', 'pattern': [0, 4, 7, 10, 14, 18]},
             {'name': '11', 'pattern': [0, 4, 7, 10, 14, 17]},
             {'name': '11-9', 'pattern': [0, 4, 7, 10, 13, 17]},
             {'name': 'aug11', 'pattern': [0, 4, 7, 10, 14, 18]},
             {'name': 'min11', 'pattern': [0, 3, 7, 10, 14, 17]},
             {'name': 'min13', 'pattern': [0, 3, 7, 10, 14, 17, 21]},
             {'name': 'maj13', 'pattern': [0, 4, 7, 11, 14, 17, 21]},
             {'name': '13', 'pattern': [0, 4, 7, 10, 14, 17, 21]},
             {'name': '13-9', 'pattern': [0, 4, 7, 10, 13, 17, 21]},
             {'name': '13-9-6', 'pattern': [0, 4, 6, 10, 13, 17, 21]},
             {'name': '13-9+11', 'pattern': [0, 4, 7, 10, 13, 18, 21]},
             {'name': '13+11', 'pattern': [0, 4, 7, 10, 14, 18, 21]},
             {'name': '13b', 'pattern': [0, 4, 7, 10, 14, 17, 20]}]

# the main pitch classes without alternating steps
PITCH_CLASSES = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}

CLASS_NAME_MAP = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

# no. of pitch classes
NO_OF_PITCH_CLASSES = 12

# note-attacks required to start a new segment
REQUIRED_ATTACKS = 3

# 
MIN_SCORE = 0.6

# the timeframe in which the required attacks must occur for chord change
# TODO: Should be based on beat?
TIME_FRAME = 1.0 / 16

VERBOSE = False

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
        if VERBOSE:
            print 'Starting parser....'
        largest_divisor, intervals, key = parse_file(file, PITCH_CLASSES)

        # partitioning
        if len(intervals) > 0:

            frame_length = TIME_FRAME / (1 / (4.0 * largest_divisor))
            #print 'frame_length:', frame_length

            segments = []
            if VERBOSE:
                print 'Starting partitioner....'
            segments = partition_score(intervals, REQUIRED_ATTACKS, frame_length)

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
                            CLASS_NAME_MAP[segments[s]['chord']['root']] + \
                            segments[s]['chord']['template']['name'] + \
                            ' (' + \
                            str(segments[s]['chord']['template']['pattern']) + ')'

