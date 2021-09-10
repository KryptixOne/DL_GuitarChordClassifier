import torch
import sklearn as sk
import pandas as pd
import numpy as np
from pydub import AudioSegment
from subprocess import call
import os


def convert_mp3_to_wav(audioPathList,
                       pathToSave):
    """
    :param audioPathList: List Containing all audio paths
    :return: True is successful, False if fail. Saves converted files to desired directory
    """

    for x in range(len(audioPathList)):
        curAudioPath = str(audioPathList[x])
        fileNameBase = os.path.basename(curAudioPath)
        fileNameNoExt = os.path.splitext(fileNameBase)
        fileName = fileNameNoExt[0]
        newPath = pathToSave + str(fileName) + ".wav"

        command = "ffmpeg -i " + curAudioPath + " -ab 160k -ac 2 -ar 44100 -vn " + newPath
        call(command, shell=True)

    return True


def create_audio_dataset(audioPathList,
                         totalAudioTime=900,
                         randomized=True
                         ):
    """

    :param audioPathList: List containing all the paths to the usable audio files/clips
    :param totalAudioTime: Number of seconds for the output to be. Default = 900 seconds
    :param randomized: Whether Audio Files should be used in a random order. Default = True
    :return: Audio file
    """


if __name__ == '__main__':
    
    audioPaths = [r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\A7.mp3',
                  r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\B7.mp3',
                  r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\C7.mp3',
                  r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\D7.mp3',
                  r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\E7.mp3',
                  r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\F7.mp3',
                  r'C:\Users\Daniel\Desktop\GuitarProject\DLMethod\ChordAudio\G7.mp3'
                  ]
    pathToSave = r'C:/Users/Daniel/Desktop/GuitarProject/DLMethod/ChordAudio/AudioWav/'
    convertFiles = convert_mp3_to_wav(audioPaths,pathToSave)

