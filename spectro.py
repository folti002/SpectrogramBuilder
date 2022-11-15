import math
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

def readWav(wavFile):
  wav = wave.open(wavFile)
  params = wav.getparams()
  nframes = params[3]
  count = 0
  windows = []
  sampleList = []
  hanning = np.hanning(400)
  for i in range (nframes):
    sample = wav.readframes(1)
    sample = (np.frombuffer(sample, dtype='int16'))[0] # IS THIS CORRECT?
    sampleList.append(sample)
    count += 1
    if count == 400:
      hanninged = [hanning[i] * sampleList[i] for i in range(len(sampleList))]
      windows.append(hanninged)
      count = 240
      sampleList = sampleList[-240:]
  return windows

def fft(windows):
  fftWindows = []
  for list in windows:
    fftWindows.append(np.fft.fft(list))
  

def main():
  wavFile = sys.argv[1]
  windows = readWav(wavFile)
  magWindows = fft(windows)
  
  return

if __name__ == '__main__':
  main()