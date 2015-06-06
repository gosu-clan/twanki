# Introduction
Early stage concept of how to learn Japanese using customise Twitter feeds.

This app consists of multiple steps:

- TWITTER: Connect and parse Twitter feed into a NoSQL database
    + Extract username, timestamp and tweet
    + Mecab (Japanese morphological analyser) to extract vocab/kanji compounds
    + Import into BlitzDB
- DICTIONARY: Convert JMDICT and KANJIDIC2 into a graph store for quick lookup (and just for fun)
    + Both JMDICT and KANJIDIC2 are in one database, which allows cross referencing without joins
- ANKI: Lookup definitions of each entry in BlitzDB in CayleyDB
    + Update BlitzDB entry with English meanings
    + Parse each document in the NoSQL database to be conducive to study
    + Import each document from BlitzDB into Anki
- **Actually learn some Japanese instead of stuffing around with programming**

# Requirements

## Executables

- Python3.4
- Mecab
- CayleyDB

## Python Packages

- blitzdb
- Mecab
- pprint
- requests
- tweepy
- lxml

## Dictionaries

- JMDICT
- KANJIDIC2

# Completed Features

- Twitter import into BlitzDB
- JMDICT && KANJIDIC2 import into CayleyDB

# TODO

- Command line arguments
- Anki Stuff
    + Anki plugin UI
    + Schema for Anki cards
    + Anki data import
 