import genanki
import random
from shared import *
from mingus.containers import Bar
import mingus.extra.lilypond as LilyPond

def main():

  scale_notes('major', major_scale, 0)
  scale_notes('natural_minor', natural_minor_scale, 2)
  scale_notes('harmonic_minor', harmonic_minor_scale, 4)

  scale_diatonic('major', major_scale, 0)
  scale_diatonic('natural minor', natural_minor_scale, 2)
  scale_diatonic('harmonic minor', harmonic_minor_scale, 4)

  where_to_find('major', major_scale, chord_types[0:2], 1)
  where_to_find('major', major_scale, chord_types[2:7], 1)
  where_to_find('major', major_scale, chord_types[7:], 1)

  where_to_find('natural_minor', natural_minor_scale, chord_types[0:2], 3)
  where_to_find('natural_minor', natural_minor_scale, chord_types[2:7], 3)
  where_to_find('natural_minor', natural_minor_scale, chord_types[7:], 3)

  where_to_find('harmonic_minor', harmonic_minor_scale, chord_types[0:2], 5)
  where_to_find('harmonic_minor', harmonic_minor_scale, chord_types[2:7], 5)
  where_to_find('harmonic_minor', harmonic_minor_scale, chord_types[7:], 5)

  scale_notes('major_pentatonic', major_pentatonic_scale, 6)
  scale_notes('major_blues', major_blues_scale, 7)
  scale_notes('minor_pentatonic', minor_pentatonic_scale, 8)
  scale_notes('minor_blues', minor_blues_scale, 9)

  b = Bar()
  b + "C"
  b + "E"
  b + "G"
  b + "B"
  bar = LilyPond.from_Bar(b)
  print(bar)
  # echo '{ \time 4/4 \key c \major c'4 e'4 g'4 b'4 }' | lilypond --png -o out.png -dpreview -#



  add_all_cards()

def scale_diatonic(scale_name, scale, priority):
  for i, n in enumerate(scale):
    types = []
    for t in chord_types:
      type_notes = chord_type_map[t]
      notes_off_base = [ n ] + [ (x + n) % 12 for x in type_notes ]
      if all([ x in scale for x in notes_off_base ]):
        priority_type = chord_type_priority_map[t]
        types.append(t)
    q = 'chords at ' + scale_name + ' scale degree ' + str(i+1)
    add_card(q, q, '<br>'.join(types), priority)

def where_to_find(scale_name, scale, chords, priority):
  for t in chords:
    type_notes = chord_type_map[t]
    scales = [ major_scale, natural_minor_scale, harmonic_minor_scale ]
    scale_names = [ 'major', 'natural minor', 'harmonic minor' ]
    places = []
    for i, n in enumerate(scale):
      notes_off_base = [ n ] + [ (x + n) % 12 for x in type_notes ]
      if all([ x in scale for x in notes_off_base ]):
        places.append(str(i+1))
    q = 'where can you find a ' + t + ' chord in the ' + scale_name + ' scale?'
    add_card(q, q, '<br>'.join(places), priority)

def scale_notes(scale_name, scale, priority):
  for base_i, base in enumerate(notes):
    for i, n in enumerate(scale):
      note = notes[(base_i + n)%12]
      q = 'what note is the ' + str(i+1) + ' degree of ' + base + ' ' + scale_name + '?'
      add_card(q, q, '<br>'.join(note.split('/')), priority)

# =================================================

card_priorities = {}

def chord_to_notes(s):
  note, base = sorted([ (n, i) for i, n in enumerate(notes) if s.startswith(n) ], key=lambda x: -len(x[0]))[0]

  chord_notes = [ base ] + list(map(lambda x: (x + base)%12, chord_type_map[s[len(note):]]))

  idx_to_note = { i: n for i,n in enumerate(notes) }
  
  return list(map(idx_to_note.get, chord_notes))

def add_card(q_id, q, a, priority):
  card_priorities.setdefault(priority, [])
  card_priorities[priority].append([ q_id, q, a ])

def add_all_cards():
  for k in sorted(card_priorities.keys()): 
    for i, (q_id, q, a) in enumerate(card_priorities[k]):
      p = '%05d' % k + ' ' + '%05d' % i
      card = QuestionNote(model = my_model, fields = [ p, q_id, q, a ])
      my_deck.add_note(card)

class QuestionNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[1])

random.seed("piano-theory")

model_id = random.randrange(1 << 30, 1 << 31)
deck_id = random.randrange(1 << 30, 1 << 31)

style = """
.card {
 font-family: times;
 font-size: 30px;
 text-align: center;
 color: black;
 background-color: white;
}
"""

my_model = genanki.Model(
  model_id,
  'Simple Model',
  fields=[
    {'name': 'priority'},
    {'name': 'q_id'},
    {'name': 'Question'},
    {'name': 'Answer'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }
  ],
    css = style)

my_deck = genanki.Deck(deck_id = deck_id, 
                      name = 'Piano Theory')


main()

genanki.Package(my_deck).write_to_file('piano-theory.apkg')

