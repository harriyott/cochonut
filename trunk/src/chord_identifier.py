'''
Chord identifier

'''

"""
pitch classes:
0: C
1: C#, Db
2: D
3: D#, Eb
4: E
5: F
6: F#, Gb
7: G
8: G#, Ab
9: A
10: A#, Bb
11: B
"""

"""
templates:

The digits in 'Templates' correspond to pitch classes 

Number of notes        Name                    Rating        Template
---------------------------------------------------------------------
0                      rest                    15            <>
1                      single note             14            <0>
2                      major 3rd / minor 6th   13            <0 4>
                       minor 3rd / major 6th   12            <0 3>
                       tritone                 11            <0 6>
...
...
...
3                      major triad              9            <0 4 7>
                       minor triad              8            <0 3 7>
                       diminished triad         7            <0 3 6>
...
...

"""

