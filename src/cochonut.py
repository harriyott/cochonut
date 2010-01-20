from sys import argv
from sys import exit
from time import time

from parser import parse_file
from partitioner import partition_score
from chord_identifier import identify_chords
from contextanalyzer import analyse_segments
from util import print_chord

VERBOSE = True

# chord templates
# Important that the pitch-classes in the patterns are given in an
# incremental order, as the context analyzer may need to check the
# sizes of the intervals used in a template. Furthermore important that
# no pitches are left out, as the context analyzer might use them.
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

# note-attacks required to start a new segment
REQUIRED_ATTACKS = 3

# related to the getscore()-function in chord_identifier: the minimum
# score of the highest found score that a chord must have to be
# considered candidate
MIN_SCORE = 0.85

# the timeframe in which the required attacks must occur for chord change
TIME_FRAME = 1.0/16

if __name__ == '__main__':

    before = time()

    if VERBOSE:
        print 'Starting cochonut....'

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
        largest_divisor, intervals, key = parse_file(file)

        # partitioning
        if len(intervals) > 0:

            shortest = 1 / (4.0 * largest_divisor)
            frame_length = TIME_FRAME / (1 / (4.0 * largest_divisor))
            #print 'frame_length:', frame_length

            segments = []
            if VERBOSE:
                print 'Starting partitioner....'
            segments = partition_score(intervals, frame_length, REQUIRED_ATTACKS)

            # chord identifiyng
            if len(segments) > 0:
                if VERBOSE:
                    print 'Starting chord-identifier....'
                identify_chords(segments, templates,
                                REQUIRED_ATTACKS, MIN_SCORE)

                # context analyzing
                if VERBOSE:
                    print 'Starting context-analyzer....'
                analyse_segments(key, segments)

                # print results (each chord will be printed with a number 
                # that specifies where the chord starts in terms of 1/8 into the music,
                # for example "17, chord: Dminor" means that a Dminor
                # starts at 17 1/8-notes into the score.
                if VERBOSE:
                    print 'Segments with chords:'
                    for s in range(len(segments)):
                        if segments[s].has_key('chord'):
                            start = int(((shortest*segments[s]['start']) / 0.125) + 1)
                            description = str(start) + ', chord:'
                            print_chord(description,segments[s]['chord'])
                            
    after = time()
    print 'Time spent: ' + str(round((after-before)*1000,2)) + 'ms'

