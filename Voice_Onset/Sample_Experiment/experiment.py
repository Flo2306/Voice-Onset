# Import necessary libraries
import sounddevice as sd
import psychopy.core as core
import os
import pandas as pd
from psychopy import visual
from scipy.io.wavfile import write

#Setting up language and participant
participant_ID = "005"
language = "en-UK"

#Setting the colour for the background and the allowed response time
WHITE = [1,1,1]
ALLOWED_RESPONSE_TIME = 5

#Creating the window
window = visual.Window(size = (600,600), fullscr=False, color=WHITE, colorSpace='rgb')

#Getting current path 
current_path = os.getcwd()

#Defining a single trial 
def singleTrial(trialNumber, image, window = window):

    #Creating the picture
    img = visual.ImageStim(window, image = image, units = 'pix')
    img.draw()
    window.flip()

    #Setting the rate for recording
    fs = 44100

    #start recording 
    myrecording = sd.rec(int(ALLOWED_RESPONSE_TIME * fs), samplerate=fs, channels=1)


    #waiting for recording to finish 
    sd.wait()


    #Creating the filename for each audio file
    filename = participant_ID + "_" + str(trialNumber + 1) + ".wav"

    #Changing to appropriate location to save audio file
    os.chdir(current_path + os.sep + "Data")

    #Creating audio file
    write(filename, fs, myrecording)
    return

#Running the experiment
def run_experiment():
    #Creating a list of image names
    images = os.listdir(current_path + os.sep + "Images")
    #Removing .DS_Store which is a file macs create 
    images.remove(".DS_Store")

    #Defining the list names for each relevant outcome
    list_of_filenames = []
    list_of_targets = []
    list_of_languages = []

    #Iterating through all pictures in order (could easily be randomised but was not 
    # necessary here)
    for number in range(len(images)):
        #Changing directory to find pictures
        os.chdir(current_path + os.sep + "Images")
        #Creating the filename to be appended
        filename = participant_ID + "_" + str(number+1) + ".wav"
        list_of_filenames.append(filename)

        #Appending the target word which is included in the filename
        target_word = images[number][0:-4]
        list_of_targets.append(target_word)

        #Appending the language used (might not be necessary for you but can 
        # useful if you have different accents of a language like Australian English)
        list_of_languages.append(language)

        #Creating a single trial
        singleTrial(number, images[number])

    #Changing path back to original folder
    os.chdir(current_path + os.sep + "CSV_Files")
    df = pd.DataFrame({'File_name': list_of_filenames, 'Target': list_of_targets, 'Language': list_of_languages})
    df.to_csv("Data" + participant_ID + ".csv")

run_experiment()