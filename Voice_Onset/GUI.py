import tkinter as tk
import os
import pandas as pd
import glob
from tkinter import filedialog, Text, messagebox, ttk
from sentence_transformers import SentenceTransformer
from unipath import Path
from pathlib import Path as path
from Voice_Onset import onset 
import time
import sys

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GUI for Voice Onset")
        self.geometry("1100x550")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.page1 = Page1(self.notebook)
        self.page2 = Page2(self.notebook, self.on_confirm)
        self.page3 = None  # Initialize Page3 instance as None

        self.notebook.add(self.page1, text="Page 1")
        self.notebook.add(self.page2, text="Page 2")

        def close_gui():
            app.destroy()
            sys.exit(1)

        close_button = tk.Button(self, text="Close everything", command=close_gui)
        close_button.pack()

    def on_confirm(self):
        if self.page2.df is None:
            # No CSV file selected, handle accordingly
            self.page3 = Page3(self.notebook, self.page2.base_directory, self.page2.language,
                               self.page2.file_path, None, self.page2.cutoff_value,
                               self.page1.model_combo.get())
        else:
            # CSV file selected, proceed as before
            self.page3 = Page3(self.notebook, self.page2.base_directory, self.page2.language,
                               self.page2.file_path, self.page2.df, self.page2.cutoff_value,
                               self.page1.model_combo.get())
            
        self.notebook.add(self.page3, text="Page 3")
        self.notebook.select(self.page3)

        self.after(300)

        self.page3.start_processing()

class Page1(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        tk.Label(self, text="Word 1:").pack()
        self.word1_entry = tk.Entry(self)
        self.word1_entry.pack()

        tk.Label(self, text="Word 2:").pack()
        self.word2_entry = tk.Entry(self)
        self.word2_entry.pack()

        all_models = ['distiluse-base-multilingual-cased-v2', 'all-mpnet-base-v2', 'paraphrase-multilingual-mpnet-base-v2', 'all-distilroberta-v1', 'multi-qa-mpnet-base-dot-v1']
        tk.Label(self, text="Model:").pack()
        self.model_combo = ttk.Combobox(self, values=all_models)
        self.model_combo.pack()
        self.model_combo.current(0)

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        tk.Button(self, text="Calculate", command=self.on_calculate_click).pack()

    def on_calculate_click(self):
        word1 = self.word1_entry.get()
        word2 = self.word2_entry.get()
        model_name = self.model_combo.get()

        similarity = onset.word_distance_caluclated(word1, word2, model_name)

        self.result_label.config(text=f"Cosine Similarity: {similarity:.4f}")


class Page2(tk.Frame):
    def __init__(self, parent, on_confirm):
        tk.Frame.__init__(self, parent)
        self.on_confirm = on_confirm
        
        self.text_label = tk.Label(self, text="Enter the language to use:\nIf you are using multiple languages which are specified in the csv, this language does not matter")
        self.text_label.pack()

        self.input_entry = tk.Entry(self)
        self.input_entry.pack()
        self.input_entry.insert(tk.END, "en-US")

        self.cutoff_label = tk.Label(self, text="Cutoff Value (based on Page 1):")
        self.cutoff_label.pack()
        self.model_warning = tk.Label(self, text="Warning: Used Model is Model selected on Page 1")
        self.model_warning.pack()

        self.cutoff_entry = tk.Entry(self)
        self.cutoff_entry.pack()
        self.cutoff_entry.insert(tk.END, "0.8")
        self.cutoff_value = float(self.cutoff_entry.get())

        self.dir_label = tk.Label(self, text="Select the directory:")
        self.dir_label.pack()

        self.dir_button = tk.Button(self, text="Browse...", command=self.handle_click)
        self.dir_button.pack()

        self.selected_dir = tk.Label(self)
        self.selected_dir.pack()

        self.file_label = tk.Label(self, text="Select the CSV file (optional):")
        self.file_label.pack()

        self.file_button = tk.Button(self, text="Browse...", command=self.open_csv)
        self.file_button.pack()

        self.selected_file = tk.Label(self)
        self.selected_file.pack()

        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm)
        self.confirm_button.pack()

        self.base_directory = None
        self.language = None
        self.file_path = None
        self.df = None

    def handle_click(self):
        current_dir = os.getcwd()
        dir_path = filedialog.askdirectory(initialdir=current_dir)
        self.selected_dir.config(text=dir_path)
        self.base_directory = dir_path

    def open_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_path:
            self.selected_file.config(text=file_path)
            self.file_path = file_path
    
            # If the user selected a file, open it as a pandas dataframe
            df_series = pd.read_csv(file_path)
            self.df = pd.DataFrame(df_series)

    def confirm(self):
        text_input = self.input_entry.get()
        self.language = text_input
        self.on_confirm()  # Call the on_confirm method provided by GUI class

class Page3(tk.Frame):
    def __init__(self, parent, base_directory, language, file_path, df, cut_off_value, model_name):

        tk.Frame.__init__(self, parent)

        self.base_directory = base_directory
        self.file_path = file_path
        self.language = language
        self.df = df
        self.cut_off_value = cut_off_value
        self.model_name = model_name

        self.progress_label = tk.Label(self, text="Progress:")
        self.progress_label.pack()

        self.progress = ttk.Progressbar(self, orient="horizontal", length=250, mode="determinate")
        self.progress.pack()

        self.count_label = tk.Label(self, text="Iteration count: 0")
        self.count_label.pack()

        self.total_label = tk.Label(self, text="Total number of iterations: 0")
        self.total_label.pack()

        self.time_label = tk.Label(self, text="Time left: ")
        self.time_label.pack()

        self.used_directory = tk.Label(self, text="Used Folder Directory: " + self.base_directory)
        self.used_directory.pack()

        if self.file_path:
            self.used_file = tk.Label(self, text="Used CSV File: " + os.path.basename(self.file_path) + "\nOutput file will be in the same location as the CSV file: Onset_times.csv")
            self.used_file.pack()

        self.finish_button = tk.Button(self, text="Finish", command=self.destroy)
        self.finish_button.pack()

        self.file_dict = {}
        self.keys = []
        self.list_of_words = []
        self.list_of_outcome_values = []
        self.list_of_file_names = []

    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

        remaining_iterations = len(self.keys) - value
        remaining_time = self.estimate_remaining_time(value, len(self.keys), self.start_time)
        self.count_label.config(text="Iteration count: {}".format(value))
        self.time_label.config(text="Time left: {} minutes".format(remaining_time))

    def estimate_remaining_time(self, iteration, total_iterations, start_time):
        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / (iteration + 1)) * (total_iterations - (iteration + 1))
        return round(remaining_time / 60, 2)

    def start_processing(self):
        self.used_directory.config(text="Used Folder Directory: " + self.base_directory)
        self.used_file.config(text="Used CSV File: " + os.path.basename(self.file_path) + "\nOutput file will be in the same location as the CSV file: Onset_times.csv")

        os.chdir(self.base_directory)

        file_types = ["*.wav", "*.mp3", "*.aiff", "*.flac", "*.m4a", "*.ogg", "*.aac", "*.wma", "*.ape"]
        files_list = []

        for file_type in file_types:
            files_list.extend(glob.glob("**/" + file_type, recursive=True))

        self.total_label.config(text="Total number of iterations: " + str(len(files_list)))
        self.progress.config(maximum=len(files_list))

        self.start_time = time.time()

        for iteration, file in enumerate(files_list):
            if file.startswith("NEW"):
                os.remove(file)
                continue

            useable_path_format = Path(os.getcwd() + os.sep + file)
            to_use_directory = useable_path_format.parent
            name_of_audio = useable_path_format.name

            self.file_dict[name_of_audio] = to_use_directory
            self.keys = list(self.file_dict.keys())

            self.update_progress(iteration)
            self.count_label.config(text="Iteration count: {}".format(iteration + 1))

            target_language = self.language

            if self.df is not None:
                # CSV file selected, proceed as before
                target_word = self.df[self.df["File_name"] == name_of_audio]["Target"].values[0]
                outcome_word, outcome_value = onset.binary_search(name_of_audio, target_language, target_word=target_word, decision_value=self.cut_off_value, model=self.model_name)
            else:
                # No CSV file selected, handle accordingly (you can decide what to do in this case)
                outcome_word, outcome_value = onset.binary_search(name_of_audio, target_language, decision_value=self.cut_off_value, model=self.model_name)

            self.list_of_words.append(outcome_word)
            self.list_of_outcome_values.append(outcome_value)
            self.list_of_file_names.append(name_of_audio)

            # Update the GUI window
            remaining_iterations = len(self.keys) - (iteration)
            remaining_time = self.estimate_remaining_time(iteration + 1, len(files_list), self.start_time)
            self.count_label.config(text="Iteration count: {}".format(iteration + 1))
            self.time_label.config(text="Time left: {} minutes".format(remaining_time))

            # Update the GUI window (if needed)
            self.update()
            self.after(100)

        df_new = pd.DataFrame(list(zip(self.list_of_words, self.list_of_outcome_values, self.list_of_file_names)), columns=["Said_word", "Onset_times", "File_name"])
        print(df_new)
        if self.df is not None:
            path_to_csv_file = Path(self.file_path)
            csv_file_parent = path_to_csv_file.parent
            os.chdir(csv_file_parent)
            df_new.to_csv("Onset_times.csv")

        return self.keys, self.file_dict
app = GUI()
app.mainloop()
app.after(300000)
app.destroy()
sys.exit(1)
