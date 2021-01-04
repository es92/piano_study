import genanki
import random
from shared import *

def main():
  scales('major', major_scale, 0)
  chords4(1, 2, 3)

  scales('major pentatonic', major_pentatonic_scale, 4)
  scales('major blues', major_blues_scale, 5)
  scales('minor pentatonic', minor_pentatonic_scale, 6)
  scales('minor blues', minor_blues_scale, 7)

  add_all_cards()

def scales(scale_name, scale, priority):
  for base_i, n in enumerate(notes):
    scale_notes = [ notes[(base_i + n)%12] for n in scale ]
    a = ' | '.join(scale_notes)
    q = n + ' ' + scale_name + ' scale'
    q_id = q
    if scale_name == 'major':
      q_id = n + ' scale'
    add_play_card(q_id, q, a, priority)

def chords4(core_priority, sevenths_priority, complex_priority):
  for n in notes:
    for t in chord_types:
      chord = n + t
      chord_notes = ' | '.join(chord_to_notes(chord))
      if '/' in n:
        q = '<br>'.join(map(lambda x: 'play ' + x + t, n.split('/')))
      else:
        q = 'play ' + n + t

      priority_type = chord_type_priority_map[t]
      priority = {
        'core': core_priority,
        'sevenths': sevenths_priority,
        'complex': complex_priority
      }[priority_type]
      add_card(chord, q, str(chord_notes), priority)

# =================================================

card_priorities = {}

def chord_to_notes(s):
  note, base = sorted([ (n, i) for i, n in enumerate(notes) if s.startswith(n) ], key=lambda x: -len(x[0]))[0]


  chord_notes = [ base ] + list(map(lambda x: (x + base)%12, chord_type_map[s[len(note):]]))

  idx_to_note = { i: n for i,n in enumerate(notes) }
  
  return list(map(idx_to_note.get, chord_notes))

def add_play_card(q_id, q, a, priority):
  add_card(q_id, 'play ' + q, a, priority)

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

random.seed("piano")

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
                      name = 'Piano')


main()

genanki.Package(my_deck).write_to_file('piano.apkg')
