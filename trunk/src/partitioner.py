VERBOSE = True

def partition_score(intervals, required_attacks, time_frame):
    '''
    Partition a score represented by intervals. The function will
    return a list of segments where each segment starts with
    required_attacks note-attacks or more within length time_frame.
    
    intervals: list of intervals that represent the score
    required_attacks: no. of note-attacks required to have chord-change
    time_frame: 
    '''
    
    if VERBOSE:
        print 'Partitioning score with ' + str(len(intervals)) + ' intervals'
         
    # create minimal segments, that is, everywhere the notes change
    mini_segments = []
    for interval in intervals:
        
        # index of currently last mini-segment
        last = len(mini_segments)-1
        
        # we append a new mini-segment if
        # - there are no mini-segments yet or
        # - there are note-attacks in the current interval or
        # - the current interval is a rest and the previous wasn't
        if len(mini_segments) == 0 or interval['attacks'] > 0 or \
        (len(interval['pitches']) == 0 and \
         len(mini_segments[last]['pitches']) > 0):
            
            mini_segments.append({'length': 1,
                                  'attacks': interval['attacks'],
                                  'pitches': interval['pitches']})
        else:
            mini_segments[last]['length'] += 1
    
    if VERBOSE:
        print 'mini-segments:', mini_segments
    
    # create segments, that is, split up every time we have
    # at least 'required_attacks' note-attacks
    
    if VERBOSE:
        print 'Creating segments from ' + str(len(mini_segments)) + \
        ' mini segments'
        print 'If ' + str(required_attacks) + \
        ' or more note-attacks happen within the length ' + \
        str(time_frame) + ', a new segment will be created'
    
    no_of_mini_segments = len(mini_segments)
    segments = []
    
    # use index to iterate mini segments as we need to be able to
    # retrieve the coming mini segments
    m = 0
    while m in range(no_of_mini_segments):
        
        # current mini segment
        mini_seg = mini_segments[m]
        
        # the list of mini-segments that will form a possible new segment
        mini_segs = [mini_seg]
        
        # the no. of note-attacks within the time-frame
        total_attacks = mini_seg['attacks']
        
        # the total length is the length of all the mini segments that
        # are within the time frame
        total_length = mini_seg['length']
        next = m + 1
        
        # check how many mini segments
        # that can fit within the timeframe
        while next < no_of_mini_segments and \
        total_length + mini_segments[next]['length'] <= time_frame:
            
            if VERBOSE:
                print 'mini segments ' + str(m) + ' and ' + str(next) + ' are within the timeframe'
            total_length += mini_segments[next]['length']
            total_attacks += mini_segments[next]['attacks']
            mini_segs.append(mini_segments[next])
            next += 1
        
        if total_attacks >= required_attacks:
            # found enoughh note attacks to start new segment
            segments.append({'possible_chord': True,
                             'candidates': [],
                             'mini-segments': mini_segs})
        elif len(segments) == 0:
            # adding first segment (not a possible chord as the first check was false) 
            segments.append({'possible_chord': False,
                             'candidates': [],
                             'mini-segments': mini_segs})
        else:
            # no new segment, so add the mini segments to the latest
            segments[len(segments) - 1]['mini-segments'].append(mini_seg)
            
        m = next
            
    if VERBOSE:
        print 'segments: ', segments
        
    return segments