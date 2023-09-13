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

Once this has been reviewed and accepted by JOSS, I will also make it available on PyPI

# Usage 

You can either write your own code using my functions or you can use the user interface (GUI). In case you want to write your own code, you can find an example of how to do this in the sample experiment. If you want to use the GUI, you can simply use these two lines: 

"

from Voice_Onset import GUI

GUI()

"

The GUI should open now from which you can continue everything automatically yourself. 

# Performance

Given that this approach is used to find voice onset times, it is important to consider multiple factors of this module such as reliability and validity. To do so, multiple different datasets were analysed and compared in terms of the test-retest reliablitiy, concurrent validity, and construct validity. 

## Test-retest reliability 

To investigate whether our model performed consitsently, the same data was analysed twice. Onset times from the second time were subtracted from the first time. The mean and sd of this variable should be equal to 0 as this would indicate consistency across trials. The results for 458 audio files collected in the experiment described above show that the mean and sd of the variable were exactly equal to 0. Therefore, this approach has high test-retrest reliability. 

## Concurrent validitiy 

To investigate the concurrent validity of our model, we compared our results both to previous data which was marked by human raters as well as using Chronset (Roux et al., 2016) on the 458 observations mentioned above. Human raters are regared as the gold-standard of voice onset and Chronset has been able to very accurately predict these values. 

### Comparison to Chronset. 

To investigate the relationship between our model and 

### Comparison to Human Raters

Secondly, the relationship between our model and values previously annontated by human raters were compared to the values returned by our model. In total, 2559 audio files were compared. Assumptions were checked but no violation of the assumptions was found. There was a significant positive correlation between the onset times from our model and the onset times from human rater, r(2559) = .89, p < .001. Additionally, a linear regression with the onset times of the human raters as a dependent variable and the onset times of our model as the independent variable was run. The results show that our model predicts the values accurately, R^2 = .789, F(1, 2554) = 9537.63, p <.001. Based on these results, our model perform similar to the onset times of human raters. 

## Construct Validity 

To investigate the construct validity of our model, we added five seconds of silence at the beginning of each of the 458 audio files. If our model had construct validity, we found find that the difference between our original onset times and the onset times with five seconds of silence is exactly 5s. As we violated the assumption of normality for this variable, we used a non-parametric Wilcoxon sign-rank test. We found a mean of 4.93 and a sd of 0.428. However, this also includes some potential outliers that were not removed from the data to keep a realisitc representation of the performance. The results indicate that there was no difference between our created variable and 5s, W (457) = 50143.00, p = .395. Therefore, we can conclude that our approach also has construct validity. 

## Conclusion

Based on these results, we can see that our approach works and delivers accurate estimations of voice onset data. However, Chronset (Roux et al., 2016) performs better than our model based on the results of their study. Future improvements in accuracy of voice transcription could also lead to improved accuracy of this approach. However, currently Chronset outperforms our approach. One advantage of our approach is the already mentioned NLP use which allows for complete automation of the analysis. 


# Troubleshooting 

## Issue with FLAC

For Mac users, you need to install a program needed to deal with FLAC files as it is part of the necessary modules. You can do so by first installing brew if you do not have it, more information under https://brew.sh. Next, you need to install the program to deal with the FLAC files using brew install flac in your terminal. 

## Connection reset by peer 

This issue is related to the connection to Google Transcribe and a potential overload/overuse of their connection. As of now, I have not found a good solution for this issue to continue analysing the data automatically. If you are using the GUI, you will have to select the data folder again. There will be an additional CSV file in the data folder telling showing the current process for each data file. If this file is deleted, the program will start from the beginning. This issue usually occurs when you process many audio files (for me it happened after processing 4000 audio files) so I hope you do not have to restart it many times. 

# Acknowledgements

We acknowledge contributions from Niels O. Schiller, Bob Slevc and Michael Nunez. 

# Authors

The current members of this module are:

Florian Burger, [f.burger@uva.nl](mailto:f.burger@uva.nl)

Denise Moerel, [denise.moerel@sydney.edu.au](mailto:denise.moerel@sydney.edu.au)

Thomas A. Carlson, [thomas.carlson@sydney.edu.au](mailto:thomas.carlson@sydney.edu.au)

In case you have any questions/feedback, please contact Florian Burger. 

