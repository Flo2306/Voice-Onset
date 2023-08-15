---
title: 'Voice_Onset: Binary Search in Combination with Word Recognition to Find Voice Onset Times'
tags:
  - Python
  - Linguistics
  - Voice Onset
  - NLP
  - Word Recognition
  - Voice Analysis
authors:
  - name: Florian Burger
    orcid: 0000-0003-4745-5515
    equal-contrib: true
    affiliation: "1, 2"
  - name: Denise Moerel
    orcid: 0000-0001-9677-0170
    equal-contrib: false 
    affiliation: 2
  - name: Thomas A. Carlson
    orcid: 0000-0002-3953-4195
    equal-contrib: false 
    affiliation: 2
affiliations:
 - name: University of Amsterdam, The Netherlands
   index: 1
 - name: University of Sydney, Australia
   index: 2
date: 15 August 2023

# Summary
This Modul allows a automatic analysis of voice onset times and whether the response 
was correct or not. Until now, most approaches use accoustic information from the audio 
to find the correct onset. However, this approach can be inaccurate if participants use 
filler words or cough before saying the word. Using a binary search approach in combination 
with word recognition allows to not be limited by these issues as it will find the moment where 
it can 'just' transcribe the word. In addition, it allows to automatically decide whether an 
answer is correct or not using nlp models and cosine similarity. What exact value is used 
can be decided individually but there is a tool implemented that can help decide what 
threshold to use. 

# Acknowledgements

We acknowledge contributions from Niels O. Schiller, Bob Slevc and Michael Nunez. 
