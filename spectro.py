import sys
import wave
import numpy as np

def readWav(wavFile):
  wav = wave.open(wavFile)
  params = wav.getparams()
  nframes = params[3]
  count = 0
  windows = []
  sampleList = []
  for i in range (nframes):
    sample = wav.readframes(1)
    sample = (np.frombuffer(sample, dtype='int16'))[0]
    sampleList.append(sample)
    if count == 400 or i == nframes - 1:
      windows.append(sampleList)
      count = 239
      sampleList = sampleList[-240:]
    count += 1
  return windows

def fft(windows):
  fftWindows = []
  for list in windows:
    # print(list)
    fftWindows.append(np.fft.fft([list]))
  print(fftWindows)

def main():
  wavFile = sys.argv[1]
  windows = readWav(wavFile)
  fft(windows)
  return

if __name__ == '__main__':
  main()