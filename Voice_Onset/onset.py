#Florian Burger 
#08.02.2023
#The code below allows you to transform audio recordings into text form and will give you approximate onset times 

#The most important thing for this algorithm is audio quality. If recording quality is poor, I recommend using a
#different platform like Chronset 

#Things to improve: 
#Include second r.recognize class in code but will most likely require some API access set up? 

import speech_recognition as sr
import pandas as pd
import numpy as np
import os
import soundfile
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from scipy.io.wavfile import read, write
import numpy as np
import time
import psutil
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def binary_search(audio_input, language_used, target_word = None, model = 'all-mpnet-base-v2', decision_value = 0.8, offset = 0, onset = 0.1, increment_increase = 0.0001, list_of_increment_values = [1], list_needed = 0, adjustment_needed = 0, run_already = 0, words_found = [], best_word = ""): 
    """Function using binary search in combination wih transcripion to estimate word onset.

    This function can estimate the onset time of a audio file by repeately splitting the file 
    until word transcription works barely. Additionally, it allows for target words to be entered, 
    compares the target word to the said word, and if the cosine similarity between the target 
    and said word is above a defined threshold, it determines the voice onset. Essentially, 
    it can be used to automate experiments which use word onset. 

    Parameters
    ----------
    audio_input : str
        This is the audio file that is input into the function. Working directory needs to 
        be able to find it
    language_used : str
        This is the language of the experiment to be used. A list of all possible languages 
        can be found under https://gist.github.com/msikma/8912e62ed866778ff8cd
    target_word: str 
        The target word picked will be compared to a transcribed version of the whole audio 
        recording that was entered (adjusting for offset and onset).
    decision_value: float 
        This is the value deciding whether the words are similar enough or not. The values we
        have found are 0.8 for very simila/the same word and 0.6 for words in the same category 
    offset: int/float 
        This can be used to limit the length of the audio file. 
    onset: int/float 
        The onset value is the minimum time frame value. It can be useful if your data includes 
        a click of the microphone as it can influence audio quality. 
    increment_increase: float 
        The increment increase value is used to establish the accuracy of the algorithm down to 
        low values. The higher this value, the less comparisons the algorithm makes leading to 
        an increase in speed but a decrease in accuracy. It is recommended to use a low value 
        as it will increase accuracy 
    list_of_increment_values: list 
        This list is used to return the already adjusted values. You can enter your own list of time points 
        to use for the binary search. The code establishes its own list depending on the offset, onset, and 
        increment value creating a list from the onset to offset in steps of the increment value 
    list_needed = int 
        If you use your own list, this is a value that you need to set to 1 or higher. When this value is 0,
        the list is created for you. 
     run_already: int 
        This parameter is used to establish a baseline and to not run the whole version of the function
        constantly. This value is set to 0 at the beginning to certain things like the decision for the 
        onset value are only done once. 
    words_found: list 
        This list includes all the potential words found in the transcribt of the audio file. 
    best_word: string
        This is the word that has the best similarity value with the target word
    
    Returns
    -------
    best_word : string
        Returns the word with the highest cosine similaity which then was used to make the algorithm 
        as accurate as possible 

    onset_value_found1 : float
        Returns the onset value found by the algorithm 

    """
    #Creating a audio file that can be used for input. This file will be called "NEW_" plus the name of 
    #the original audio file but it will be removed once the code is finished
    if adjustment_needed == 0:
        audio_input = adjust_audio_input(audio_input)

    #Setting the offset value
    if offset == 0:
        offset = len(audio_input)

    #Creating a list of potential intervals from onset to onset in increments 
    #of increment_increase
    if list_needed == 0:
        list_of_intervals =  list(np.arange(onset,offset,increment_increase))
    
    #Using the input list if one was provided
    else:
        list_of_intervals = list_of_increment_values

    #Setting values used for indexing with low being the first value and 
    #high representing the last index. Mid_index is the index in the middle 
    #of the list
    low = 0
    high = len(list_of_intervals) - 1
    mid_index = int((low + high)/2)

    #End of the recursion when there are maximum two items left in the list. 
    if high < 2:
        #Returning the appropriate value
        onset_value_found = list_of_intervals[0]
        onset_value_found1 = onset_value_found.item()
        
        #Removing the newly created audio file
        os.remove(audio_input)
        
        #Return the best word found instead of the target word?
        if onset_value_found1 < onset + 0.01:
            return "Not working", onset_value_found1
        #Returns the best word found 
        else:
            return best_word, onset_value_found1
    
    #Defining the value that is in the middle of the increment list. 
    #An example would be that in a audio file of 5 seconds, the first 
    #middle value is 2.5, the second either 1.25 or 3.75 and so on. 
    mid = list_of_intervals[mid_index]

    #Setting up the recognizer
    r = sr.Recognizer()
    with sr.AudioFile(audio_input) as source:
        
        #Removes some noise from file
        r.adjust_for_ambient_noise(source, duration=onset)
        # listen for the data (load audio to memory)
        audio_data = r.record(source, offset=mid)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language=language_used, show_all = True)

        if len(text) == 0:
            text = r.recognize_whisper(audio_data, show_all = True)
        
        text_str = str(text)

        #Used for set up of the model. 
        if run_already == 0:
            words_found = word_recognizer(audio_input, language = language_used)
            if target_word:
                #Finding the potential words in the audio input
                cosine_similarity_list = []
                #Calculating the cosine values for each word in the output
                for word in words_found:
                    #In rare occasions, the transcription returned ints or floats which is 
                    #why we skip over all values that are not strings
                    if type(word) != str:
                        words_found.remove(word)
                        continue
                    correct_value = word_distance_caluclated(target_word, word, model_name = model)
                    #Appending the values to the list 
                    cosine_similarity_list.append(correct_value)

                #Selecting the best cosine value found (assuming it is the best match within all responses). 
                best_cosine_value = max(cosine_similarity_list, default=0)
                if best_cosine_value > 0: 
                    index_for_word = cosine_similarity_list.index(max(cosine_similarity_list))
                    best_word = words_found[index_for_word]
                else: 
                    best_word = "INVALID"
                
                #Checking if the best value we found is higher than the decision value, otherwise the loop continues
                if best_cosine_value < decision_value:
                    os.remove(audio_input)
                    #This is where the message is returned that the response was too different from the original word/target
                    return best_word, 0
                    
            #If there is no target word, the word found in the audio with the highest confidence is picked as the target word and 
            #then used for further analysis
            else:
                #Picking the word with the highest confidence is not difficult as we can use list comprehension due to the way 
                #the word_recognizer function works
                try:
                    best_word = words_found[0]
                except:
                    os.remove(audio_input)
                    #This is where the message is returned that the response was too different from the original word/target
                    return "INVALID", 0
                    
        source.__exit__(None, None, None)    
        #This checks whether the best word we found is in the audio file and then runs the recursion
        if best_word in text_str: 
            #Moves the time frame up (e.g. from 2.5s to 3.75s)
            list_of_intervals1 = list_of_intervals[mid_index:high]
            return binary_search(audio_input, language_used, target_word, list_needed = 1, list_of_increment_values = list_of_intervals1, run_already=1, words_found = words_found, best_word = best_word, adjustment_needed= 1)
        else: 
            #Moves the time frame down (e.g. from 2.5 to 1.25)
            list_of_intervals1 = list_of_intervals[low:mid_index]
            return binary_search(audio_input, language_used, target_word, list_needed = 1, list_of_increment_values = list_of_intervals1, run_already=1, words_found = words_found, best_word = best_word, adjustment_needed=1)

def word_distance_caluclated(target_word, word_found, model_name):
    """Function calculating cosine similarity between target word and word found

    This function calculates the cosine similarity between two words and returns 
    a value between 0 and 1 (0 means NO similarity, 1 means perfect similarity (same word)). 

    Parameters
    ----------
    target_word : str
        This is the word that we want to find meaning that this is the original name of the 
        picture
    word_found : str
        The word that was found using the transcription
    model: str 
        Model that can be used to for estimating the value. More models can be found under 
        https://www.sbert.net/docs/pretrained_models.html
    
    Returns
    -------
    final_value : float 
        Returns the cosine similarity between the target word and the found word
    """
    #Model for calculating word embeddings using spacy 
    model = SentenceTransformer(model_name)
    sen = [word_found, target_word] 
    sen_embeddings = model.encode(sen)
    outcome = cosine_similarity(sen_embeddings)
    final_value = outcome[1][0]
    return final_value

def finding_appropriate_value(model):
    """Function returning cosine similarity for two input words until user is done

    This function can be used to investigate how similar words are. The user can
    enter words and see how they are related next to each other in the model specified. 
    Once the user has had enough, he can quite the loop by pressing "n" and then enter 
    a value that seems useful 

    Parameters
    ----------
    model : str
        This is the model that the user can input to see which values make most sense. 
        A list of all available models can be found under https://www.sbert.net/docs/pretrained_models.html
    
    Returns
    -------
    decided_value : int
        Returns the value that is going to be used as a threshold for the rest of the data 
    """
    #Used to create while loop 
    done = False
    while done == False:
        #Getting input from user
        word_1 = input("Please enter a word: ")
        word_2 = input("Please enter the second word: ")
        #Calculating the cosine distance between both words
        final_value = word_distance_caluclated(word_1, word_2, model)
        
        #Asking for another iteration
        done_yet = input("Do you want to try another word combination? Enter y/n: ")
        #Asking if they want to continue
        if done_yet == "n": 
            done = True
    decided_value = float(input("Please enter the decision value you want to use by seperating it with a . e.g. 0.6: "))
    return decided_value

def adjust_audio_input(file_name):
    """Function creating useable input file for data

    This function creates a seperate wav file that fulfills the conditions 
    from the input file and saves it in the current working directory. 
    Supported audio types can be found under http://www.mega-nerd.com/libsndfile/#Features

    Parameters
    ----------
    file_name : str
        Uses the file name that is input into the function. Can be any audio file in the 
        working directory 
    
    Returns
    -------
    new_name: string
        Returns the string value of the new sound file
    """
    #Reading the data
    data, samplerate = soundfile.read(file_name)
    #Creating new name for file
    new_name = "NEW_" + str(file_name)
    #Adjusting the type of recording so sound recognition works 

    with soundfile.SoundFile(file_name, 'r') as f:
        data = f.read()
        samplerate = f.samplerate
        
        #Adjusting the type of recording so sound recognition works 
        soundfile.write(new_name, data, samplerate, subtype='PCM_16')
    
    return new_name

def word_recognizer(sound_file, language):
    """Function used to recognize the words said. 

    This function returns a list of the words found in the full audio file 
    and returns them. 

    Parameters
    ----------
    sound_file : str
        name of audio file that will be used for recognition 
    
    Returns
    -------
    new_name: list
        Strings found in the audio returned as strings 
    """

    #Creating a list for the output 
    list_for_output = []
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(sound_file) as source:
        try:
            #Removes some noise from file using the first 0.2 seconds as a baseline
            r.adjust_for_ambient_noise(source, duration = 0.2)
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data, language=language, show_all=True)
            
            words_found = list(text.values())
            #Complicated for loop to deal with return data from r.recongnize_google 
            for word in words_found:
                for item in word:
                    outcome = list(item.values())
                    for thing in outcome:
                        list_for_output.append(thing)         
            return(list_for_output)
        except:
            return(list_for_output)
