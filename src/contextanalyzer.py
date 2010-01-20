from util import print_chord

VERBOSE = True

# chord types
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

# for printing chord type names during tests
names = {
TONIC: 'tonic',
DOMINANT: 'dominant',
DOMINANT_SEVENTH: 'dominant seventh',
INCOMPLETE_DOMINANT: 'incomplete dominant',
DOMINANT_NONE: 'dominant none', 
DOMINANT_QUARTER_SIXTH: 'dominant quarter sixth',
SUBDOMINANT: 'subdominant',
SUBDOMINANT_SIXTH: 'subdominant sixth',
SUBDOMINANT_PARALLEL_SEVENTH: 'subdominant parallel seventh',
MINOR_SUBDOMINANT: 'minor subdominant',
INCOMPLETE_SUBDOMINANT: 'incomplete subdominant',
TONIC_PARALLEL: 'tonic parallel',
SUBDOMINANT_PARALLEL: 'subdominant parallel',
DOMINANT_PARALLEL: 'dominant parallel'
}

# TODO: Check
# possible chord-transitions: a transition is possible from a key in
# this dictionary to every chord in the list, coupled with this key
possible_transitions = {
TONIC: [TONIC, DOMINANT, SUBDOMINANT, SUBDOMINANT_PARALLEL, DOMINANT_PARALLEL, TONIC_PARALLEL, INCOMPLETE_DOMINANT, INCOMPLETE_SUBDOMINANT],
TONIC_PARALLEL: [DOMINANT, DOMINANT_SEVENTH, SUBDOMINANT, SUBDOMINANT_SIXTH, DOMINANT_PARALLEL, INCOMPLETE_SUBDOMINANT],
SUBDOMINANT: [DOMINANT, DOMINANT_SEVENTH, SUBDOMINANT_SIXTH, DOMINANT_QUARTER_SIXTH],
DOMINANT: [TONIC, TONIC_PARALLEL, DOMINANT_SEVENTH],
DOMINANT_SEVENTH: [TONIC],
INCOMPLETE_DOMINANT: [TONIC],
DOMINANT_NONE: [TONIC],
DOMINANT_QUARTER_SIXTH: [DOMINANT, DOMINANT_SEVENTH],
SUBDOMINANT_SIXTH: [SUBDOMINANT, TONIC, DOMINANT, DOMINANT_SEVENTH],
SUBDOMINANT_PARALLEL_SEVENTH: [],
MINOR_SUBDOMINANT: [DOMINANT_QUARTER_SIXTH],
INCOMPLETE_SUBDOMINANT: [DOMINANT, DOMINANT_SEVENTH, DOMINANT_QUARTER_SIXTH],
SUBDOMINANT_PARALLEL: [DOMINANT_PARALLEL, SUBDOMINANT, INCOMPLETE_DOMINANT, DOMINANT],
DOMINANT_PARALLEL: [SUBDOMINANT, DOMINANT_SEVENTH]}


def find_chord_type(tonic, chord):
    '''
    Find the chord-type of a given chord, relative to a given tonic
    '''
    
    SUBDOMINANT_DIST = 5
    SMALL_SEVENTH = 10
    LARGE_SEVENTH = 11
    LARGE_SIXTH = 9
    SMALL_NONE = 13
    DOMINANT_DIST = 7
    minor = tonic['mode'] == 'minor'
    
    pattern = chord['template']['pattern']
    third_replacedby_quarter = pattern[1] > 4
    fifth_replacedby_sixth = pattern[2] > 7
    fifth_size = pattern[2] - pattern[0]
    
    # the pitch classes that the dominant and subdominant are built on 
    dominant = (tonic['root'] + DOMINANT_DIST) % 12
    subdominant = (tonic['root'] + SUBDOMINANT_DIST) % 12
    
    root = chord['root'] # the root of the chord
            
    # tonic: same root as tonic
    if tonic['root'] == root:
        return TONIC
    
    # dominant
    elif root == dominant:
        
        # dominant none: dominant added a small none
        if chord['pitches'][(root + SMALL_NONE) % 12] != 0:
            return DOMINANT_NONE
        
        # dominant seventh: dominant added a small seventh
        elif chord['pitches'][(root + SMALL_SEVENTH) % 12] != 0:

            # in-complete dominant: dominant with no pitch at root
            if chord['pitches'][(tonic['root'] + DOMINANT_DIST) % 12] == 0:
                return INCOMPLETE_DOMINANT
            
            return DOMINANT_SEVENTH
        
        # dominant 4-6: dominant but replace third with quarter and fifth with sixth
        elif third_replacedby_quarter and fifth_replacedby_sixth:
            return DOMINANT_QUARTER_SIXTH
        
        return DOMINANT
    
    # subdominant
    elif root == subdominant:
        
        # subdominant sixth: subdominant added a small sixth
        if chord['pitches'][(root + LARGE_SIXTH) % 12] != 0:
            
            # in-complete subdominant: subdominant sixth with no fifth
            if chord['pitches'][(root + fifth_size) % 12] == 0:
                return INCOMPLETE_SUBDOMINANT
            
            return SUBDOMINANT_SIXTH
        
        # minor subdominant: subdominant added a large sixth
        elif chord['pitches'][(root + LARGE_SIXTH) % 12] != 0:
            return MINOR_SUBDOMINANT
        
        return SUBDOMINANT
    
    # tonic parallel: parallel chord to the tonic
    elif (minor and ((tonic['root'] + 3) % 12) == root) or \
    (not minor and ((tonic['root'] - 3) % 12) == root):
        return TONIC_PARALLEL
    
    # dominant parallel: parallel chord to the dominant
    elif (minor and root == (dominant + 3) % 12) or \
    (not minor and root == (dominant - 3) % 12):
        return DOMINANT_PARALLEL
    
    #elif (minor and DOMINANT_DIST == (root - (tonic['root'] + 3)) % 12) or \
    #(not minor and DOMINANT_DIST == (root - (tonic['root'] - 3)) % 12):
    #    return DOMINANT_PARALLEL
    
    # subdominant parallel: parallel chord to the subdominant
    elif (minor and root == (subdominant + 3) % 12) or \
    (not minor and root == (subdominant - 3) % 12):
        
        # subdominant parallel seventh: sub. parallel added a seventh
        if (minor and (chord['pitches'][(root + SMALL_SEVENTH) % 12] != 0)) or \
           (not minor and (chord['pitches'][(root + LARGE_SEVENTH) % 12] != 0)):
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
    prev_type = find_chord_type(tonic, previous)
    legal_chords = []
    
    if prev_type is not None:
        if VERBOSE:
            print 'Previous chord:', names[prev_type]
        pos = possible_transitions[prev_type]
        
        # search for each chord in list of legal transitions
        for chord in chords:
            type = find_chord_type(tonic, chord)
            if pos.count(type):
                if VERBOSE:
                    print 'Found legal transition to', names[type], chord
                legal_chords.append(chord)
    elif VERBOSE:
        print 'Type of previous not found!'
                
    return legal_chords


def get_highest(chords):
    '''
    Find the chord with the highest score among a list of chords
    and return this chord. In case of more than one chords having
    the highest score, the first one found will be returned.
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
    
    # A perfect fifth is the distance between the elements in the
    # circle of fifths. A perfect fifth is 7 semitone-steps
    PERFECT_FIFTH = 7
    
    if key:
    
        # step through circle of fifths to find root in scale
        tonic = {}
        tonic['mode'] = key['mode']
        if tonic['mode'] == 'major':
            tonic['root'] = (key['fifths'] * PERFECT_FIFTH) % 12
        else:
            # the circle of fifths has 'A' as the first element in 'minor mode'
            tonic['root'] = (9 + (key['fifths'] * PERFECT_FIFTH)) % 12
        
        if VERBOSE:
            print 'Found tonic:', tonic
            
        prev_chord = None
        for segment in segments:
            
            # find legal chords among candidates
            candidates = segment['candidates']
            
            legal_chords = []
            if prev_chord:
                if VERBOSE:
                    print 'Finding legal transitions for segment with candidates ', candidates 
                legal_chords = find_legal_chords(tonic, prev_chord, candidates)            
                
            if len(legal_chords) > 0:
                segment['chord'] = get_highest(legal_chords)
                prev_chord = segment['chord']
                if VERBOSE:
                    print_chord('Chosen chord:', segment['chord'])
                
            elif len(candidates) > 0:
                segment['chord'] = get_highest(candidates)
                prev_chord = segment['chord']
                if VERBOSE:
                    print_chord('Chosen chord:', segment['chord'])
    
    # no key has been set for the score so we pick candidates with highest score
    else:
        for segment in segments:
            candidates = segment['candidates']
            if len(candidates) > 0:
                segment['chord'] = get_highest(candidates)