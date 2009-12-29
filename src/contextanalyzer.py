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
               7: 'incomplete dominant'}

def is_tonic(tonic, chord):
    pass

def is_dominant(tonic_pitch_class, chord):
    '''
    chord must be normalized so we have its root at the first index
    '''
    return scale[5] == (chord[0] - tonic_pitch_class) % 12

def is_dominantseptim(tonic_pitch_class, chord):
    '''
    chord must be normalized so we have its root at the first index
    '''
    pass
    #return is_dominant(tonic_pitch_class, chord) and len(chord) >= 4 and ??
    
def is_subdominant(tonic_pitch_class, chord):
    return scale[4] == (chord[0] - tonic_pitch_class) % 12

def is_tonikaparallel(tonic_pitch_class, chord_root, chord_is_minor):
    if chord_is_minor:
        return ((tonic_pitch_class - 3) % 12) == chord_root
    else:
        return ((tonic_pitch_class + 3) % 12) == chord_root
    

def is_subdominantparallel(tonic_pitch_class, chord_root):
    return is_subdominant(tonic_pitch_class,((chord_root + 3) % 12))

def is_dominantparallel(tonic_pitch_class, chord_root):
    return is_dominant(tonic_pitch_class,((chord_root + 3) % 12))




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