import random 
import pandas as pd
from pydub import AudioSegment
import matplotlib as plt
import librosa
import math
meta_url = "C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\meta.txt"
meta_pd = pd.read_csv(meta_url, sep="\t", names=["file_name","class_type","scene"])

def pitch(file_path):
  original_file_class, original_file_scene = find_attributes_from_path(file_path)
  original_audio, sr = librosa.load(file_path)
  semi = int(random.randint(-12,12))
  pitched = librosa.effects.pitch_shift(original_audio, sr,semi)
  return pitched, original_file_class, original_file_scene


def shuffler(file_path, cuts, waveform=False):
    file_class, file_scene = find_attributes_from_path(file_path)
    #print(l_class)
    audio = AudioSegment.from_file(file_path)
    seg_len = len(audio) // cuts
    audio_container = []
    
    for i in range(0, cuts):
        if i == 0:
          audio_container.append(audio[0:seg_len])
        else:
          start = seg_len * i
          end = seg_len * (i+1)
          audio_container.append(audio[start:end])
         
    random.shuffle(audio_container)
    
    new_res = sum(audio_container)
    if waveform:
      p = new_res.get_array_of_samples()
      plt.plot(p)

    return new_res, file_class, file_scene
  
    
def find_attributes_from_path(file_path):
  raw_file = file_path.split("\\")[-1]
  location = "audio/" + raw_file
  #print(raw_file)
  #meta_pd = pd.read_csv(meta_url, sep="\t", names=["file_name","class_type","scene"])
  x = meta_pd[meta_pd["file_name"].str.contains(location)]  #print(row["file_name"])
  result_class = x.iloc[0]["class_type"]
  result_scene = x.iloc[0]["scene"]
  return result_class, result_scene


def get_random_from_class(class_type):
  meta_url = "C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\meta.txt"
  x = meta_pd[meta_pd["class_type"].str.contains(class_type)]  #print(row["file_name"])
  return x.sample()

def mixer(file_path, cuts, waveform=False, mix=2):
  original_file_class, original_file_scene = find_attributes_from_path(file_path)
  original_audio = AudioSegment.from_file(file_path)
  
  seg_len = len(original_audio) // cuts
  original_container = []
  
  for i in range(0, cuts):
    if i == 0:
      original_container.append(original_audio[0:seg_len])
    else:
      start = seg_len * i
      end = seg_len * (i+1)
      original_container.append(original_audio[start:end])
  random.shuffle(original_container)
  sample_container = []
  sample_row = get_random_from_class(original_file_class)
  sample_file = str(sample_row.iloc[0]["file_name"].split("/")[-1])
  sample_path = "C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\audio\\" + sample_file
  #print(sample_path)
  #print(random.randint(0,cuts-1))
  sample_class, sample_scene = find_attributes_from_path(sample_path)
  sample_audio = AudioSegment.from_file(sample_path)
  
  for i in range(0, cuts):
    if i == 0:
      sample_container.append(sample_audio[0:seg_len])
    else:
      start = seg_len * i
      end = seg_len * (i+1)
      sample_container.append(sample_audio[start:end])
  for i in range(0,mix):
    slice = random.randint(0,cuts-1)
    original_container[slice] = sample_container[slice]
  result = sum(original_container)
  return result, original_file_class, original_file_scene
  #result.export("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\test.wav",format="wav")
 
  
  
  

