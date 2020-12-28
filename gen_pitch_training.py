import genanki

import random
from shared import *
from mingus.midi import fluidsynth   
from mingus.midi import midi_file_out as MidiFileOut
from mingus.containers import Bar
import time
import os

def main():
  #fluidsynth.init('piano.sf2')
  #fluidsynth.start_recording()
  #fluidsynth.play_Note(48,0,100)
  #fluidsynth.stop_event()
  #time.sleep(1)

  #nc = NoteContainer(["C", ])
  bar = Bar('C')
  bar.place_notes('C', 1)
  MidiFileOut.write_Bar("c.mid", bar)

  os.system('fluidsynth -ni piano.sf2 c.mid -F c.wav -r 44100')
  os.system('ffmpeg -i c.wav -codec:a libmp3lame -qscale:a 2 c.mp3 -y')

  add_card('C', 'C 🎹', '', '[sound:c.mp3]', 0)

  add_all_cards()

  # 

# =================================================

card_priorities = {}

def chord_to_notes(s):
  note, base = sorted([ (n, i) for i, n in enumerate(notes) if s.startswith(n) ], key=lambda x: -len(x[0]))[0]

  chord_notes = [ base ] + list(map(lambda x: (x + base)%12, chord_type_map[s[len(note):]]))

  idx_to_note = { i: n for i,n in enumerate(notes) }
  
  return list(map(idx_to_note.get, chord_notes))

def add_card(q_id, q, a, sound, priority):
  card_priorities.setdefault(priority, [])
  card_priorities[priority].append([ q_id, q, a, sound ])

def add_all_cards():
  for k in sorted(card_priorities.keys()): 
    for i, (q_id, q, a, sound) in enumerate(card_priorities[k]):
      p = '%05d' % k + ' ' + '%05d' % i
      card = QuestionNote(model = my_model, fields = [ p, q_id, q, a, sound ])
      my_deck.add_note(card)

class QuestionNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[1])

random.seed("piano-pitch-training")

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
    {'name': 'Answer'},
    {'name': 'MyMedia'},   
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}{{MyMedia}}',
    }
  ],
    css = style)

my_deck = genanki.Deck(deck_id = deck_id, 
                      name = 'Piano Pitch Training')


main()

package = genanki.Package(my_deck)
package.media_files = [ 'c.mp3' ]

package.write_to_file('piano-pitch-training.apkg')


