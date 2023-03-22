from onset import *
import glob

#This code is an example of how you can use this module to write you analysis yourself. It will not run on any data as I used it 
#on my own data so it works currently. It is more meant to be used for inspiration and should be adjusted accordingly

def example_for_folder(): 
    #Select model from https://www.sbert.net/docs/pretrained_models.html an input as string
    #decision_value = finding_appropriate_value(model)
    decision_value = 0.5
    #defining the paths to use
    original_path = os.getcwd()
    path_to_audios = original_path + os.sep + "Voice_Data"
    datafile = pd.read_csv("Combined Values from Participants.csv")

    #creating empty lists and setting it up 
    os.chdir(path_to_audios)
    files = glob.glob("*")
    list_of_answers = []
    list_of_file_names = []
    list_of_onset = []

    for file in files: 
        new_path = path_to_audios + os.sep + file
        os.chdir(new_path)
        files_in_folder = glob.glob("*")
        for file1 in files_in_folder:
            if file1 == "1":
                nothing = 0 
            else:
                continue
            os.chdir(new_path + os.sep + file1)
            files_in_folder1 = glob.glob("*")
            for file2 in files_in_folder1:
                print(file2)
                target_word_row = datafile.loc[datafile["File"] == file2, "Target"].values
                try: 
                    target_word = str(target_word_row[0])
                except: 
                    continue
                word_used, outcome_value = binary_search(file2, "en-US", target_word, decision_value=decision_value)
                list_of_answers.append(word_used)
                list_of_file_names.append(file2)
                list_of_onset.append(outcome_value)

    #Creating a dataframe and saving the results into one file
    df = pd.DataFrame()
    df['File']=list_of_file_names
    df['Answer']=list_of_answers
    df['Onset'] = list_of_onset

    os.chdir(original_path)
    df.to_csv("Answers_as_text_for_testing_3.csv")
