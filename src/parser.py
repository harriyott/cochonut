"""
Created on Nov 18, 2009

@author: epb
"""

from xml.etree import ElementTree

def parse_file(file, logger):
    """
    Parse a file of the MusicXML format.
    
    """
    
    global myLogger
    myLogger = logger
    
    myLogger.info('Parsing ' + file)    
    
    tree = ElementTree.parse(file)
    
    # check that we have MusicXML
    root = tree.getroot()
    if root.tag != 'score-partwise' and root.tag != 'score-timewise':
        error = 'Provided file is not MusicXML'
        myLogger.error(error)
        raise Exception(error)
    
    # TODO: convert to score-timewise?? (lxml)
    
    # TODO: Only supporting part-wise
    
    # TODO: Below: Consistent looping through children: either by using find() or getchildren()
    
    largest_divisions = 1
    data = []
    
    # iterate through file
    parts = tree.findall('part')
    for part in parts:
        print 'part', part.attrib['id']
        measures = part.findall('measure')
        
        for measure in measures:
            print 'measure', measure.attrib['number']
            
            
            #---- attributes ----#
            
            attributes = measure.find('attributes')
            
            if attributes is not None:
                divisions = attributes.find('divisions')
                if divisions is not None:
                    print 'divisions:', divisions.text
                    if int(divisions.text) > largest_divisions:
                        largest_divisions = int(divisions.text)
                        myLogger.info('Found new largest divisions element: ' + str(largest_divisions))
                        
                key = attributes.find('key')
                if key is not None:
                    print 'key:'
                    fifths = key.find('fifths')
                    print 'fifths:', fifths.text
                    
                    mode = key.find('mode')
                    if mode is not None:
                        print 'mode:', mode.text
            
            
            #---- notes ----#
            
            #notes = measure.findall('m_child')
            measure_children = measure.getchildren()
            for m_child in measure_children:
                
                #---- note ----#
                
                if m_child.tag == 'note':
                    print 'note:'
                    
                    note_children = m_child.getchildren()
                    for n_child in note_children:
                        
                        if n_child.tag == 'chord':
                            print 'this note is part of a chord'
                            
                        if n_child.tag == 'pitch':
                            
                            pitch_children = n_child.getchildren()
                            
                            for p_child in pitch_children:
                                
                                # step (A-G)
                                #step = n_child.find('step')
                                #if step is not None:
                                if p_child.tag == 'step':
                                    print 'step', p_child.text
                                    
                                # octave (0-9)
                                #octave = n_child.find('octave')
                                #if octave is not None:
                                elif p_child.tag == 'octave':
                                    print 'octave', p_child.text
                                    
                                # alternation
                                #alter = n_child.find('alter')
                                #if alter is not None:
                                elif p_child.tag == 'alter':
                                    print 'alter', p_child.text
                                
                        elif n_child.tag == 'unpitched':
                            print '??'
                            
                        elif n_child.tag == 'rest':
                            print 'this note is a rest'
                            
                        if n_child.tag == 'duration':
                            print 'duration', n_child.text
                
                #---- forward/backup ----#
                
                if m_child.tag == 'forward':
                    print 'forward:'
                    
                    duration = m_child.find('duration')
                    print 'duration:', duration.text
                    
                if m_child.tag == 'backup':
                    print 'backup:'
                    
                    duration = m_child.find('duration')
                    print 'duration:', duration.text
                    
    return data
    
#---- end of parse_file ----#




#----------- UNUSED CODE --------------#

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
            
        