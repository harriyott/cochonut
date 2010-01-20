# map: pitch-class numbers to pitch-class names
NUMBER_NAME_MAP = {0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E', 5: 'F',
                   6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'}

# map: pitch-class names to pitch-class numbers
PITCH_CLASSES = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}

def print_chord(description, chord):
    '''
    Pretty-print the contents of a chord.
    '''
    print description + ' ' + \
    NUMBER_NAME_MAP[chord['root']] + \
    chord['template']['name'] + ' (' + \
    str(chord['template']['pattern']) + ')'