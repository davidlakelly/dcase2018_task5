import os
import glob
import re
import pandas as pd
import math
import random
import preprocessor
from pydub import audio_segment
import tqdm
import shutil
source = pd.read_csv("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\meta.txt", sep="\t", names=["file_name","class_type","scene"])

def percent_augment(step, mode, out_name, cuts, mix=2):
    if(mode == "shuffle"):
        if not os.path.exists("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"):
            os.mkdir("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\")
        
        if not os.path.exists("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name):
            os.mkdir("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name)
        else:
            shutil.rmtree("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name)
            os.mkdir("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name)

        result = pd.DataFrame(source.iloc[::step,:])
        result=result.sample(frac=1).reset_index(drop=True)

        for index, row in tqdm.tqdm(result.iterrows()):
            file_name = row["file_name"].split("/")[-1]
            file_name_without_ext = file_name.split(".")[0]
            base_url = "C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\audio\\"
            full_path = str(base_url) + str(file_name)
            result_file, result_class, result_scene  = preprocessor.shuffler(full_path,cuts)
            result_file.export("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\" + out_name + "\\" + out_name + "_" + file_name_without_ext +".wav", format="wav")
            f = open("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\" + out_name + "\\" + out_name +"_meta.txt", "a+")
            f.write(str(out_name) + "/" + out_name + "_" + file_name_without_ext +".wav"+ "\t" + str(result_class) + "\t" + str(result_scene) + "\n")
            f.close()
            
    elif(mode =="mixer"):
    
        if not os.path.exists("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"):
            os.mkdir("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\")
        
        if not os.path.exists("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name):
            os.mkdir("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name)
        else:
            shutil.rmtree("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name)
            os.mkdir("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\"+out_name)

        result = pd.DataFrame(source.iloc[::step,:])
        result=result.sample(frac=1).reset_index(drop=True)
        
        for index, row in tqdm.tqdm(result.iterrows()):
            file_name = row["file_name"].split("/")[-1]
            file_name_without_ext = file_name.split(".")[0]
            base_url = "C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\audio\\"
            full_path = str(base_url) + str(file_name)
            #print(full_path)
            result_file, result_class, result_scene  = preprocessor.mixer(full_path,cuts, mix=mix)
            result_file.export("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\" + out_name + "\\" + out_name + "_" + file_name_without_ext +".wav", format="wav")
            f = open("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\" + out_name + "\\" + out_name +"_meta.txt", "a+")
            f.write(str(out_name) + "/" + out_name + "_" + file_name_without_ext +".wav"+ "\t" + str(result_class) + "\t" + str(result_scene) + "\n")
            f.close()
    else:
        pass
        
        #print(type(temp))
    #print(result.head())

        

# percent_augment(10, "shuffle", "aug_shuffle_10_per_3_cuts", 3)
# percent_augment(10, "shuffle", "aug_shuffle_10_per_5_cuts", 5)
# percent_augment(10, "shuffle", "aug_shuffle_10_per_7_cuts", 7)


# percent_augment(5, "shuffle", "aug_shuffle_20_per_3_cuts", 3)
percent_augment(5, "shuffle", "aug_shuffle_20_per_5_cuts", 5)
percent_augment(5, "shuffle", "aug_shuffle_20_per_7_cuts", 7)

percent_augment(10, "mixer", "aug_mixer_10_per_3_cuts_2_mix", 3)
percent_augment(10, "mixer", "aug_mixer_10_per_5_cuts_2_mix", 5)
percent_augment(10, "mixer", "aug_mixer_10_per_7_cuts_2_mix", 7)

percent_augment(5, "mixer", "aug_mixer_20_per_3_cuts_2_mix", 3)
percent_augment(5, "mixer", "aug_mixer_20_per_5_cuts_2_mix", 5)
percent_augment(5, "mixer", "aug_mixer_20_per_3_cuts_2_mix", 7)

percent_augment(10, "mixer", "aug_mixer_10_per_5_cuts_3_mix", 5, 3)
percent_augment(10, "mixer", "aug_mixer_10_per_7_cuts_3_mix", 7, 3)



