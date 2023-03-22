import os
import pandas as pd
from Voice_Onset import onset
import tkinter as tk


current_directory = os.getcwd()
path_to_audio = current_directory + os.sep + "Data"
path_to_csv = current_directory + os.sep + "CSV_Files"

list_of_csv_files = os.listdir(path_to_csv)
list_of_csv_files.remove(".DS_Store")

os.chdir(path_to_csv)

#To combine all csv files 
#df = pd.DataFrame()
#for filename in list_of_csv_files:
    #if filename == 'Combined_csv_files.csv':
        #continue
    #print(filename)
    #df = df.append(pd.read_csv(filename, sep= ";"))

#print(df)
#df.to_csv("Combined_csv_files.csv", sep=",")

df_to_use = pd.read_csv("Combined_csv_files.csv")

list_of_found_words = []
list_of_onset_values = []

for i in range(len(df_to_use)):
    os.chdir(path_to_audio)
    file_name = df_to_use.loc[i, "File_name"]
    language = df_to_use.loc[i, "Language"]
    target = df_to_use.loc[i, "Target"]
    best_word, onset_value = onset.binary_search(audio_input = file_name, language_used= language, target_word = target)
    list_of_found_words.append(best_word)
    list_of_onset_values.append(onset_value)


df_to_use['Best_word'] = list_of_found_words
df_to_use['Onset_value'] = list_of_onset_values

print(df_to_use)