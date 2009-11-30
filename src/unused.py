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