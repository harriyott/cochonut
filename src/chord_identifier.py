VERBOSE = False

def get_score(weight, template):
    '''
    Get the score of a weight vector using a given template.
    The template must be adjusted to a given root/template combination
    before it is passed to the function, fx. the template [9, 1, 4]
    represents an A-major.
    '''
    # sum of pitch-occurences for pitch-classes in template
    positives = 0.0
    # sum of pitch-occurences for pitch-classes outside template
    negatives = 0.0
    # number of pitch-classes from template that are not present in weight-vector
    misses = 0.0
    for w in range(len(weight)):
        if w in template:
            if weight[w] == 0:
                misses += 1
            else:
                positives += weight[w]
        else:
            negatives += weight[w]
    return positives - (negatives + misses)


def identify_chords(segments, chord_templates,
                    required_attacks, min_score):
    '''
    Identify the chords in a list of segments.
    '''
    
    if VERBOSE:
        print 'Identifying chords in score with ' + \
        str(len(segments)) + ' segments'

    for segment in segments:
        mini_segments = segment['mini-segments']
        if segment['possible_chord']: # the first segment may not have enough note-attacks

            # step through mini-segments and collect pitches in weight
            weight = [0] * 12
            for mini_segment in mini_segments:
                for pitch in mini_segment['pitches']:
                    weight[pitch['pitch_class']] += 1

            if VERBOSE:
                print 'Identifying chords for segment with weight:', weight

            best_score = -1000
            scores = []

            # for all pitch classes, step through all templates
            for p in range(12):
                for t in chord_templates:
                    template = t['pattern'][:]
                    template_length = len(template)

                    for i in range(template_length):
                        template[i] = (template[i] + p) % 12

                    score = get_score(weight, template)

                    # append a chord with the found score
                    scores.append({'root': p,
                                   'template': t,
                                   'pitches': weight,
                                   'score': score})

                    if score > best_score:
                        best_score = score


            # From list of scores: use those who are more
            # than min_score of the highest score
            segment_chords = []
            for score in scores:
                if best_score > 0 and \
                score['score'] / best_score >= min_score:
                    segment_chords.append(score)
             
            if VERBOSE:       
                print 'candidates for segment:', segment_chords
            
            segment['candidates'] = segment_chords
