import tkinter as tk
import os
import pandas as pd
import glob
from tkinter import filedialog, Text, messagebox, ttk
from sentence_transformers import SentenceTransformer
from unipath import Path
from pathlib import Path as path
from Voice_Onset import onset 

list_of_languages = ["en-AU", "en-UK", "en-US"]

def gui_1(): 
    def on_calculate_click():
        # Get the input values
        word1 = word1_entry.get()
        word2 = word2_entry.get()
        model_name = model_combo.get()

        # Calculate the similarity
        similarity = onset.word_distance_caluclated(word1, word2, model_name)

        # Update the output label
        result_label.config(text=f"Cosine Similarity: {similarity:.4f}")

    def on_continue_click():

        global model_name
        model_name = model_combo.get()

        global cut_off_value 
        cut_off_value = float(cut_off_entry.get())
        
        root.destroy()

    root = tk.Tk("800x400")
    root.title("GUI for Voice Onset")
    root.geometry("800x400")

    # Create the input widgets
    tk.Label(root, text="Word 1:").pack()
    word1_entry = tk.Entry(root)
    word1_entry.pack()

    tk.Label(root, text="Word 2:").pack()
    word2_entry = tk.Entry(root)
    word2_entry.pack()

    #Selected useful models from https://www.sbert.net/docs/pretrained_models.html
    all_models = ['distiluse-base-multilingual-cased-v2', 'all-mpnet-base-v2', 'paraphrase-multilingual-mpnet-base-v2', 'all-distilroberta-v1', 
                  'multi-qa-mpnet-base-dot-v1']

    tk.Label(root, text="Model:\n (selected model will be used for search when continue is clicked)").pack()
    model_combo = ttk.Combobox(root, values=all_models)
    model_combo.pack()
    model_combo.current(0)

    # Create the output widget
    result_label = tk.Label(root, text="")
    result_label.pack()

    # Create the button
    tk.Button(root, text="Calculate", command=on_calculate_click).pack()

    tk.Label(root, text="Cut-off Value").pack()
    cut_off_entry = tk.Entry(root)
    cut_off_entry.pack()

    tk.Button(root, text="Continue", command=on_continue_click).pack()
    root.mainloop()

def gui_2():
    # Create a Tkinter window
    root = tk.Tk("800x400")
    root.title("GUI for Voice Onset")
    root.geometry("800x400")

    # Define a function to handle button click events
    def handle_click():
        # Open a file dialog to select a directory
        dir_path = filedialog.askdirectory(initialdir=os.getcwd())

        selected_dir.config(text=dir_path)

        # Prompt the user to enter some text input
        text_input = input_entry.get()

        #Setting the global variables
        global base_directory
        global language

        base_directory = dir_path
        language = text_input

    def open_csv():
        # Use a file dialog to select a CSV file
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

        #Not sure why this does not display the file location
        selected_file.config(text=file_path)

        # If the user selected a file, open it as a pandas dataframe
        global df
        df_series = pd.read_csv(file_path)
        df = pd.DataFrame(df_series)

    #Creating the validate function 
    def validate(): 
        #Getting the used language
        text_input = input_entry.get()
        global language
        language = text_input
        root.destroy()
       
    # Create a label for the input text
    text_label = tk.Label(root, text="Enter the language to use: \nIf you are using multiple languages which are specified in the csv this language does not matter")
    text_label.pack()

    # Create an entry field for the input text
    input_entry = tk.Entry(root)
    input_entry.pack()
    input_entry.insert(tk.END, "en-US")

    # Create a label for the input directory
    dir_label = tk.Label(root, text="Select the directory:")
    dir_label.pack()

    # Create a button to select a directory
    dir_button = tk.Button(root, text="Browse...", command=handle_click)
    dir_button.pack()

    selected_dir = tk.Label(root)
    selected_dir.pack()

    # Create a label for the input csv file
    file_label = tk.Label(root, text="Select the csv file:")
    file_label.pack()

    # Create a button to select a file
    file_button = tk.Button(root, text="Browse...", command=open_csv)
    file_button.pack()

    #Show selected file
    selected_file = tk.Label(root)
    selected_file.pack()

    #Confirm choices button
    confirm_button = tk.Button(root, text="Confirm", command = validate)
    confirm_button.pack()

    root.mainloop()

def gui_3():
    #Creating root window
    root1 = tk.Tk("800x400")
    root1.title("GUI for Voice Onset")
    root1.geometry("800x400")

    #Used to update progressbar
    def update_progress(progress, value):
        progress['value'] = value
        root1.update_idletasks()

    #Changing to the directory selected
    os.chdir(base_directory)

    #specifying all audio types
    file_types = ["*.wav", "*.mp3", "*.aiff", "*.flac", "*.m4a", "*.ogg", "*.aac", "*.wma", "*.ape"]
    #List to extend to
    files_list = []

    #filtering through the data multiple times checking for different audio extensions
    for type in file_types:
        files_list.extend(glob.glob("**/" + str(type), recursive= True))

    # Create a label for the input csv file
    progress_label = tk.Label(root1, text="Progress:")
    progress_label.pack()

    #Creating the progressbar
    progress = ttk.Progressbar(root1, orient="horizontal", length=250, mode="determinate", maximum= len(files_list))
    progress.pack()

    #Iteration count
    count_label = tk.Label(root1, text="Iteration count: 0")
    count_label.pack()

    #Total number of iterations
    total_label = tk.Label(root1, text="Total number of iterations: " + str(len(files_list)))
    total_label.pack()

    #Used directory
    used_directory = tk.Label(root1, text="Used Folder Directory: " + base_directory)
    used_directory.pack()

    #Used csv file
    used_file = tk.Label(root1, text="Used CSV File: " + path(file_path).name + "\nOutput file will be in same location as the csv file")
    used_file.pack()

    finish_button = tk.Button(root1, text="Finish", command=root1.destroy)
    finish_button.pack()

    #Dictionary for file names and their relevant directories 
    file_dict = {}

    #Iterating through each file creating the appropriate format
    for file in files_list:
        #To remove and then skip files created when the loop was already stopped
        if str(file).startswith("NEW"):
            os.remove(file)
            continue
        useable_path_format = Path(os.getcwd() + os.sep + file)
        to_use_directory = useable_path_format.parent
        name_of_audio = useable_path_format.name
        file_dict[name_of_audio] = to_use_directory

    #Getting the keys from the dictionary which are the filenames
    keys = list(file_dict.keys()) # convert the keys to a list

    #Create empty lists to be used
    list_of_words = []
    list_of_outcome_values = []
    #This is necessary as I am using a dictionary before so the output is unsorted
    list_of_file_names = []

    #Iterating through the dictionary
    for iteration in range(len(file_dict)):
        #Updating progressbar
        update_progress(progress, iteration)
        #Updating Iteration counter
        count_label.config(text="Iteration count: {}".format(iteration+1))
        root1.update()

        key = keys[iteration]
        print(key)
        #Necessary to include if the location of audio files is not the same (like files per participant)
        os.chdir(file_dict[key])
        #Find the approppriate row in the input csv file 
        df_row = df.loc[df['File_name'] == key]
        #Get target word
        target_word = df_row['Target'].values[0]
        #Get target language
        try:
            target_language = df_row['Language'].values[0]
        except:
            target_language = language
        #Run binary search
        outcome_word, outcome_value = onset.binary_search(key, target_language, target_word=target_word, decision_value = cut_off_value, model = model_name)
        #Appending all values to the right list
        list_of_words.append(outcome_word)
        list_of_outcome_values.append(outcome_value)
        list_of_file_names.append(key)
    
    #Creating df and saving it 
    df_new = pd.DataFrame(list(zip(list_of_words, list_of_outcome_values, list_of_file_names)), columns=["Said_word", "Onset_times", "File_name"])
    os.chdir(path(file_path).parent)
    df_new.to_csv("Onset_times.csv")
    root1.mainloop()

gui_1() 
gui_2()
gui_3()