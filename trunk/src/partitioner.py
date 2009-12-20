'''
Partitioner

'''

# TODO: Not considering time-window (section 4.1, COCHONUT)

def partition_score(intervals, logger, required_attacks):
    logger.info('Partitioning score with ' + str(len(intervals)) + ' intervals')
    
    # create minimal segments, that is, everywhere the notes change
    logger.info('Creating minimal segments')
    mini_segments = []
    for interval in intervals:
        if interval['attacks'] > 0:
            # new mini-segment
            mini_seg = {'length': 1,
                        'attacks': interval['attacks'],
                        'pitches': interval['pitches']}
            mini_segments.append(mini_seg)
        else:
            # no attacks: append interval to current mini-segment
            last = len(mini_segments)-1
            length = mini_segments[last]['length']
            length = length + 1 
            mini_segments[last]['length'] = length
    
    #print 'mini-seg 3:', mini_segments[3]
    
    # create segments, that is, split up every time we have
    # at least 'required_attacks' note-attacks
    logger.info('Creating segments')
    
    segments = [{'chord': '', 'mini-segments': []}]
    for mini_seg in mini_segments:
        
        if mini_seg['attacks'] >= required_attacks:
            s = {'chord': '', 'mini-segments': [mini_seg]}
            segments.append(s)
        else:
            last = len(segments) - 1
            segments[last]['mini-segments'].append(mini_seg)
            
    logger.info('Done partitioning, now returning')
    print 'segments: ', segments
    return segments