'''
Chord identifier

'''


def get_score(weight, template):
    '''
    Get the score of a weight vector using a given template.
    The template must be ...
    '''
    # sum of pitch-occurences for pitch-classes in template
    positive = 0
    # sum of pitch-occurences for pitch-classes outside template
    negative = 0
    # number of pitch-classes from template that are not "attacked"
    misses = 0
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
    print 'Identifying chords in score with ' + str(len(segments)) + ' segments'
    #print 'No. of pitches:', no_of_pitches

    for segment in segments:
        mini_segments = segment['mini-segments']
        attacks = mini_segments[0]['attacks']
        #print "Attacks: ", attacks
        # first segment may have less attacks than required
        if attacks >= required_attacks:

            # step through mini-segments and collect pitches in weight
            weight = [0] * no_of_pitches
            for mini_segment in mini_segments:

                for pitch in mini_segment['pitches']:
                    #print 'pitch_class:', pitch['pitch_class']
                    weight[pitch['pitch_class']] += 1

            print 'weight:', weight

            #best_scores = []
            #best_score = {'root': 0, 'template': {}, 'score': -1000}
            best_score = -1000
            scores = []

            # for all pitch classes, step through all templates
            for p in range(no_of_pitches):
                for t in chord_templates:
                    template = t['template'][:]
                    template_elems = len(template)
                    #print 'template_elems:', template_elems
                    #if template_elems == attacks:

                    for i in range(template_elems):
                        template[i] = (template[i] + p) % no_of_pitches
                    #print 'template:', template

                    score = get_score(weight, template)

                    #if score > 0:
                    #print 'pitchclass ' + str(p) + ' with template ' + \
                    #str(template) + ' has score is ' + str(score)

                    #print 'score:', score

                    if score > best_score:
                        best_score = score
                        #best_score = {'root': p,
                        #              'template': t,
                        #              'score': score}


            print 'best:', best_score


            # From list of scores: use those who are less than 85% of max. score
            segment_chords = []
            for score in scores:
                if score['score'] / best_score >= min_score:
                    segment_chords.append(score)
