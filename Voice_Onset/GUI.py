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

# Define the main GUI class
class GUI(tk.Tk):
    def __init__(self):
        # Initialize the main GUI window
        tk.Tk.__init__(self)
        self.title("GUI for Voice Onset")
        self.geometry("1100x550")

        # Create a notebook to hold multiple pages
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create instances of Page1 and Page2
        self.page1 = Page1(self.notebook)
        self.page2 = Page2(self.notebook, self.on_confirm)
        self.page3 = None  # Initialize Page3 instance as None

        # Add Page1 and Page2 to the notebook
        self.notebook.add(self.page1, text="Page 1")
        self.notebook.add(self.page2, text="Page 2")

        # Define a function to close the GUI
        def close_gui():
            app.destroy()
            sys.exit(1)

        # Create a button to close the GUI
        close_button = tk.Button(self, text="Close everything", command=close_gui)
        close_button.pack()

    # Callback function to be called when Page2 is confirmed
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
            
        # Add Page3 to the notebook and select it
        self.notebook.add(self.page3, text="Page 3")
        self.notebook.select(self.page3)

        # Wait for a short period before starting processing
        self.after(300)

        # Start the processing in Page3
        self.page3.start_processing()

# Define Page1 class
class Page1(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        # Create labels and entry widgets for user input
        tk.Label(self, text="Word 1:").pack()
        self.word1_entry = tk.Entry(self)
        self.word1_entry.pack()

        tk.Label(self, text="Word 2:").pack()
        self.word2_entry = tk.Entry(self)
        self.word2_entry.pack()

        # Define a list of available model names
        all_models = ['distiluse-base-multilingual-cased-v2', 'all-mpnet-base-v2', 'paraphrase-multilingual-mpnet-base-v2', 'all-distilroberta-v1', 'multi-qa-mpnet-base-dot-v1']
        # Create a label and combo box for model selection
        tk.Label(self, text="Model:").pack()
        self.model_combo = ttk.Combobox(self, values=all_models)
        self.model_combo.pack()
        self.model_combo.current(0)

        # Create a label to display the result and a button for calculation
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()
        tk.Button(self, text="Calculate", command=self.on_calculate_click).pack()

    # Callback function when "Calculate" button is clicked in Page1
    def on_calculate_click(self):
        # Get user input values
        word1 = self.word1_entry.get()
        word2 = self.word2_entry.get()
        model_name = self.model_combo.get()

        # Calculate the cosine similarity using the provided function
        similarity = onset.word_distance_caluclated(word1, word2, model_name)

        # Display the calculated similarity with four decimal places
        self.result_label.config(text=f"Cosine Similarity: {similarity:.4f}")


# Define Page2 class
class Page2(tk.Frame):
    def __init__(self, parent, on_confirm):
        tk.Frame.__init__(self, parent)
        self.on_confirm = on_confirm
        
        # Create labels and entry widgets for user input
        self.text_label = tk.Label(self, text="Enter the language to use:\nIf you are using multiple languages which are specified in the csv, this language does not matter")
        self.text_label.pack()

        self.input_entry = tk.Entry(self)
        self.input_entry.pack()
        self.input_entry.insert(tk.END, "en-US")

        # Create labels, entry widgets, and buttons for user input and interaction
        self.cutoff_label = tk.Label(self, text="Cutoff Value (based on Page 1):")
        self.cutoff_label.pack()
        self.model_warning = tk.Label(self, text="Warning: Used Model is Model selected on Page 1")
        self.model_warning.pack()

        self.cutoff_entry = tk.Entry(self)
        self.cutoff_entry.pack()
        self.cutoff_entry.insert(tk.END, "0.8")
        self.cutoff_value = float(self.cutoff_entry.get())

        self.dir_label = tk.Label(self, text="Select the data directory:")
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

        # Initialize variables to store user selections and data
        self.base_directory = None
        self.language = None
        self.file_path = None
        self.df = None

    # Callback function when "Browse" button for directory selection is clicked
    def handle_click(self):
        current_dir = os.getcwd()
        dir_path = filedialog.askdirectory(initialdir=current_dir)
        self.selected_dir.config(text=dir_path)
        self.base_directory = dir_path

    # Callback function when "Browse" button for CSV file selection is clicked
    def open_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_path:
            self.selected_file.config(text=file_path)
            self.file_path = file_path

            # If the user selected a file, open it as a pandas dataframe
            df_series = pd.read_csv(file_path)
            self.df = pd.DataFrame(df_series)

    # Callback function when "Confirm" button is clicked
    def confirm(self):
        # Get the user input for the language to use
        text_input = self.input_entry.get()
        self.language = text_input
        self.on_confirm()  # Call the on_confirm method provided by the GUI class

# Define Page3 class
class Page3(tk.Frame):
    def __init__(self, parent, base_directory, language, file_path, df, cut_off_value, model_name):
        # Initialize the Page3 instance with relevant data and GUI elements
        tk.Frame.__init__(self, parent)

        # Store provided data for later use
        self.base_directory = base_directory
        self.file_path = file_path
        self.language = language
        self.df = df
        self.cut_off_value = cut_off_value
        self.model_name = model_name

        # Create labels to display progress information
        self.progress_label = tk.Label(self, text="Progress:")
        self.progress_label.pack()

        # Create a progress bar to show the progress of iterations
        self.progress = ttk.Progressbar(self, orient="horizontal", length=250, mode="determinate")
        self.progress.pack()

        # Create labels to display iteration count and total iterations
        self.count_label = tk.Label(self, text="Iteration count: 0")
        self.count_label.pack()

        self.total_label = tk.Label(self, text="Total number of iterations: 0")
        self.total_label.pack()

        # Create label to display estimated remaining time
        self.time_label = tk.Label(self, text="Time left: ")
        self.time_label.pack()

        # Create labels to display used directory and file information
        self.used_directory = tk.Label(self, text="Used Folder Directory: " + self.base_directory)
        self.used_directory.pack()

        # Check if a file path is provided and display corresponding information
        if self.file_path:
            self.used_file = tk.Label(self, text="Used CSV File: " + os.path.basename(self.file_path) + "\nOutput file will be in the same location as the CSV file: Onset_times.csv")
            self.used_file.pack()
        else:
            self.csv_location = tk.Label(self, text="Name of final file: Onset_times.csv, Location: Same as Used Folder Directory")
            self.csv_location.pack()

        # Create a button to finish the processing
        self.finish_button = tk.Button(self, text="Finish", command=self.destroy)
        self.finish_button.pack()

        # Initialize data structures to store processing results
        self.file_dict = {}
        self.keys = []
        self.list_of_words = []
        self.list_of_outcome_values = []
        self.list_of_file_names = []

    # Update the progress bar and time estimate
    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

        # Estimate the remaining time based on current progress
        remaining_time = self.estimate_remaining_time(value, len(self.keys), self.start_time)
        self.count_label.config(text="Iteration count: {}".format(value))
        self.time_label.config(text="Time left: {} minutes".format(remaining_time))

    # Estimate the remaining time for the entire process
    def estimate_remaining_time(self, iteration, total_iterations, start_time):
        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / (iteration + 1)) * (total_iterations - (iteration + 1))
        return round(remaining_time / 60, 2)

    # Start the processing of audio files
    def start_processing(self):
        # Update the GUI to show the used directory and file information
        self.used_directory.config(text="Used Folder Directory: " + self.base_directory)
        if self.file_path:
            self.used_file.config(text="Used CSV File: " + os.path.basename(self.file_path) + "\nOutput file will be in the same location as the CSV file: Onset_times.csv")

        # Change the current working directory to the specified base directory
        os.chdir(self.base_directory)

        # Define a list of file types to search for
        file_types = ["*.wav", "*.mp3", "*.aiff", "*.flac", "*.m4a", "*.ogg", "*.aac", "*.wma", "*.ape"]
        files_list = []

        # Iterate over file types and gather a list of matching files
        for file_type in file_types:
            files_list.extend(glob.glob("**/" + file_type, recursive=True))

        # Update the total label with the number of iterations and configure the progress bar
        self.total_label.config(text="Total number of iterations: " + str(len(files_list)))
        self.progress.config(maximum=len(files_list))

        # Record the start time of the processing
        self.start_time = time.time()

        # Initialize variables for restart attempts and maximum restart attempts
        restart_attempts = 0
        max_restart_attempts = 10

        try:
            # Attempt to read the current status from a CSV file
            self.df_current = pd.read_csv('current_status.csv')
            restart_attempts = self.df_current.at[self.df_current.index[-1], 'RestartAttempts']

        except FileNotFoundError:
            # Create an empty DataFrame if the CSV file is not found
            columns = ['OnsetTime', 'SaidWord', 'FileName', 'TargetWord', 'RestartAttempts']
            self.df_current = pd.DataFrame(columns=columns)

        # Loop to handle processing and restart attempts
        while restart_attempts < max_restart_attempts:
            try:
                # Iterate over each file in the list
                for iteration, file in enumerate(files_list):
                    if file.startswith("NEW"):
                        try:
                            # Remove temporary files and continue to the next iteration
                            os.remove(file)
                            continue
                        except:
                            continue

                    directory_name = os.path.dirname(file)
                    
                    file_directory = os.path.join(self.base_directory, directory_name)
                    print(file_directory)
                    os.chdir(file_directory)
                    

                    # Read the current status if the DataFrame is not empty
                    if not self.df_current.empty:
                        self.df_current = pd.read_csv('current_status.csv')

                    # Skip files that are already processed
                    if file in self.df_current['FileName'].values:
                        continue

                    # Format the file path for processing
                    useable_path_format = Path(os.getcwd() + os.sep + file)
                    to_use_directory = useable_path_format.parent
                    name_of_audio = useable_path_format.name

                    # Store file information in the dictionary
                    self.file_dict[name_of_audio] = to_use_directory
                    self.keys = list(self.file_dict.keys())

                    # Update the progress bar and labels
                    self.update_progress(iteration)
                    self.count_label.config(text="Iteration count: {}".format(iteration + 1))

                    # Define the target language
                    target_language = self.language

                    if self.df is not None:
                        # CSV file selected, proceed as before
                        matching_rows = self.df[self.df["File_name"] == name_of_audio]
                        if not matching_rows.empty:
                            target_word = matching_rows["Target"].values[0]
                            target_language = self.df[self.df["File_name"] == name_of_audio]["Language"].values[0]
                            outcome_word, outcome_value, correct_answer = onset.binary_search(name_of_audio, target_language, target_word=target_word, decision_value=self.cut_off_value, model=self.model_name)
                        else:
                            outcome_word, outcome_value = onset.binary_search(name_of_audio, target_language, decision_value=self.cut_off_value, model=self.model_name)
                            outcome_word = "File not found in CSV file"
                    else:
                        # No CSV file selected, handle accordingly
                        outcome_word, outcome_value = onset.binary_search(name_of_audio, target_language, decision_value=self.cut_off_value, model=self.model_name)

                    # Create a new row for the current processing result
                    if correct_answer:
                        new_row = {'FileName': file, 'OnsetTime': outcome_value, 'SaidWord': outcome_word, 'TargetWord': target_word, 'CorrectAnswer': correct_answer, 'RestartAttempts': restart_attempts}
                    else: 
                        new_row = {'OnsetTime': outcome_value, 'SaidWord': outcome_word, 'FileName': file, 'TargetWord': target_word, 'RestartAttempts': restart_attempts}
                    new_row_df = pd.DataFrame(new_row, index=[0])

                    # Concatenate the new row DataFrame with the main DataFrame
                    self.df_current = pd.concat([self.df_current, new_row_df], ignore_index=True)

                    # Save the current status to a CSV file
                    self.df_current.to_csv('current_status.csv', index=False)

                    # Update the GUI window with the remaining iterations and time estimate
                    remaining_iterations = len(self.keys) - (iteration)
                    remaining_time = self.estimate_remaining_time(iteration + 1, len(files_list), self.start_time)
                    self.count_label.config(text="Iteration count: {}".format(iteration + 1))
                    self.time_label.config(text="Time left: {} minutes".format(remaining_time))

                    # Update the GUI window (if needed)
                    self.update()
                    self.after(100)

                # Save the final processed data to a CSV file
                if self.df is not None:
                    path_to_csv_file = Path(self.file_path)
                    csv_file_parent = path_to_csv_file.parent
                    os.chdir(csv_file_parent)
                    self.df_current.to_csv("Onset_times.csv")
                else:
                    self.df_current.to_csv("Onset_times.csv")

                # Return keys and file_dict to the caller
                return self.keys, self.file_dict

            except ConnectionResetError as e:
                # Handle restart attempts and update the DataFrame
                restart_attempts += 1
                new_row = {'OnsetTime': None, 'SaidWord': None, 'FileName': None, 'TargetWord': None, 'RestartAttempts': restart_attempts}
                new_row_df = pd.DataFrame(new_row, index=[0])

                # Concatenate the new row DataFrame with the main DataFrame
                self.df_current = pd.concat([self.df_current, new_row_df], ignore_index=True)

                # Save the current status to a CSV file
                self.df_current.to_csv('current_status.csv', index=False)

                # Handle maximum restart attempts
                if restart_attempts == max_restart_attempts:
                    print("Max restart attempts reached. Exiting.")
                    break

                # Restart the script using execv to recover from the error
                os.execv(sys.executable, ['python'] + sys.argv)

# Create an instance of the GUI class and start the main loop
app = GUI()
app.mainloop()

# Add a delay before destroying the GUI and exiting the application
app.after(300000)
app.destroy()
sys.exit(1)
