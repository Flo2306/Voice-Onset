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

---

---
title: 'Gala: A Python package for galactic dynamics'
tags:
  - Python
  - astronomy
  - dynamics
  - galactic dynamics
  - milky way
authors:
  - name: Adrian M. Price-Whelan
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Author Without ORCID
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Author with no affiliation
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: 3
affiliations:
 - name: Lyman Spitzer, Jr. Fellow, Princeton University, USA
   index: 1
 - name: Institution Name, Country
   index: 2
 - name: Independent Researcher, Country
   index: 3
date: 13 August 2017
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---
# Summary

This module allows automatic analysis of voice onset times and whether the response 
was correct or not. 

It finds the onset times of words by using a binary search implementation
in combination with word recognition. Binary search for finding voice onset in audio files works 
by repeatedly dividing the file into smaller intervals, transcribing the midpoint of each interval, 
and narrowing down the search area until the precise onset time of the word is determined. Essentially, 
you can think of the audio file as a sorted list and the word recognition as our criteria to move the mid-point 
up or down. 

Additionally, it automatically decides whether a response is correct or almost correct (e.g. fries 
and chips). In the example, both mean the same thing and have the same underlying concept 
with the only difference being the accent used. It does this by automatically determining correct 
answers using NLP models and cosine similarity. The exact threshold for correctness can be customized, 
and a built-in tool aids in threshold selection. Additionally, the model that will be used can be selected. 

# Statement of need

Unlike previous approaches that rely solely on acoustic information 
from the audio to find the correct onset, this approach combines binary search with 
word recognition. It overcomes issues caused by filler words or coughs before the word, 
as it identifies the point where it can 'just' transcribe the word. 

Additionally, it automatically decides whether a response is correct or almost correct (e.g. fries 
and chips). In the example, both mean the same thing and have the same underlying concept 
with the only difference being the accent used. Using an approach like this has, to my knowledge, 
not been done before either as it always involved a human rater determining whether the answer 
is correct or not. Using this module, the analysis of audio recordings can mostly be done automatically 
but I do still recommend checking some parts manually as the quality of the recordings and the set-up 
of your experiment can influence the accuracy. 

# Acknowledgements

We acknowledge contributions from Niels O. Schiller, Bob Slevc, and Michael Nunez.

