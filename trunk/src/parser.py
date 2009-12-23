from lxml import etree

VERBOSE = False

def get_note_data(note_elem):
    '''
    Retrieve data about a note from a MusicXML note-element. The data
    will be returned in a dictionary
    '''

    if VERBOSE:
        print 'Getting note_data for:\n', etree.dump(note_elem)

    note_data = {'is_chord': False}

    chord_elem = note_elem.find('chord')
    if chord_elem is not None:
        note_data['is_chord'] = True

    pitch_elem = note_elem.find('pitch')
    if pitch_elem is not None:
        note_data['type'] = 'pitch'

        step_elem = pitch_elem.find('step')
        if step_elem is not None:
            note_data['p_step'] = step_elem.text

        octave_elem = pitch_elem.find('octave')
        if octave_elem is not None:
            note_data['p_octave'] = int(octave_elem.text)

        alter_elem = pitch_elem.find('alter')
        if alter_elem is not None:
            note_data['p_alt'] = int(alter_elem.text)

    # TODO: Use unpitched-tag?
    #unpitch_elem = note_elem.find('unpitched')
    #if unpitch_elem is not None:
    #    note_data['type'] = 'unpitched'

    rest_elem = note_elem.find('rest')
    if rest_elem is not None:
        note_data['type'] = 'rest'

    dur_elem = note_elem.find('duration')
    if dur_elem is not None:
        note_data['duration'] = int(dur_elem.text)

    return note_data

def get_part_list(tree):
    '''
    Retrieve a list of the part_elems in the music. The music must be
    represented by a MusicXML-tree.
    '''
    part_list = []
    part_elems = tree.find('part-list')
    for part_elem in part_elems.findall('score-part'):
        id = part_elem.attrib['id']
        name = part_elem.find('part-name').text
        part = {'id': id, 'name': name, 'div': '', 'next_interval': 0}
        part_list.append(part)
    return part_list

def get_part(part_list, part_id):
    '''
    Find a part with a given id in the list of parts
    '''
    for part in part_list:
        if part['id'] == part_id:
            return part
    return None

def find_largest_div(tree):
    '''
    Find the largest divisor in the entire score. Used to specifiy the length
    of intervals that are the length of the shortest note in the score.
    '''
    largest_divisor = 1
    divisions = tree.findall('measure/part/attributes/divisions')
    for d in divisions:
        div = int(d.text)
        if div > largest_divisor:
            largest_divisor = div

    return largest_divisor

def store_rest(intervals, start, length):
    '''
    Store a rest in the list of intervals. The rest will start at
    interval 'start' and last start+length intervals.
    '''
    for i in range(start,start+length):
        if i+1 > len(intervals):
            intervals.append({'attacks': 0, 'pitches': []})

def store_pitch(intervals,pitch, start, length):
    """
    Store a pitch in the list of intervals. The pitch will start at
    interval 'start' and last start+length intervals.
    """
    #print start
    
    for i in range(start,start+length):
        if i+1 > len(intervals):
            intervals.append({'attacks': 0, 'pitches': []})
        intervals[i]['pitches'].append(pitch)
        
    intervals[start]['attacks'] = intervals[start]['attacks'] + 1
    #print str(intervals[start])




def parse_file(file, pitch_classes):
    """
    Parse a file of the MusicXML format.
    
    """
    
    if VERBOSE:
        print 'Parsing', file

    # parse file to a xml-xml_tree datastructure
    #xml_tree = ElementTree.parse(file)
    docFile = open(file, 'r')
    doc = etree.parse(docFile)
    docroot = doc.getroot()

    # check if we need to convert to time-wise format
    if docroot.tag == 'score-partwise':
        xslt_file_name = '../xslt_stylesheets/parttime.xsl'
        xslt_file = open(xslt_file_name, 'r')
        xslt_tree = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_tree)
        xml_tree = transform(doc)
    elif docroot.tag == 'score-timewise':
        xml_tree = doc
    else:
        error = 'Provided file is not MusicXML'
        raise Exception(error)

    # TODO: Below: Consistent looping through children: either by using find() or getchildren() which is faster?

    # the intervals that will be returned
    intervals = []

    # get the list of parts that the score contains
    part_list = get_part_list(xml_tree)
    if VERBOSE:
        print 'Found part_elem-list: ', str(part_list)

    # the current interval
    current_interval = 0

    # find largest divisor
    largest_divisor = find_largest_div(xml_tree)
    if VERBOSE:
        print "Shortest note in score is 1/" + str(4*largest_divisor)

    # current divisor (will be based on the current part)
    current_div = largest_divisor

    # iterate through file
    measures = xml_tree.findall('measure')
    for measure in measures:
        parts = measure.findall('part')
        for part_elem in parts:

            # get id of part
            part_id = part_elem.attrib['id']
            if VERBOSE:
                print '---- part ' + part_elem.attrib['id']
                
            part = get_part(part_list, part_id)
            next_interval = part['next_interval']
            
            if VERBOSE:
                print 'Next interval in this part: ', next_interval

            #---- attributes ----#

            att_elem = part_elem.find('attributes')

            if att_elem is not None:
                divisions = att_elem.find('divisions')
                if divisions is not None:
                    part['div'] = int(divisions.text)
                    #set_part_div(part_list, part_id, int(divisions.text))
                    
            current_div = part['div'] # current divisor in this part


            #---- pitches ----#

            p_children = part_elem.getchildren()
            for p_child in p_children:

                #---- note ----#

                if p_child.tag == 'note':
                    note_data = get_note_data(p_child)

                    # TODO: handle grace notes with no duration?
                    duration = 0
                    if note_data.has_key('duration'):
                        duration = note_data['duration']
                    
                    # how long is the note in terms of a quater note?
                    quater_part = duration / float(current_div)
                    
                    # length in the terms of intervals over which
                    # the note lasts
                    length = int(quater_part * largest_divisor)
                    
                        
                    # TODO: handle rests (have next/current intervals for measures/parts)
                    if note_data['type'] == 'rest':
                        store_rest(intervals, next_interval, length)
                        if VERBOSE:
                            print "Added rest from " + str(next_interval) + " to " \
                            + str(next_interval+length-1)
                        next_interval = next_interval + length
                        
                    elif note_data['type'] == 'pitch':

                        if note_data['is_chord']:
                            pass
                            #print 'Chord note'
                        else:
                            #print "Non-chord note"
                            # the note is not a chord, so the interval that we
                            # place the note in is the next one
                            current_interval = next_interval                                
                            next_interval = current_interval + length                        
                        
                        # pitch alternation
                        alt = 0
                        if note_data.has_key('p_alt'):
                            alt = note_data['p_alt']
                        
                        # pitch (class + octave)
                        # TODO: Support quater-tone sharp?
                        p_class = (pitch_classes[note_data['p_step']] + alt) % 12
                        pitch = {'pitch_class': p_class, 'octave': note_data['p_octave']}
                                
                        # store in intervals list
                        # TODO: handle grace notes with no duration
                        if duration > 0:
                            store_pitch(intervals, pitch, current_interval, length)
                            if VERBOSE:
                                print "Added " + str(pitch) + ' from ' + \
                                str(current_interval) + ' to ' + \
                                str(current_interval+length-1)


                #---- forward/backup ----#

                if p_child.tag == 'forward':
                    duration_elem = p_child.find('duration')
                    duration = int(duration_elem.text)
                    #current_div = get_part_div(part_list, part_id)
                    quater_part = duration / float(current_div)
                    length = int(quater_part * largest_divisor)
                    next_interval = next_interval + length
                    
                    if VERBOSE:
                        print 'Forward with length ' + str(length)

                if p_child.tag == 'backup':
                    duration_elem = p_child.find('duration')
                    duration = int(duration_elem.text)
                    #current_div = get_part_div(part_list, part_id)
                    quater_part = duration / float(current_div)
                    length = int(quater_part * largest_divisor)
                    next_interval = next_interval - length
                    
                    if VERBOSE:
                        print 'Backup with length ' + str(length)
                    
            part['next_interval'] = next_interval
    
    return largest_divisor, intervals

#---- end of parse_file ----#