import genanki
import random
from shared import *
from mingus.midi import fluidsynth   
import time

def main():
  fluidsynth.init('piano.sf2')
  fluidsynth.play_Note(48,0,100)
  time.sleep(1)

  add_all_cards()

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

random.seed("piano-ear-training")

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
                      name = 'Piano Ear Training')


main()

genanki.Package(my_deck).write_to_file('piano-ear-training.apkg')

