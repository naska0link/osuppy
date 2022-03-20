import numpy as np
from scipy.io import wavfile
from osuppy.osb import *

import pylab as plt
import math
import os
import re

alt_file_name = {
    "#": "pound",
    "%": "percent",
    "&": "ampersand",
    "{": "leftCBracket",
    "}": "rightCBracket",
    "\\": "backSlash",
    "<": "leftABracket",
    ">": "rightABracket",
    "*": "asterisk",
    "?": "question",
    "/": "forward",
    " ": "blank",
    "$": "dollar",
    "!": "exclamation",
    ".": "period",
    "'": "single",
    '"': "double quotes",
    ":": "colon",
    "@": "at",
    "+": "plus",
    "`": "backtick",
    "|": "pipe",
    "=": "equal",
    " ": "space"
}


def convert_time(time):
    '''08:38:685
    \d{2}:\d{2}:\d{3}'''
    if type(time) == int:
        return str(time)
    elif type(time) == str:
        time = re.search(r'\d{2}:\d{2}:\d{3}', time)
        if time:
            return str(sum([int(t) * 60000 if i == 0 else int(t) * 1000 if i == 1 else int(t)
                            for i, t in enumerate(time.group().split(":"))]))
        else:
            raise ValueError(
                "Could not find correct time in provided value. Please make sure time is 00:00:000 format.")
    else:
        raise TypeError("Could not find time string in given time")


def audio_data(audiofile):
    # converts audiofile
    if type(audiofile) != str:
        raise TypeError("Audiofile name is not a string")
    elif not audiofile.endswith(".wav"):
        ValueError("Audio file is not a wav file")
    frame_rate, snd = wavfile.read("audio.wav")
    return plt.specgram(snd[:, 0],
                        NFFT=1024,
                        Fs=frame_rate,
                        noverlap=5,
                        mode='magnitude')


def audio_spectrum(audiofile, start=None, end=None, effect_range=(0, 1), listen_range=(0, 1), bars=1):
    specgrams, frequencies, t, im = audio_data(audiofile)
    if bars > (le := len(specgrams)):
        raise ValueError(f"Bars can not be greater than {le}")
    inc = (int(len(specgrams) * listen_range[1]) -
           int(len(specgrams) * listen_range[0])) // bars
    #
    if start == None:
        start = 0
    else:
        start = int(convert_time(start))
    if end == None:
        end = len(specgrams[0])//1000
    else:
        end = int(convert_time(end))
    r_list = []
    #
    for bar in range(bars):
        # averages the peak amplitudes of the frequency between desired frequency
        specrange_min = int(len(specgrams) * listen_range[0]) + (bar*inc)
        specgram_max = int(len(specgrams) * listen_range[1]) + ((bar+1)*inc)
        specgram_max = specgram_max if specgram_max <= int(
            len(specgrams) * listen_range[1]) else int(len(specgrams) * listen_range[1])
        specgram = np.average(
            specgrams[specrange_min:specgram_max], axis=0)
        # Highest and lowest points
        minimum = plt.amin(specgram)
        maximum = plt.amax(specgram)
        # Gives value an initial value, for the if statement to be able to check
        a_value = [
            (math.ceil(
                (((specgram[0] - minimum) / (maximum - minimum)) *
                 ((effect_range[1] - effect_range[0]) + effect_range[0])) * 1000) /
             1000, 0)
        ]
        # Loops through the specgram ands adds the values that are in the designated time to the value and time list
        for index, power in enumerate(specgram[start*1000:end*1000]):
            if (p := math.ceil(
                (((power - minimum) / (maximum - minimum)) *
                 ((effect_range[1] - effect_range[0]) + effect_range[0])) * 1000) /
                    1000) != a_value[-1][0] and index % 2 == 0:
                a_value.append((p, int(round(t[index] * 1000))))
        # Returns the value and time list, excluding the initial value of value as to align the two list correctly
        r_list.append(a_value[1:])
    return r_list
