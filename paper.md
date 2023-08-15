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

# Summary

This module allows automatic analysis of voice onset times and whether the response 
was correct or not. Unlike previous approaches that rely solely on acoustic information 
from the audio to find the correct onset, this approach combines binary search with 
word recognition. It overcomes issues caused by filler words or coughs before the word, 
as it identifies the point where it can 'just' transcribe the word. Additionally, it 
automatically determines answer correctness using NLP models and cosine similarity. 
The exact threshold for correctness can be customized, and a built-in tool aids in 
threshold selection.

# Acknowledgements

We acknowledge contributions from Niels O. Schiller, Bob Slevc, and Michael Nunez.

