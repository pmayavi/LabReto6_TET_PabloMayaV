#!/usr/bin/python

import os
import sys
import glob
import codecs

# Editado del original porque tenia errores

inputdir = "."

if len(sys.argv) >= 2:
    inputdir = sys.argv[1]


def processdir(dir):
    dirList = glob.glob(dir)
    wordcount = {}
    for f in dirList:
        wordcountfile(f, wordcount)
    for w in wordcount:
        print(w, wordcount[w])


def wordcountfile(f, wordcount):
    file = codecs.open(f, "r", "utf-8")
    for word in file.read().split():
        word = word.lower()  # Convert word to lowercase
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    file.close()
    return wordcount


processdir(inputdir)
