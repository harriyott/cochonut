VERBOSE = True


# key/value: step in scale/pitch class relative to root-note in scale
scale = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}

possible_transitions = {0: [],
                        1: [0]}

chord_types = {0: 'tonic',
               1: 'dominant',
               2: 'dominant seventh',
               3: 'subdominant',
               4: 'tonic parallel',
               5: 'subdominant parallel',
               6: 'dominant parallel',
               7: 'incomplete dominant',
               8: 'dominant none',
               9: 'dominant quater sixth',
               10: 'subdominant sixth',
               11: 'incomplete subdominant',
               12: 'minor subdominant'}


def is_tonic(tonic, chord):
    return tonic == chord['root']

def is_dominant(tonic, chord):
    return scale[5] == (chord['root'] - tonic) % 12

def is_subdominant(tonic, chord):
    return scale[4] == (chord['root'] - tonic) % 12



def is_dominant_seventh(tonic, chord):
    return is_dominant(tonic, chord) and \
    chord['pitches'][(tonic + scale[4]) % 12] != 0
    
def is_incomplete_dominant(tonic, chord):
    return is_dominant_seventh(tonic, chord) and \
    chord['pitches'][(tonic + scale[5]) % 12] == 0
    
    
# TODO: p. 56
def is_dominant_none(tonic, chord):
    return is_dominant(tonic, chord)

# TODO: p. 57
def is_dominant_quater_sixth(tonic, chord):
    return is_dominant(tonic, chord)


# TODO: p. 58
def is_subdominant_sixth(tonic, chord):
    return is_subdominant(tonic, chord)

# TODO: p. 58
def is_incomplete_subdominant(tonic, chord):
    return is_subdominant_sixth(tonic, chord)

def is_minor_subdominant(tonic, chord):
    '''
    Should only be used when the key is major
    '''
    return is_subdominant(tonic, chord)


def is_tonic_parallel(tonic, chord, chord_is_minor):
    if chord_is_minor:
        return ((tonic - 3) % 12) == chord['root']
    else:
        return ((tonic + 3) % 12) == chord['root']

def is_subdominant_parallel(tonic, chord):
    return is_subdominant(tonic,((chord['root'] + 3) % 12))

def is_dominant_parallel(tonic, chord):
    return is_dominant(tonic,((chord['root'] + 3) % 12))




def find_legal_transitions(tonic, previous, candidates):
    transitions = []
    
    
    
    return transitions




def analyse_segments(key, segments):
    '''
    Assumes that tonality doesnt change in score.
    Assumes that "something with g-key is always on"
    Assumes that musicxml has revealed the key
    '''
    
    # a perfect fifth is 7 semitone-steps
    fifth_dist = 7
    
    # step through circle of fifths to find root in scale
    tonic = {}
    tonic['mode'] = key['mode']
    if tonic['mode'] == 'major':
        tonic['root'] = (key['fifths'] * fifth_dist) % 12
    else:
        # the circle of fifths has 'A' as the first element in 'minor mode'
        tonic['root'] = 9 + (key['fifths'] * fifth_dist) % 12
    
    if VERBOSE:
        print 'Found tonic:', tonic
        
    prev_chord = None
        
    #for s in range(len(segments)):
    for current in segments:
        
        #current = segments[s]
        candidates = current['candidates']
        
        #if s > 0:
        #    prev_chord = segments[s-1]
        
        if len(candidates) == 1:
            current['chord'] = candidates[0]
            
        elif len(candidates) > 1:
            transitions = find_legal_transitions(tonic, prev_chord, candidates)
            
            if len(transitions) > 0:
                pass
            
            else:
                pass # select candidate with highest score