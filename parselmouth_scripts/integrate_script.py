"""
Listing 5: Already existing Praat scripts can be run through the parselmouth.praat.run and
parselmouth.praat.run file functions to interface with the use of Parselmouth objects and
standard Python variables.

https://ai.vub.ac.be/~yajadoul/jadoul_introducing-parselmouth_a-python-interface-to-praat.pdf
"""

import parselmouth
from parselmouth.praat import call, run_file

import numpy as np
import pandas as pd


def extract_syllable_intervals(file_name):
    print("Extracting syllable intervals from '{}'...".format(file_name))
    # Use Praat script to extract syllables
    objects = run_file('syllable_nuclei.praat', -25, 2, 0.3, file_name)
    textgrid = objects[1]
    n = call(textgrid, "Get number of points", 1)
    syllable_nuclei = [call(textgrid, "Get time of point", 1, i + 1)
                       for i in range(n)]
    # Use NumPy to calculate intervals between the syllable nuclei
    syllable_intervals = np.diff(syllable_nuclei)
    return syllable_intervals


def syllable_intervals_data(row):
    # Get file name of corpus audio file
    file_name_format = "corpus/dialectaccent_vol_01_{:02}{}_64kb.mp3"
    file_name = file_name_format.format(row['audio_id'], row['speaker'])

    # Extract syllables and intervals with previously defined function
    intervals = extract_syllable_intervals(file_name)

    # Return a new data frame with a row for each extracted interval
    return pd.DataFrame({'speaker': row['speaker'],
                         'native': row['native'],
                         'interval': intervals})

if __name__ == '__main__':

    corpus = pd.read_csv("corpus/corpus.csv")
    # Concatenate all data from the corpus into one big pandas DataFrame
    data = pd.concat([syllable_intervals_data(row) for _, row in corpus.iterrows()])
