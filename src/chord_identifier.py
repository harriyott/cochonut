VERBOSE = False

def get_score(weight, template):
    '''
    Get the score of a weight vector using a given template.
    The template must be ...
    '''
    # sum of pitch-occurences for pitch-classes in template
    positive = 0.0
    # sum of pitch-occurences for pitch-classes outside template
    negative = 0.0
    # number of pitch-classes from template that are not "attacked"
    misses = 0.0
    for w in range(len(weight)):
        if w in template:
            if weight[w] == 0:
                misses += 1
            else:
                positive += weight[w]
        else:
            negative += weight[w]
    score = positive - negative - misses
    return score

def identify_chords(segments, chord_templates,
                    required_attacks, no_of_pitches, min_score):
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
            weight = [0] * no_of_pitches
            for mini_segment in mini_segments:
                for pitch in mini_segment['pitches']:
                    weight[pitch['pitch_class']] += 1

            if VERBOSE:
                print 'Identifying chords for segment with weight:', weight

            best_score = -1000
            scores = []

            # for all pitch classes, step through all templates
            for p in range(no_of_pitches):
                for t in chord_templates:
                    template = t['template'][:]
                    template_length = len(template)

                    for i in range(template_length):
                        template[i] = (template[i] + p) % no_of_pitches

                    score = get_score(weight, template)

                    scores.append({'root': p,
                                   'template': t,
                                   'score': score})

                    if score > best_score:
                        best_score = score


            # From list of scores: use those who are less than 85% of max. score
            segment_chords = []
            for score in scores:
                if best_score > 0 and \
                score['score'] / best_score >= min_score:
                    segment_chords.append(score)
             
            if VERBOSE:       
                print 'candidates for segment:', segment_chords
            
            segment['candidates'] = segment_chords
    
    # ----- end of segment in segments ----- #