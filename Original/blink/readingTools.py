'''
TODO: figure out how to incorporate functions from preprocessing module 
'''

import numpy as np
from scipy import stats
import biosppy.signals as bsig
import csv
import math as m

def rowskip(data):
    """
    Determines the number of lines to skip as start of csv for EEG data_stim

    Arguments:
        data: csv file name of the labels

    Returns:
        Appropriate value to pass for skiprows in np.loadtxt
    """
    with open(data, newline='') as f:
        reader = csv.reader(f)
        row1 = next(reader)
    return int(row1[1])+2


def get_corrupt(data):
    """
    Obtains the start and end timestamps for each corrupt period as ints

    Arguments:
            data: csv file name for labels

    Returns:
            corrupt: array of pairs of indeces denoting start and end of corruption
    """
    with open(data, newline='') as f:
        reader = csv.reader(f)
        row1 = next(reader)

        corrupt = []
        for i in range(int(row1[1])):
            corrupt.append(next(reader))

        #There has to be a better way to accomplish what I'm about to do
        corrupt = [list(map(float, item)) for item in corrupt]  #string to flot
        corrupt = [np.floor(entry) for entry in corrupt]  #float floored
        corrupt = [list(map(int, item)) for item in corrupt]  #flot to int
        return corrupt


def get_corrupt_indeces(label_file, sr):
    """
    interpolates from start-end timestamps to obtain an array of every index
    which corresponds to a corrupted instance

    Arguments:
            label_file: csv filename for labels for a single subject
    """
    filledin = np.array([])
    bad = get_corrupt(label_file)
    for i in range(len(bad)):
        start = m.floor(bad[i][0]*sr)
        stop = m.floor(bad[i][1]*sr)
        elong = (np.linspace(start, stop, stop-start))
        filledin = np.concatenate((filledin, elong))
    return filledin.astype(int)

#These require functions from preprocessing
'''def lbl_wo_corrupt(label_file, timestamps, sr, length, window_size, window_step):
    """
    PREAMBLE: takes in label_file to determine corrupt instances,
    uses get_corrupt_indeces function to return every index of a
    corrupt channel, use label_from_timestamps function to elongate
    list of provided timestamps for blinks, make every instance which
    is corrupt a 2, containment to obtain labelled window, get rid of
    windows with title 2
    returns: all non-corrupt windowed-labels, all windowed labels (to be used
    to get rid of corrupt epochs later)

    Arguments:
       label_file: filename for csv of labels
       timestamps: csv of timestamps
       sr: sampling rate
       length: length of eeg channel (i.e number of datum in an eeg channel)
       window_size: number of data points in training input elements
       window_step: increment for "lateral" window shift across all data
    """
    labels = labels_from_timestamps(timestamps, sr, length)
    corrupt_indeces = get_corrupt_indeces(label_file, sr)
    labels[corrupt_indeces] = 2
    windowed_raw = label_epochs(labels, window_size, window_step, max)
    windowed_refined = [window for window in windowed_raw if window != 2]
    return windowed_refined, windowed_raw

def epoch_subject_data(dataset, window_size, window_step, sensor):
    """
    Iterates through large array of subjects and returns one array containing
    unfiltered training data

    Arguments:
          dataset: array of subjects and subject eeg voltages
          window_size, window_step: see above
          sensor: refers to which data channel you wish to generate data from

    Returns:
          subject_epochs: array of all subject epochs for training (unfiltered)
    """
    placeholder = np.array(dataset)
    number_of_subjects = len(dataset) #change this to first value in shape array since one dimensional might just give a shit ton of stuff
    subject_epochs = []

    for i in range(number_of_subjects):
        subject_data = placeholder[i]
        channel_of_interest = subject_data[:,sensor]
        epoched = epoch(channel_of_interest, window_size, window_step)

        for j in range(len(epoched)):
            subject_epochs.append(epoched[j])

    return np.array(subject_epochs)


def epoch_subject_labels(dataset, labels, label_files, sr, window_size, window_step, mode='default'):
    """
    will return the refined labels, raw labels to be used for refining the
    data epochs. takes in the array of subject blink timestamps, NOT individual.

    Arguments:
       dataset: array of eeg data for subjects.  used for determining length parameter in labelling function
       labels: array of timstamps
       label_files: label csv filenames
       mode: 'default' returns raw and refined labelled windows (ie. including corrupt
       vs no corrupt channels). 'only_raw' returns every possible label window regardless
       of corruption

    Returns:
       raw or refined (no corrupt) labelled windows
    """
    number_of_subjects = len(labels)
    placeholder1 = np.array(labels)
    placeholder2 = np.array(dataset)  #need this for the length parameter

    subject_labels_raw = []
    subject_labels_refined = []

    for i in range(number_of_subjects):
        subject_labels = placeholder1[i]
        subject_data = placeholder2[i]
        subject_len = len(subject_data[:,0])
        refined, raw = lbl_wo_corrupt(label_files[i], subject_labels, sr, subject_len, window_size, window_step)

        for j in range(len(raw)):
            subject_labels_raw.append(raw[j])

        for k in range(len(refined)):
            subject_labels_refined.append(refined[k])

    if mode=='only_raw':
        return np.array(subject_labels_raw)

    elif mode =='default':
        return np.array(subject_labels_raw), np.array(subject_labels_refined)
'''

def purify_epochs(epoched_data, raw_epoched_labels):
    """
    takes in the long list of raw epochs and returns only non-corrupt ones
    """
    indeces = np.where(raw_epoched_labels !=2)[0]
    return np.array(epoched_data[indeces])
