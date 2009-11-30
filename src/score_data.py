'''
Created on Nov 30, 2009

@author: epb
'''

class ScoreData(object):
    '''
    classdocs
    '''


    def __init__(self, interval_length):
        '''
        Constructor
        '''
        i = 0
        self.intervals = []
    
    
    def insert_pitch(self, pitch, start, length):
        for i in range(start,start+length):
            if i+1 > len(self.intervals):
                self.intervals[i] = []
            self.intervals[i].append(pitch)
    
    #def insert_chord_pitch(self, pitch, length):
    #    pass
        
    def do_backup(self, duration):
        pass
    
    def do_forward(self, duration):
        pass