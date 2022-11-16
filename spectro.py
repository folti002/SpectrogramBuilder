import math
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

def readWav(wavFile): # NOT SURE IF I AM ACCOUNTING FOR STEP CORRECTLY.
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
      hanninged = [hanning[i] * sampleList[i] for i in range(len(sampleList))] # IS THIS CORRECT?
      windows.append(hanninged)
      count = 240
      sampleList = sampleList[-240:]
  return windows

def fft(windows):
  fftWindows = []
  for list in windows:
    fftWindows.append(np.fft.rfft(list))
  magWindows = []
  for thing in fftWindows:
    singleWindow = []
    for val in thing:
      magnitude = ((val.imag)**2) + (val.real ** 2)
      squareMag = 10 * math.log(magnitude, 10)
      singleWindow.append(squareMag)
    magWindows.append(singleWindow)
  return magWindows

def normalize (magWindows):
  minVal = float("inf")
  maxVal = float("-inf")
  for list in magWindows: # Get max and min of lists to normalize
    listMax = max(list)
    listMin = min(list)
    if listMax > maxVal:
      maxVal = listMax
    if listMin < minVal:
      minVal = listMin
  normalMagWindows = []
  for list in magWindows:
    normalList = []
    for val in list:
      normalized = (val - minVal) / (maxVal - minVal)
      normalList.append(normalized)
    normalMagWindows.append(normalList)
  return normalMagWindows


def plot (magWindows):
  # I think plt.imshow may be helpful here. 
  # By using the rfft function, I believe this only outputs the necessary data (half the array).
  pixelPlt = plt.figure()
  magnitudes = np.array(magWindows)
  # magnitudes = magnitudes.reshape(len(magnitudes[0]), len(magnitudes))
  pixel_plot = plt.imshow(magnitudes, cmap = 'binary', interpolation='nearest', origin='lower')
  plt.show()

def main():
  wavFile = sys.argv[1]
  windows = readWav(wavFile) # Contains a list of lists. Outer list is each window and inner list is each sample.
  magWindows = fft(windows) # Contains a list of lists. Outer list is each window and inner list is each magnitude.
  normalMagWindows = normalize(magWindows)
  plot(normalMagWindows)
  return

if __name__ == '__main__':
  main()