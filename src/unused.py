#----------- UNUSED CODE --------------#

#def is_tonic(tonic, chord):
#    return tonic == chord['root']
#
#def is_dominant(tonic, chord):
#    return scale[5] == (chord['root'] - tonic) % 12
#
#def is_subdominant(tonic, chord):
#    return scale[4] == (chord['root'] - tonic) % 12



#def is_dominant_seventh(tonic, chord):
#    return is_dominant(tonic, chord) and \
#    chord['pitches'][(tonic + scale[4]) % 12] != 0
    
#def is_incomplete_dominant(tonic, chord):
#    return is_dominant_seventh(tonic, chord) and \
#    chord['pitches'][(tonic + scale[5]) % 12] == 0
    
    
#def is_dominant_none(tonic, chord):
#    return is_dominant(tonic, chord)
#    
#

#def is_dominant_quater_sixth(tonic, chord):
#    return is_dominant(tonic, chord)


#def is_subdominant_sixth(tonic, chord):
#    return is_subdominant(tonic, chord)

#def is_incomplete_subdominant(tonic, chord):
#    return is_subdominant_sixth(tonic, chord)

#def is_minor_subdominant(tonic, chord):
#    '''
#    Should only be used when the key is major
#    '''
#    return is_subdominant(tonic, chord)

#chord_types = {0: 'tonic',
#               1: 'dominant',
#               2: 'dominant seventh',
#               3: 'subdominant',
#               4: 'tonic parallel',
#               5: 'subdominant parallel',
#               6: 'dominant parallel',
#               7: 'incomplete dominant',
#               8: 'dominant none',
#               9: 'dominant quater sixth',
#               10: 'subdominant sixth',
#               11: 'incomplete subdominant',
#               12: 'minor subdominant'}

#def is_tonic_parallel(tonic, chord, chord_is_minor):
#    if chord_is_minor:
#        return ((tonic - 3) % 12) == chord['root']
#    else:
#        return ((tonic + 3) % 12) == chord['root']
#
#def is_subdominant_parallel(tonic, chord):
#    return is_subdominant(tonic,((chord['root'] + 3) % 12))
#
#def is_dominant_parallel(tonic, chord):
#    return is_dominant(tonic,((chord['root'] + 3) % 12))



#def get_part_div(part_list, id):
#    for part in part_list:
#        if part['id'] == id:
#            return part['div']
#    return None

#def set_part_div(part_list, id, div):
#    #myLogger.info('Setting divisions for part ' + id + ' to ' + str(div))
#    for part in part_list:
#        if part['id'] == id:
#            part['div'] = div

#def set_up_logging():
#    global myLogger
#    myLogger = logging.getLogger('myLogger')
#    myLogger.setLevel(logging.INFO) #handler = logging.FileHandler(LOG_FILE)
#    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
#    formatter = logging.Formatter('%(asctime)s: %(message)s', '%Y-%m-%d %H:%M:%S')
#    handler.setFormatter(formatter)
#    myLogger.addHandler(handler)

#------- unused code  ------#

#    # set current divider
                #    part['div'] = div

                #    # check if this is largest divider
                #    if div > largest_divisions:
                #        largest_divisions = div
                #        myLogger.info('Found new largest divisions element: ' + str(largest_divisions))

                
                #key = att_elem.find('key')
                #if key is not None:
                #    #print 'key:'
                #    fifths = key.find('fifths')
                #    #print 'fifths:', fifths.text
                #
                #    mode = key.find('mode')
                #    if mode is not None:
                #        #print 'mode:', mode.text
                #        pass
                
#if len(mini_segments) >= current + 1:
                            #    # a minimal segment already exists
                            #    pass

                            #else:
                            #    # no minimal segment; create one
                            #    print 'Creating mini seg'


                                #mini_seg = {'attacks': 1, 'length': 0, 'pitches': []}
                                #mini_segments.append(mini_seg)
                                
                                #mini_segments[current]['pitches'] = []
                                #mini_segments[current]['pitches'].append(pitch)
                                #current = current + 1

                                #next_interval = 
                                
# 
                            #current = current - 1
                            
                            # pitch
                            #alt = 0
                            #if note_data.has_key('p_alt'):
                            #    alt = note_data['p_alt']
                            #p_class = get_pitch_class(note_data['p_step'], alt)
                            #pitch = {'pitch': p_class, 'octave': note_data['p_octave']}
                                
                            # store in intervals list
                            #for i in range(current_interval,current_interval+length):
                            #    if i+1 > len(intervals):
                            #        intervals.append([])
                            #    intervals[i].append(pitch)
                            #    
                            #print "Added " + str(pitch) + ' from ' + str(current_interval) + ' to ' + str(current_interval+length)
                            
                            # increment no. of attacks 
                            #a = mini_segments[current]['attacks']
                            #a = a + 1
                            #mini_segments[current]['attacks'] = a
                            
                            #mini_segments[current]['pitches'].append(pitch)
                            #current = current + 1


#for mini_seg in mini_segments:
        
    #    if mini_seg['attacks'] >= required_attacks or \
    #    len(segments) == 0:
    #        s = {'chord': '', 'mini-segments': [mini_seg]}
    #        segments.append(s)
    #    else:
    #        last = len(segments) - 1
    #        segments[last]['mini-segments'].append(mini_seg)
    
#parse(file,ScoreHandler())

#from xml.sax.handler import ContentHandler
#from xml.sax import parse


#                rest = note.find('rest')
    #                if rest is not None:
    #                    #logger.info('rest')
    #                    print 'rest'
    #                    
    #                pitch = note.find('pitch') # TODO: Is more than one pitch per note possible?
    #                if pitch is not None:
    #                #for pitch in pitches:
    #                    
    #                    # step
    #                    step = pitch.find('step')
    #                    if step is not None:
    #                        print 'step', step.text
    #                        
    #                    # octave
    #                    octave = pitch.find('octave')
    #                    if octave is not None:
    #                        print 'octave', octave.text
    #                        
    #                    # alternation
    #                    alter = pitch.find('alter')
    #                    if alter is not None:
    #                        print 'alter', alter.text

    #                duration = note.find('duration')
    #                if duration is not None:
    #                    print 'duration', duration.text

#class Dispatcher:
#    
#    def startElement(self, name, attrs):
#        print 'Found start-tag:', name
#        #logger.info('Found start-tag: ' + name)
#        self.dispatch('start', name, attrs)
#        
#    def endElement(self, name):
#        print 'Found end-tag:', name
#        #logger.info('Found end-tag: ' + name)
#        self.dispatch('end', name)
#        
#    def dispatch(self, prefix, name, attrs=None):
#        mname = prefix + name.capitalize()
#        dname = 'default' + prefix.capitalize()
#        
#        # try to find handler
#        method = getattr(self, mname, None)
#        if callable(method):
#            args = ()
#        else:
#            method = getattr(self, dname, None)
#            args = name,
#            
#        # if we have a start tag, we want to pass the attributes
#        if prefix == 'start':
#            args += attrs,
#            
#        # call the handler
#        if callable(method):
#            method(*args)
#            
#            
#class ScoreHandler(Dispatcher, ContentHandler):
#    
#    def startPitch(self, attrs):
#        self.in_pitch = True
#        
#    def endPitch(self):
#        self.in_pitch = False
#        
#    def startOctave(self, attrs):
#        if self.in_pitch:
#            pass
#            
#    def endOctave(self):
#        if self.in_pitch:
#            pass
#        
#    def startStep(self, attrs):
#        print 'Beginning step'
#        
#    def endStep(self):
#        print 'Step ended'