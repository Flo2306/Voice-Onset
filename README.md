# Voice-Onset

This module can be used to estimate word onset data using a method that is based on voice transcription. It works by continuously splitting the audio file until the voice recognition just recognizes the input word. It also allows for words with high similarity (e.g., ship & boat) to be considered correct responses depending on a value you can decide yourself. Now why would you use my approach compared to other approaches available already?

Pro:

- It is similarly accurate to existing approaches (e.g. high correlation r=0.8 with Chronset).
- It allows for automatic target word application (e.g. the picture shown is a boat and only if the said word is "boat", the algorithm will return the onset value)
- It allows for the target word to be semantically related to the shown picture (e.g. the picture shown is a boat and the said word is "ship", the response would still be considered correct)

Con:

- The audio quality plays a big role in how many audio files are classified. Using a computer microphone, we lost about 15% of the data to the voice transcription not recognizing the correct word.
- It can take quite some time as it is splitting the recording multiple times (a 5 second recording takes about 12 seconds to process on a MacbookAir 2020 with a M1 chip, the algorithm has a complexity of log(n))

The idea for this project came about in a research internship at the University of Sydney. In the experiment, pictures were shown and participants had to name the object they saw. As I was unaware that there were other softwares available (e.g. Chronset), I decided to try and write my own function. I decided to use a binary search + transcribe approach which, to my knowledge, has not been used before this way. I am currently in the process of writing a paper about this and I hope to publish within this year.

The use case I can think of the most is to use it in response time related experiments using verbal responses. It can be used to automate almost the whole process of analyzing data as it returns the onset times and determines whether the word is close enough to the target word/right response. An example of how this could work can be found using the example\_analysis function.

Potential future functions could expand to keyword search in audio recordings as the approach should work for this kind too. Another potential expansion is to implement different ways of voice recognition which could improve the accuracy of the algorithm.

# Installation

To install this module, you can use the following code in your python terminal: 

pip install git+https://github.com/Flo2306/Voice_Onset

# Usage 

You can either write your own code using my function or you can use the user interface (GUI). In case you want to write your own code, you can find an example of how to do this in the sample experiment. If you want to use the GUI, you can simply use these two lines: 

"

from Voice_Onset import GUI

GUI()

"

The GUI should open now from which you can continue everything automatically yourself. 

# Troubleshooting 

## Issue with FLAC

For Mac users, you need to install a program needed to deal with FLAC files as it is part of the necessary modules. You can do so by first installing brew if you do not have it, more information under https://brew.sh. Next, you need to install the program to deal with the FLAC files using brew install flac in your terminal. 

## Connection reset by peer 

This issue is related to the connection to Google Transcribe and a potential overload/overuse of their connection. As of now, I have not found a good solution for this issue to continue analysing the data automatically. If you are using the GUI, you will have to select the data folder again. There will be an additional CSV file in the data folder telling showing the current process for each data file. If this file is deleted, the program will start from the beginning. This issue usually occurs when you process many audio files (for me it happened after processing 4000 audio files) so I hope you do not have to restart it many times. 

# Acknowledgements

We acknowledge contributions from Niels O. Schiller, Bob Slevc and Michael Nunez. 

## Authors

The current members of this module are:

Florian Burger, [f.burger@uva.nl](mailto:f.burger@uva.nl)

Denise Moerel, [denise.moerel@sydney.edu.au](mailto:denise.moerel@sydney.edu.au)

Thomas A. Carlson, [thomas.carlson@sydney.edu.au](mailto:thomas.carlson@sydney.edu.au)

In case you have any questions/feedback, please contact Florian Burger. 

