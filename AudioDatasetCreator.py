import torch
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from subprocess import call
import os
import argparse
from scipy.io import wavfile
import matplotlib.pyplot as plt
from random import randint

# import sys

'''
Note: ffmpeg needs to be installed in the directory running this script in order to operate successfully.
'''


# def parse_args(argv):
def parse_args():
    parser = argparse.ArgumentParser(description="Guitar Chord Classifier")
    parser.add_argument(
        "--dataset",
        default=None,
        type=str,
        help="Training dataset Location"
    )
    parser.add_argument(
        "--epochs",
        default=100,
        type=int,
        help="Number of epochs (default: %(default)s)"
    )
    parser.add_argument(
        "--batch_size",
        default=16,
        type=int,
        help="Batch Size used for training (default: %(default)s)"
    )
    parser.add_argument(
        "--pathToSaveUnscaledAudio",
        default=r'C:/Users/Daniel/Desktop/GuitarProject/DLMethod/ChordAudio/AudioWavUnscaled/',
        type=str,
        help="Location to save created Audio Files (default: %(default)s)"
    )
    parser.add_argument(
        "--randomAudioFile",
        default=True,
        type=bool,
        help="Whether Audio file should be created in a random fashion (default: %(default)s)"
    )
    parser.add_argument(
        "--createWav",
        default=False,
        type=bool,
        help="Whether dataset and audio files need to be created (default: %(default)s)"
    )
    parser.add_argument(
        "--locOfScaledWavFiles",
        default=r'C:/Users/Daniel/Desktop/GuitarProject/DLMethod/ChordAudio/AudioWavScaled/',
        type=str,
        help="Directory containing the usable wave Audio files. Usually the same as the save location. "
             + "(default: %(default)s)"
    )
    parser.add_argument(
        "--totalAudioTime",
        default=900,
        type=int,
        help="Total Audio time in seconds (default: %(default)s)"
    )
    parser.add_argument(
        "--datasetDirectory",
        default=r'C:/Users/Daniel/Desktop/GuitarProject/DLMethod/ChordAudio/AudioDataset/',
        type=str,
        help="Directory of dataset (default: %(default)s)"
    )

    # args = parser.parse_args(argv)
    args = parser.parse_args()
    return args


def convert_mp3_to_wav(audioPathList,
                       pathToSave):
    """
    :param audioPathList: List Containing all audio paths
    :return: NewAudioPaths, a list of new audioPaths. Saves converted files to desired directory
    """
    newAudioPaths = list(range(len(audioPathList)))

    for x in range(len(audioPathList)):
        curAudioPath = str(audioPathList[x])
        fileNameBase = os.path.basename(curAudioPath)
        fileNameNoExt = os.path.splitext(fileNameBase)
        fileName = fileNameNoExt[0]
        newPath = pathToSave + str(fileName) + ".wav"
        newAudioPaths[x] = newPath

        command = "ffmpeg -i " + curAudioPath + " -ab 160k -ac 2 -ar 44100 -vn " + newPath
        call(command, shell=True)

    return newAudioPaths


def min_max_wav_data(audioPathList, pathToSaveDirectory):
    audioData = list(range(len(audioPathList)))
    sampleRate = list(range(len(audioPathList)))

    for x in range(len(audioPathList)):
        fileNameBase = os.path.basename(audioPathList[x])
        fileNameNoExt = os.path.splitext(fileNameBase)
        fileName = fileNameNoExt[0] + '.wav'

        scaler = MinMaxScaler(feature_range=(-1, 1))
        sampleRate[x], audioTempData = wavfile.read(audioPathList[x])
        audioData[x] = scaler.fit_transform(audioTempData)

        saveFileLoc = os.path.join(pathToSaveDirectory, fileName)
        wavfile.write(saveFileLoc, sampleRate[x], audioData[x])


def create_audio_dataset(audioPathList,
                         pathToDataDirectory,
                         totalAudioTime=900,
                         randomized=True
                         ):
    """

    :param audioPathList: List containing all the paths to the usable audio files/clips
    :param totalAudioTime: Number of seconds for the output to be. Default = 900 seconds
    :param randomized: Whether Audio Files should be used in a random order. Default = True
    :return: Dataset Audio file Path and respective labels path based on sampling rate. Saves Audio File to that location.
    """

    # create list housing the Audio Data, labels and Sampling Rates

    audioData = list(range(len(audioPathList)))
    sampleRate = list(range(len(audioPathList)))
    nameIndexList = list(range(len(audioPathList)))

    for x in range(len(audioPathList)):
        fileNameBase = os.path.basename(audioPathList[x])
        fileNameNoExt = os.path.splitext(fileNameBase)
        fileName = fileNameNoExt[0]

        nameIndexList[x] = str(fileName)
        sampleRate[x], audioData[x] = wavfile.read(audioPathList[x])

    for x in range(600):
        if x == 0:
            tempRand = randint(0, len(audioPathList) - 1)
            tempVal = audioData[tempRand]
            audioDataSet = tempVal
            labelDataSet = [nameIndexList[tempRand]] * (tempVal.shape[0])
        else:
            tempRand = randint(0, len(audioPathList) - 1)
            tempVal = audioData[tempRand]
            audioDataSet = np.concatenate((audioDataSet, tempVal), axis=0)
            labelDataSet = labelDataSet + [nameIndexList[tempRand]] * tempVal.shape[0]

    locOfDatasetWav = os.path.join(pathToDataDirectory, 'dataset.wav')
    locOfDatasetCsv = os.path.join(pathToDataDirectory, 'dataset.csv')
    dfLabelDataSet = pd.DataFrame(labelDataSet)
    dfLabelDataSet = dfLabelDataSet.rename(columns={0: 'ChordPlayed'})

    dfLabelDataSet.to_csv(locOfDatasetCsv)
    wavfile.write(locOfDatasetWav, sampleRate[0], audioDataSet)

    return locOfDatasetWav, locOfDatasetCsv


def get_audio_paths(directoryOfAudio):
    """
    Should be already scaled audio
    :param directoryOfAudio: audio directory of WAV files
    :return: List of audio file paths
    """
    audioPaths = []
    for path in os.listdir(directoryOfAudio):
        full_path = os.path.join(directoryOfAudio, path)
        if os.path.isfile(full_path):
            audioPaths.append(full_path)
    return audioPaths


def main():
    args = parse_args()
    if args.createWav == True:

        mp3AudioPaths = [r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\A7.mp3',
                         r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\B7.mp3',
                         r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\C7.mp3',
                         r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\D7.mp3',
                         r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\E7.mp3',
                         r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\F7.mp3',
                         r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\G7.mp3'
                         ]
        pathToSave = args.pathToSaveUnscaledAudio
        wavAudioPathsUnscaled = convert_mp3_to_wav(mp3AudioPaths, pathToSave)
        wavAudioPathsScaled = min_max_wav_data(wavAudioPathsUnscaled, args.locOfScaledWavFiles)

    else:
        # Get audio Paths from Directory
        wavAudioPathsScaled = get_audio_paths(args.locOfScaledWavFiles)

    dataSetPathWav, dataSetPathCsv = create_audio_dataset(wavAudioPathsScaled,
                                                          args.datasetDirectory,
                                                          args.totalAudioTime,
                                                          args.randomAudioFile)


if __name__ == '__main__':
    main()
