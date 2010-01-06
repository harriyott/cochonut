VERBOSE = True

# key/value: step in scale/pitch class relative to root-note in scale
#scale = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}

TONIC, \
DOMINANT, \
DOMINANT_SEVENTH, \
INCOMPLETE_DOMINANT, \
DOMINANT_NONE, \
DOMINANT_QUARTER_SIXTH, \
SUBDOMINANT, \
SUBDOMINANT_SIXTH, \
SUBDOMINANT_PARALLEL_SEVENTH, \
MINOR_SUBDOMINANT, \
INCOMPLETE_SUBDOMINANT, \
TONIC_PARALLEL, \
SUBDOMINANT_PARALLEL, \
DOMINANT_PARALLEL \
= range(14)

# T: T T_3 D S D{4,3} S6_5 S6_6 D_3 Sp Dp 4D Tp /S /D S_3
# T_3: T D D7 S_3 D{4,3} 4D {6,4}D S6 S6_6 S6_5 /S /D +S S Tp D{6,5}
# T{6,4}: S6
# Ts: D D7 S S6 Dp T_3 D_3 /S
# Tp: D D7 S S6 Dp T_3 D_3 /S
# S: D D7 S_3 D_2 {6,4}D Tp 4D T /D D9 oD
# +S: /D
# oS: {6,4}D +D
# S_3: S T D D7 D{6,5} T{6,4} D_3 4D +D S6 T_3
# Sp: Dp S /D T_3 D
# Sp7: ...
# /S: D D7 +D {6,4}D
# S6: D D7 {6,4}D +D
# S6_5: D{6,5} D_3
# S6_6: D D7 /D
# D: T D_2 D_3 Tp Ts D7
# +D: T
# oD: T
# D_3: D D7 T S_3
# Dp: S D7
# /D: T Ts T_3
# 4D: D D7
# {6,4}D: D +D D7
# D7: T
# D{6,5}: T
# D{4,3}: T
# D_2: T_3
# D9: T

possible_transitions = {TONIC: [TONIC, DOMINANT, SUBDOMINANT,
                                SUBDOMINANT_PARALLEL,
                                DOMINANT_PARALLEL, TONIC_PARALLEL,
                                INCOMPLETE_DOMINANT, INCOMPLETE_SUBDOMINANT],
                        TONIC_PARALLEL: [DOMINANT, DOMINANT_SEVENTH,
                                         SUBDOMINANT, SUBDOMINANT_SIXTH,
                                         DOMINANT_PARALLEL, INCOMPLETE_SUBDOMINANT],
                        SUBDOMINANT: [DOMINANT, DOMINANT_SEVENTH,
                                      SUBDOMINANT_SIXTH, DOMINANT_QUARTER_SIXTH],
                                      DOMINANT: [],
                                      DOMINANT_SEVENTH: [],
                                      INCOMPLETE_DOMINANT: [],
                                      DOMINANT_NONE: [],
                                      DOMINANT_QUARTER_SIXTH: [],
                                      SUBDOMINANT_SIXTH: [],
                                      SUBDOMINANT_PARALLEL_SEVENTH: [],
                                      MINOR_SUBDOMINANT: [],
                                      INCOMPLETE_SUBDOMINANT: [],
                                      SUBDOMINANT_PARALLEL: [],
                                      DOMINANT_PARALLEL: []}


def get_chord_type(tonic, chord):
    
    # TODO: values correct?
    subdomi_dist = 5
    small_seventh = 10
    small_sixth = 8
    large_sixth = 9
    small_none = 14
    fifth = 6
    domi_dist = 7
    minor = tonic['mode'] == 'minor'
    
    # tonic
    if tonic['root'] == chord['root']:
        return TONIC
    
    # dominant
    elif domi_dist == (chord['root'] - tonic['root']) % 12:
        
        # dominant none, small none added
        if chord['pitches'][(chord['root'] + small_none) % 12] != 0:
            return DOMINANT_NONE
        
        # dominant seventh, added small seventh
        elif chord['pitches'][(chord['root'] + small_seventh) % 12] != 0:

            # in-complete dominant, no pitch at root
            if chord['pitches'][(tonic['root'] + domi_dist) % 12] == 0:
                return INCOMPLETE_DOMINANT
            
            return DOMINANT_SEVENTH
        
        # dominant 4-6
        # TODO!
        elif False:
            return DOMINANT_QUARTER_SIXTH
        
        return DOMINANT
    
    # subdominant
    elif subdomi_dist == (chord['root'] - tonic['root']) % 12:
        
        # subdominant sixth, added a small sixth
        if chord['pitches'][(chord['root'] + small_sixth) % 12] != 0:
            
            # in-complete subdominant, no fifth
            if chord['pitches'][(chord['root'] + fifth) % 12] == 0:
                return INCOMPLETE_SUBDOMINANT
            
            return SUBDOMINANT_SIXTH
        
        # minor subdominant, added a large sixth
        elif chord['pitches'][(chord['root'] + large_sixth) % 12] != 0:
            return MINOR_SUBDOMINANT
        
        return SUBDOMINANT
    
    # tonic parallel (two possiblities)
    elif (minor and ((tonic['root'] - 3) % 12) == chord['root']) or \
    (not minor and ((tonic['root'] + 3) % 12) == chord['root']):
        return TONIC_PARALLEL
    
    # dominant parallel
    elif (minor and domi_dist == (chord['root'] - tonic['root'] + 3) % 12) or \
    (not minor and domi_dist == (chord['root'] - tonic['root'] - 3) % 12):
        return DOMINANT_PARALLEL
    
    # subdominant parallel
    elif (minor and subdomi_dist == (chord['root'] - tonic['root'] + 3) % 12) or \
    (not minor and subdomi_dist == (chord['root'] - tonic['root'] - 3) % 12):
        
        # subdominant parallel seventh
        if False:
            return SUBDOMINANT_PARALLEL_SEVENTH
        
        return SUBDOMINANT_PARALLEL
        
    return None


def find_legal_chords(tonic, previous, chords):
    '''
    Given a tonic (pitch-class), the previous chord and a set of
    possible chords, find the chords from this set that are legal,
    that is, the chords that the previous chord can transite into.
    '''
    
    # find possible transitions from previous chord
    #print 'tonic:', tonic
    #print 'previous:', previous
    type = get_chord_type(tonic, previous)
    print 'Type of previous:', type
    
    legal_chords = []
    
    if type:
        pos = possible_transitions[type]
        
        # search for each chord in list of legal transitions
        for chord in chords:
            type = get_chord_type(tonic, chord)
            if pos.count(type):
                legal_chords.append(chord)
                
    return legal_chords


def get_highest(chords):
    '''
    Find the chord with the highest score among a list of chords
    and return this chord.
    '''
    highest = 0
    index = 0
    for c in range(len(chords)):
        if chords[c]['score'] > highest:
            highest = chords[c]['score']
            index = c
    return chords[index]



def analyse_segments(key, segments):
    '''
    Assumes that tonality doesnt change in score.
    Assumes that "something with g-key is always on"
    Assumes that musicxml has revealed the key
    '''
    
    # a perfect fifth is 7 semitone-steps
    fifth_dist = 7
    
    if key:
    
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
        for segment in segments:
            
            # find legal chords among candidates
            candidates = segment['candidates']
            
            legal_chords = []
            if prev_chord:
                legal_chords = find_legal_chords(tonic, prev_chord, candidates)            
                
            if len(legal_chords) > 0:
                if VERBOSE:
                    print 'Found legal transitions:', legal_chords
                segment['chord'] = get_highest(legal_chords)
                prev_chord = segment['chord']
                
            elif len(candidates) > 0:
                segment['chord'] = get_highest(candidates)
                prev_chord = segment['chord']
    
    # no key has been set for the score so we pick candidates with highest score
    else:
        for segment in segments:
            candidates = segment['candidates']
            if len(candidates) > 0:
                segment['chord'] = get_highest(candidates)