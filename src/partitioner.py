'''
Partitioner

'''

def partitionScore(mSegments, logger):
    logger.info('Partitioning score with ' + str(len(mSegments)) + ' minimal segments')
    segments = [{'chord': '', 'mSegments': []}]
    for mSegment in mSegments:
        
        print str(mSegment)

        if mSegment['attacks'] >= 3:
            s = {'chord': '', 'mSegments': [mSegment]}
            segments.append(s)
        else:
            last = len(segments) - 1
            segments[last]['mSegments'].append(mSegment)

    logger.info('Done partitioning, now returning')
    return segments