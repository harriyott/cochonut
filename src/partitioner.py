'''
Partitioner

'''

def partitionScore(intervals, logger):
    logger.info('Partitioning score with ' + str(len(intervals)) + ' intervals')
    
    # create minimal segments, that is, everywhere the notes change
    logger.info('Creating minimal segments')
    mini_segments = []
    for interval in intervals:
        if interval['attacks'] > 0:
            mini_seg = {'length': 1,
                        'attacks': interval['attacks'],
                        'pitches': interval['pitches']}
            mini_segments.append(mini_seg)
        else:
            last = len(mini_segments)-1
            length = mini_segments[last]['length']
            length = length + 1 
            mini_segments[last]['length'] = length
    
    #print 'mini-seg 3:', mini_segments[3]
    
    # create segments, that is, split up every time we have
    # at least REQUIRED note-attacks
    REQUIRED = 3
    logger.info('Creating segments')
    
    segments = [{'chord': '', 'mini-segments': []}]
    for mini_seg in mini_segments:
        
        if mini_seg['attacks'] >= REQUIRED:
            s = {'chord': '', 'mini-segments': [mini_seg]}
            segments.append(s)
        else:
            last = len(segments) - 1
            segments[last]['mini-segments'].append(mini_seg)
            
    logger.info('Done partitioning, now returning')
    print 'segments: ', segments
    return segments
    
    #for mSegment in mSegments:
    #    
    #    print str(mSegment)
    #
    #    if mSegment['attacks'] >= 3:
    #        s = {'chord': '', 'mSegments': [mSegment]}
    #        segments.append(s)
    #    else:
    #        last = len(segments) - 1
    #        segments[last]['mSegments'].append(mSegment)
    #
    #logger.info('Done partitioning, now returning')
    #return segments