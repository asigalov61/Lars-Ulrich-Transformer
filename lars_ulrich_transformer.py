# -*- coding: utf-8 -*-
"""Lars_Ulrich_Transformer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i2Woj9BY8PQUECn_V-2X4PXdQcJx6NOX

# Lars Ulrich Transformer (ver. 1.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect. https://www.nscai.gov/

***

#### Project Los Angeles

#### Tegridy Code 2023

***

# (GPU CHECK)
"""

#@title NVIDIA GPU check
!nvidia-smi

"""# (SETUP ENVIRONMENT)"""

#@title Install dependencies
!git clone --depth 1 https://github.com/asigalov61/Lars-Ulrich-Transformer
!pip install huggingface_hub
!pip install torch
!pip install einops
!pip install torch-summary
!pip install sklearn
!pip install tqdm
!pip install matplotlib
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

# Commented out IPython magic to ensure Python compatibility.
#@title Import modules

print('=' * 70)
print('Loading core Lars Ulrich Transformer modules...')

import os
import copy
import pickle
import random
import secrets
import statistics
from time import time
import tqdm

from huggingface_hub import hf_hub_download

print('=' * 70)
print('Loading main Lars Ulrich Transformer modules...')
import torch

# %cd /content/Lars-Ulrich-Transformer

import TMIDIX
from x_transformer import TransformerWrapper, Decoder, AutoregressiveWrapper

# %cd /content/
print('=' * 70)
print('Loading aux Lars Ulrich Transformer modules...')

import matplotlib.pyplot as plt

from torchsummary import summary
from sklearn import metrics

from midi2audio import FluidSynth
from IPython.display import Audio, display

print('=' * 70)
print('Done!')
print('Enjoy! :)')
print('=' * 70)

"""# (LOAD MODEL)"""

#@title Load Lars Ulrich Transformer Small Model

#@markdown Fast model, 32 layers, 201k MIDIs training corpus

full_path_to_model_checkpoint = "/content/Lars-Ulrich-Transformer/Model/Lars_Ulrich_Transformer_Small_Trained_Model_51000_steps_0.5062_loss_0.8283_acc.pth" #@param {type:"string"}
display_tokens_embeddings = False #@param {type:"boolean"}

print('=' * 70)
print('Loading Lars Ulrich Transformer Small Pre-Trained Model...')
print('Please wait...')
print('=' * 70)
hf_hub_download(repo_id='asigalov61/Lars-Ulrich-Transformer', 
                filename='Lars_Ulrich_Transformer_Small_Trained_Model_51000_steps_0.5062_loss_0.8283_acc.pth', 
                local_dir='/content/Lars-Ulrich-Transformer/Model/', 
                local_dir_use_symlinks=False)
print('=' * 70)
print('Instantiating model...')

SEQ_LEN = 2048

# instantiate the model

model = TransformerWrapper(
    num_tokens = 659,
    max_seq_len = SEQ_LEN,
    attn_layers = Decoder(dim = 1024, depth = 32, heads = 8)
)

model = AutoregressiveWrapper(model)

model = torch.nn.DataParallel(model)

model.cuda()
print('=' * 70)

print('Loading model checkpoint...')

model.load_state_dict(torch.load(full_path_to_model_checkpoint))
print('=' * 70)

model.eval()

print('Done!')
print('=' * 70)

# Model stats
print('Model summary...')
summary(model)


if display_tokens_embeddings: 
  # Plot Token Embeddings
  tok_emb = model.module.net.token_emb.emb.weight.detach().cpu().tolist()

  tok_emb1 = []

  for t in tok_emb:
      tok_emb1.append([abs(statistics.median(t))])

  cos_sim = metrics.pairwise_distances(
    tok_emb1, metric='euclidean'
  )
  plt.figure(figsize=(7, 7))
  plt.imshow(cos_sim, cmap="inferno", interpolation="nearest")
  im_ratio = cos_sim.shape[0] / cos_sim.shape[1]
  plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
  plt.xlabel("Position")
  plt.ylabel("Position")
  plt.tight_layout()
  plt.plot()
  plt.savefig("/content/Lars-Ulrich-Transformer-Small-Tokens-Embeddings-Plot.png", bbox_inches="tight")

"""# (GENERATE)

# (IMPROV)
"""

#@title Improv Generation

#@markdown Improv settings

number_of_tokens_tp_generate = 500 #@param {type:"slider", min:30, max:2045, step:5}
number_of_batches_to_generate = 1 #@param {type:"slider", min:1, max:16, step:1}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
render_MIDI_to_audio = False #@param {type:"boolean"}

print('=' * 70)
print('Lars Ulrich Transformer Improv Model Generator')
print('=' * 70)

outy = [658, 658, 658, 658, 658]

print('Selected Improv sequence:')
print(outy)
print('=' * 70)

inp = [outy] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

out = model.module.generate(inp, 
                      number_of_tokens_tp_generate, 
                      temperature=temperature, 
                      return_prime=True, 
                      verbose=True)

out0 = out.tolist()

print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================

print('Rendering results...')

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out1) != 0:
    
      song = out1
      song_f = []

      time = 0
      dur = 0
      vel = 90
      pitch = 0
      channel = 0
                      
      for ss in song:
          
        if ss >= 0 and ss < 10:
            
            channel = ss
        
        if ss >= 10 and ss < 266:

            time += (ss-10) * 8
          
        if ss >= 266 and ss < 394:
            
            dur = (ss-266) * 32
          
        if ss >= 394 and ss < 650:
      
            pitch = ((ss-394) % 128)
            
        if ss >= 650 and ss < 658:
            
            vel = ((ss-650)+1) * 15

            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'Lars Ulrich Transformer',  
                                                          output_file_name = '/content/Lars-Ulrich-Transformer-Composition_'+str(i), 
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 19, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)


      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/Lars-Ulrich-Transformer-Composition_'+str(i)

      x = []
      y =[]
      c = []

      colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

      for s in song_f:
        x.append(s[1] / 1000)
        y.append(s[4])
        c.append(colors[s[3]])

      if render_MIDI_to_audio:
        FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
        display(Audio(str(fname + '.wav'), rate=16000))

      plt.figure(figsize=(14,5))
      ax=plt.axes(title=fname)
      ax.set_facecolor('black')

      plt.scatter(x,y, c=c)
      plt.xlabel("Time")
      plt.ylabel("Pitch")
      plt.show()

"""# (CUSTOM MIDI)"""

#@title Load Seed MIDI
select_seed_MIDI = "Sharing The Night Together" #@param ["Nothing Else Matters", "Honesty", "House Of The Rising Sun", "Sharing The Night Together"]
full_path_to_custom_seed_MIDI = "" #@param {type:"string"}
render_MIDI_to_audio = False #@param {type:"boolean"}

if full_path_to_custom_seed_MIDI == '':
  f = '/content/Lars-Ulrich-Transformer/Seeds/'+select_seed_MIDI+'.mid'

else:
  f = full_path_to_custom_seed_MIDI

print('=' * 70)
print('Lars Ulrich Transformer Seed MIDI Loader')
print('=' * 70)
print('Loading seed MIDI...')
print('=' * 70)
print('File:', f)
print('=' * 70)

#=======================================================
# START PROCESSING

melody_chords_f = []
melody_chords_f1 = []
chords = []

# Convering MIDI to ms score with MIDI.py module
score = TMIDIX.midi2ms_score(open(f, 'rb').read())

# INSTRUMENTS CONVERSION CYCLE
events_matrix = []
itrack = 1
patches = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

patch_map = [
            [0, 1, 2, 3, 4, 5, 6, 7], # Piano 
            [24, 25, 26, 27, 28, 29, 30], # Guitar
            [32, 33, 34, 35, 36, 37, 38, 39], # Bass
            [40, 41], # Violin
            [42, 43], # Cello
            [16, 17, 18, 19, 20], # Organ
            [56, 57, 58, 59, 60], # Trumpet
            [64, 65, 66, 67, 68, 69, 70, 71], # Sax
            [72, 73, 74, 75, 76, 77, 78], # Flute
            [-1], # Drums            
            ]

while itrack < len(score):
    for event in score[itrack]:         
        if event[0] == 'note' or event[0] == 'patch_change':
            events_matrix.append(event)
    itrack += 1

events_matrix.sort(key=lambda x: x[1])

events_matrix1 = []

for event in events_matrix:
        if event[0] == 'patch_change':
            patches[event[2]] = event[3]

        if event[0] == 'note':
            event.extend([patches[event[3]]])
            once = False
            
            for p in patch_map:
                if event[6] in p and event[3] != 9: # Except the drums
                    event[3] = patch_map.index(p)
                    once = True
                    
            if not once and event[3] != 9: # Except the drums
                event[3] = 0 # All other instruments/patches channel
                event[5] = max(80, event[5])
                
            if event[3] < 10: # We won't write chans 12-16 for now...
                events_matrix1.append(event)

if len(events_matrix1) > 0:           
  if min([e[1] for e in events_matrix1]) >= 0 and min([e[2] for e in events_matrix1]) > 0:
    
    #=======================================================
    # PRE-PROCESSING

    # checking number of instruments in a composition
    instruments_list_without_drums = list(set([y[3] for y in events_matrix1 if y[3] != 9]))

    if len(events_matrix1) > 0 and len(instruments_list_without_drums) > 0:

      # recalculating timings
      for e in events_matrix1:
          e[1] = int(e[1] / 8) # Max 2 seconds for start-times
          e[2] = int(e[2] / 32) # Max 4 seconds for durations

      # Sorting by pitch, then by start-time
      events_matrix1.sort(key=lambda x: x[4], reverse = True)
      events_matrix1.sort(key=lambda x: x[3])
      events_matrix1.sort(key=lambda x: x[1])

      #=======================================================
      # FINAL PRE-PROCESSING

      melody_chords = []
      melody_chords_d = []

      pe = events_matrix1[0]
      ped = events_matrix1[0]

      for e in events_matrix1:

          if e[3] != 9:

            # Cliping all values...
            time = max(0, min(255, e[1]-pe[1]))             
            dur = max(1, min(127, e[2]))
            cha = max(0, min(9, e[3]))
            ptc = max(1, min(127, e[4]))
            
            # Shifting drums pitches
            if cha != 9:                
                aug_ptc = ptc
            else:
                aug_ptc = ptc + 128

            # Calculating octo-velocity
            vel = max(8, min(127, e[5]))
            velocity = round(vel / 15)-1

            # Writing final note 
            melody_chords.append([time, dur, cha, aug_ptc, velocity])

            pe = e

          # Cliping all values...
          time = max(0, min(255, e[1]-ped[1]))             
          dur = max(1, min(127, e[2]))
          cha = max(0, min(9, e[3]))
          ptc = max(1, min(127, e[4]))
          
          # Shifting drums pitches
          if cha != 9:                
              aug_ptc = ptc
          else:
              aug_ptc = ptc + 128

          # Calculating octo-velocity
          vel = max(8, min(127, e[5]))
          velocity = round(vel / 15)-1

          # Writing final note 
          melody_chords_d.append([time, dur, cha, aug_ptc, velocity])

          ped = e

      if len([y for y in melody_chords if y[2] != 9]) > 12: # Filtering out tiny/bad MIDIs...

        times = [y[0] for y in melody_chords[12:]]
        avg_time = sum(times) / len(times)

        times_list = list(set(times))

        mode_dur = statistics.mode([y[1] for y in melody_chords if y[2] != 9])

        instruments_list = list(set([y[2] for y in melody_chords]))
        num_instr = len(instruments_list)

        if instruments_list != [9]: # Filtering out bad MIDIs...
            if avg_time < 64 and mode_dur < 64: # Filtering out bad MIDIs...
              if 0 in times_list: # Filtering out (mono) melodies MIDIs

                  #=======================================================
                  # FINAL PROCESSING
                  #=======================================================

                  # Break between compositions / Intro seq

                  melody_chords_f.extend([658, 658, 658, 658, 658])

                  #=======================================================

                  # TOTAL DICTIONARY SIZE 658+1=659

                  #=======================================================
                  # MAIN PROCESSING CYCLE
                  #=======================================================

                  for m in melody_chords_d:
                    
                      # WRITING EACH NOTE HERE
                      time = m[0]                                  
                      dur = m[1]
                      cha = m[2]
                      ptc = m[3]
                      vel = m[4]

                      melody_chords_f.extend([cha, time+10, dur+266, ptc+394, vel+650])
                      melody_chords_f1.append([cha, time+10, dur+266, ptc+394, vel+650])

                  cho = []

                  for m in melody_chords:

                      # WRITING EACH CHORD HERE
                      time = m[0]                                  
                      dur = m[1]
                      cha = m[2]
                      ptc = m[3]
                      vel = m[4]

                      if time == 0:
                        cho.append([cha, time+10, dur+266, ptc+394, vel+650])
                      else:
                        if len(cho) > 0:
                          chords.append(cho)
                        cho = []
                        cho.append([cha, time+10, dur+266, ptc+394, vel+650])
                      
                  if len(cho) > 0:
                      chords.append(cho)

#=======================================================
  
song = melody_chords_f

song_f = []

time = 0
dur = 0
vel = 90
pitch = 0
channel = 0
                
for ss in song:
    
  if ss >= 0 and ss < 10:
      
      channel = ss
  
  if ss >= 10 and ss < 266:

      time += (ss-10) * 8
    
  if ss >= 266 and ss < 394:
      
      dur = (ss-266) * 32
    
  if ss >= 394 and ss < 650:

      pitch = ((ss-394) % 128)
      
  if ss >= 650 and ss < 658:
      
      vel = ((ss-650)+1) * 15

      song_f.append(['note', time, dur, channel, pitch, vel ])

detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                      output_signature = 'Lars Ulrich Transformer',  
                                                      output_file_name = '/content/Lars-Ulrich-Transformer-Seed-Composition',
                                                      track_name='Project Los Angeles',
                                                      list_of_MIDI_patches=[0, 24, 32, 40, 42, 19, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0],
                                                      number_of_ticks_per_quarter=500)
    
#=======================================================

print('=' * 70)
print('Composition stats:')
print('Composition has', len([y for y in melody_chords_d if y[0] != 0]), 'chords')
print('Composition has', len(melody_chords_f1), 'notes')
print('Composition has', len(melody_chords_f), 'tokens')
print('=' * 70)

print('Displaying resulting composition...')
print('=' * 70)

fname = '/content/Lars-Ulrich-Transformer-Seed-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

if render_MIDI_to_audio:
  FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
  display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

"""# (COUNTINUATION)"""

#@title Standard/Simple Continuation

#@markdown Generation settings

number_of_prime_tokens = 500 #@param {type:"slider", min:5, max:2045, step:5}
number_of_tokens_to_generate = 500 #@param {type:"slider", min:30, max:2045, step:5}
number_of_batches_to_generate = 1 #@param {type:"slider", min:1, max:16, step:1}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}

#@markdown Other settings
include_prime_tokens_in_generated_output = True #@param {type:"boolean"}
allow_model_to_stop_generation_if_needed = False #@param {type:"boolean"}
render_MIDI_to_audio = False #@param {type:"boolean"}

print('=' * 70)
print('Lars Ulrich Transformer Standard Model Generator')
print('=' * 70)

if allow_model_to_stop_generation_if_needed:
  min_stop_token = 658
else:
  min_stop_token = None

outy = melody_chords_f[5:number_of_prime_tokens]

inp = [outy] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

out = model.module.generate(inp, 
                      number_of_tokens_to_generate, 
                      temperature=temperature, 
                      return_prime=include_prime_tokens_in_generated_output, 
                      eos_token=min_stop_token, 
                      verbose=True)

out0 = out.tolist()
print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================
print('Rendering results...')

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out) != 0:
      
      song = out1
      song_f = []

      time = 0
      dur = 0
      vel = 90
      pitch = 0
      channel = 0
                      
      for ss in song:
          
        if ss >= 0 and ss < 10:
            
            channel = ss
        
        if ss >= 10 and ss < 266:

            time += (ss-10) * 8
          
        if ss >= 266 and ss < 394:
            
            dur = (ss-266) * 32
          
        if ss >= 394 and ss < 650:
      
            pitch = ((ss-394) % 128)
            
        if ss >= 650 and ss < 658:
            
            vel = ((ss-650)+1) * 15

            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'Lars Ulrich Transformer',  
                                                          output_file_name = '/content/Lars-Ulrich-Transformer-Composition_'+str(i), 
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 19, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)


      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/Lars-Ulrich-Transformer-Composition_'+str(i)

      x = []
      y =[]
      c = []

      colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

      for s in song_f:
        x.append(s[1] / 1000)
        y.append(s[4])
        c.append(colors[s[3]])

      if render_MIDI_to_audio:
        FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
        display(Audio(str(fname + '.wav'), rate=16000))

      plt.figure(figsize=(14,5))
      ax=plt.axes(title=fname)
      ax.set_facecolor('black')

      plt.scatter(x,y, c=c)
      plt.xlabel("Time")
      plt.ylabel("Pitch")
      plt.show()

"""# (DRUMS INPAINTING)"""

#@title Inpaint drum track

#@markdown NOTE: You can stop the generation at any time to render partial results

number_of_prime_chords = 8 #@param {type:"slider", min:1, max:64, step:1}

#@markdown Number of generation attempts per chord option helps make drums more complex and detailed but it will slow down the generation proportionally and may also produce an overloaded drum track at higher settings

number_of_generation_attempts_per_chord = 3 #@param {type:"slider", min:1, max:8, step:1}

#@markdown Memory tokens control long-term structure of the generated drum track at the cost of the generation speed

number_of_memory_tokens = 500 #@param {type:"slider", min:50, max:2045, step:5}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}
render_MIDI_to_audio = False #@param {type:"boolean"}


print('=' * 70)
print('Lars Ulrich Transformer Drums Inpainting Model Generator')
print('=' * 70)

outy = []

for c in chords[:number_of_prime_chords]:
  for cc in c:
    outy.extend(cc)

next_chord_time = 0
cur_time = 0
chord_time_delta = 0

for i in tqdm.tqdm(range(number_of_prime_chords, len(chords))):
  
  try:

    for c in chords[i]:
      if c[0] != 9:
        
        if chord_time_delta > 0:
          if (c[1]-10) != 0:

            adjusted_note = copy.deepcopy(c)
            adjusted_note[1] = chord_time_delta+10
            
            outy.extend(adjusted_note)
            chord_time_delta = 0
        
        else:
          outy.extend(c)
    
    if (i+1) != len(chords):
      next_chord_time = chords[i+1][0][1]-10
    else:
      next_chord_time = 255

    cur_time = 0
    tries = 0

    while cur_time < next_chord_time and tries < number_of_generation_attempts_per_chord:

      outy.extend([9])

      inp = [outy[-number_of_memory_tokens:]]
      inp = torch.LongTensor(inp).cuda()

      out = model.module.generate(inp, 
                            4, 
                            temperature=temperature, 
                            return_prime=False, 
                            eos_token=None, 
                            verbose=False)

      out0 = out.tolist()[0]

      cur_time += (out0[0]-10)

      if cur_time < next_chord_time:
        chord_time_delta = next_chord_time - cur_time
        outy.extend(out0)
      else:
        cur_time -= (out0[0]-10)


      tries += 1
  
  except KeyboardInterrupt:
    break

  except:
    break

print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================
print('Rendering results...')
print('=' * 70)

out1 = outy

print('Sample INTs', out1[:12])
print('=' * 70)

if len(out) != 0:
    
    song = out1
    song_f = []

    time = 0
    dur = 0
    vel = 90
    pitch = 0
    channel = 0
                    
    for ss in song:
        
      if ss >= 0 and ss < 10:
          
          channel = ss
      
      if ss >= 10 and ss < 266:

          time += (ss-10) * 8
        
      if ss >= 266 and ss < 394:
          
          dur = (ss-266) * 32
        
      if ss >= 394 and ss < 650:
    
          pitch = ((ss-394) % 128)
          
      if ss >= 650 and ss < 658:
          
          vel = ((ss-650)+1) * 15

          song_f.append(['note', time, dur, channel, pitch, vel ])

    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Lars Ulrich Transformer',  
                                                        output_file_name = '/content/Lars-Ulrich-Transformer-Composition', 
                                                        track_name='Project Los Angeles',
                                                        list_of_MIDI_patches=[0, 24, 32, 40, 42, 19, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0],
                                                        number_of_ticks_per_quarter=500)


    print('=' * 70)
    print('Displaying resulting composition...')
    print('=' * 70)

    fname = '/content/Lars-Ulrich-Transformer-Composition'

    x = []
    y =[]
    c = []

    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

    for s in song_f:
      x.append(s[1] / 1000)
      y.append(s[4])
      c.append(colors[s[3]])

    if render_MIDI_to_audio:
      FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
      display(Audio(str(fname + '.wav'), rate=16000))

    plt.figure(figsize=(14,5))
    ax=plt.axes(title=fname)
    ax.set_facecolor('black')

    plt.scatter(x,y, c=c)
    plt.xlabel("Time")
    plt.ylabel("Pitch")
    plt.show()

"""# Congrats! You did it! :)"""