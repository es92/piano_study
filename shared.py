

notes = [ 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B' ]
#          0     1       2     3       4    5      6      7      8      9     10      11

major_scale = [ 0, 2, 4, 5, 7, 9, 11 ]
natural_minor_scale = [ 0, 2, 3, 5, 7, 8, 10 ]
harmonic_minor_scale = [ 0, 2, 3, 5, 7, 8, 11 ]

major_blues_scale = [ 0, 2, 3, 4, 7, 9 ]
minor_blues_scale = [ 0, 3, 5, 6, 7, 10 ]
major_pentatonic_scale = [ 0, 2, 4, 7, 9 ]
minor_pentatonic_scale = [ 0, 3, 5, 7, 10]

chord_types = [ 'maj', 'min', 'dim', 'aug', '6', '7', 'maj7', 'min7', '7sus4', 'maj7sus4', 'min7b5', 'dim7', 'minmaj7', 'min6', 'aug7' ]

chord_type_map = {
  'maj': [ 4, 7 ],
  'min': [ 3, 7 ],
  'dim': [ 3, 6 ],
  'aug': [ 4, 8],
  '6': [  4, 7, 9 ],
  '7': [ 4, 7, 10 ],
  'maj7': [ 4, 7, 11 ],
  'min7': [ 3, 7, 10 ],
  '7sus4': [ 5, 7, 10 ],
  'maj7sus4': [ 5, 7, 11 ],
  'min7b5': [ 3, 6, 10 ],
  'dim7': [ 3, 6, 9 ],
  'minmaj7': [ 3, 7, 11 ],
  'min6': [ 3, 7, 9 ],
  'aug7': [ 4, 8, 10 ],
}

chord_type_priority_map = {
  'maj': 'core',
  'min': 'core',
  'dim': 'sevenths',
  'aug': 'sevenths',
  '6': 'sevenths',
  '7': 'sevenths',
  'maj7': 'sevenths',
  'min7': 'sevenths',
  '7sus4': 'complex',
  'maj7sus4': 'complex',
  'min7b5': 'complex',
  'dim7': 'complex',
  'minmaj7': 'complex',
  'min6': 'complex',
  'aug7': 'complex',
}
