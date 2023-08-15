---
title: 'Voice_Onset: Binary Search in Combination with Word Recognition to Find Voice Onset Times'
tags:
  - Python
  - Linguistics
  - Voice Onset
  - NLP
  - Word Recognition
authors:
  - name: Florian Burger
    orcid: 0000-0003-4745-5515
    corresponding: true
    affiliation: "1, 2" 
    email: f.burger@uva.nl
  - name: Denise Moerel
    orcid: 0000-0001-9677-0170
    affiliation: 2
  - name: Thomas A. Carlson
    orcid: 0000-0002-3953-4195
    affiliation: 2
affiliations:
 - name: University of Amsterdam, The Netherlands
   index: 1
 - name: University of Sydney, Australia
   index: 2
date: 15 August 2023
bibliography: paper.bib
---

# Summary

This module can be used to find voice onset times (when somebody begins to speak) in audio files. It can also determine automatically whether the response was correct or not. 

It finds the voice onset times by using a binary search algorithm in connection with word recognition. It first finds a target word (or is given a target word) and then continuously splits the audio file in half using a binary search approach until the word recognition is able to "just" find the target word at which point it decides that this is the voice onset. 

Additionally, it automatically decides whether the answer given was correct or not in case a specific target word is given. It uses cosine similarity and NLP models to determine whether the words are close or not. For example, chips and fries have the same underlying concept but could be considered wrong answers without the use of NLP. It uses a pre-defined threshold to decide whether a word is correct or not. The GUI also includes a visual representation where users can find a value optimal for their research by trying out different words and seeing how similar they are. 

# Statement of need

Using the described approach allows for two advantages compared to previous approaches. Until now, to my knowledge, approaches to determine voice onset times used acoustic features of the recording to determine when a person starts speaking. While this approach often works out nicely, it can be confused by responses of participants coughing or saying filler words such as "ah". My algorithm does not deal perfectly with these issues either but that is mostly due to the audio quality of my recordings. I assume that it would work better if the audio quality goes beyond the in-built microphone of a computer. Secondly, the use of NLP models allows the decision of whether a word is correct or not to be determined automatically. Until now, to my knowledge, this decision was done manually. I would still recommend checking the results manually but the bulk of work should be taken away by using this approach. 


# Acknowledgements

We acknowledge the work of Bob Slevc, Niels O. Schiller, and Michael Nunez all aiding this project with data or technical help. 


# References
