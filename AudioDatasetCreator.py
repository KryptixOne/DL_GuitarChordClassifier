import torch
import sklearn as sk
import pandas as pd
import numpy as np
from subprocess import call
import os
import argparse
#import sys

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
        "--pathToSaveAudio",
        default=r'C:/Users/Daniel/Desktop/GuitarProject/DLMethod/ChordAudio/AudioWav/',
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
        "--locOfWavFiles",
        default=r'C:/Users/Daniel/Desktop/GuitarProject/DLMethod/ChordAudio/AudioWav/',
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

    # args = parser.parse_args(argv)
    args = parser.parse_args()
    return args


def convert_mp3_to_wav(audioPathList,
                       pathToSave):
    """
    :param audioPathList: List Containing all audio paths
    :return: NewAudioPaths, a list of new audioPaths. Saves converted files to desired directory
    """
    NewAudioPaths = range(audioPathList)
    for x in range(len(audioPathList)):

        curAudioPath = str(audioPathList[x])
        fileNameBase = os.path.basename(curAudioPath)
        fileNameNoExt = os.path.splitext(fileNameBase)
        fileName = fileNameNoExt[0]
        newPath = pathToSave + str(fileName) + ".wav"
        NewAudioPaths[x] = newPath

        command = "ffmpeg -i " + curAudioPath + " -ab 160k -ac 2 -ar 44100 -vn " + newPath
        call(command, shell=True)

    return NewAudioPaths


def create_audio_dataset(audioPathList,
                         totalAudioTime=900,
                         randomized=True
                         ):
    """

    :param audioPathList: List containing all the paths to the usable audio files/clips
    :param totalAudioTime: Number of seconds for the output to be. Default = 900 seconds
    :param randomized: Whether Audio Files should be used in a random order. Default = True
    :return: Dataset Audio file Path. Saves Audio File to that location.
    """


def get_audio_paths(directoryOfAudio):
    """
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
        pathToSave = args.pathToSaveAudio
        wavAudioPaths = convert_mp3_to_wav(mp3AudioPaths, pathToSave)
        create_audio_dataset(wavAudioPaths)
    else:
        # Get audio Paths from Directory
        wavAudioPaths = get_audio_paths(args.locOfWavFiles)

    dataSetPath = create_audio_dataset (wavAudioPaths, args.totalAudioTime, args.randomAudioFile)


if __name__ == '__main__':
    main()
