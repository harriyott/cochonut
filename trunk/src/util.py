# maps pitch-class numbers to pitch-class names
CLASS_NAME_MAP = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

# the pitch classes
PITCH_CLASSES = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}

def print_chord(description, chord):
    '''
    Pretty-print the contents of a chord.
    '''
    print description + ' ' + \
    CLASS_NAME_MAP[chord['root']] + \
    chord['template']['name'] + ' (' + \
    str(chord['template']['pattern']) + ')'

#def new_chord(root, template, pitches, score):
#    return {'root': root,
#            'template': template,
#            'pitches': pitches,
#            'score': score}

#    
#def chord_template(name, template):
#    return {'name': name,
#            'template': template}
    
    