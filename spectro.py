# File Name: spectro.py
# File Authors: Safwan Diwan and Mikkel Folting
# Date: November 18, 2022
# Description: This script takes in a .wav file and displays a spectrogram of frequencies in that .wav file

import math
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

# Read our .wav file and extract windows with frequencies  
def readWav(wavFile):
  # Open wav file and retrieve number of frames
  wav = wave.open(wavFile)
  params = wav.getparams()  
  print(params)
  nframes = params[3]

  # Set up variables to use in loop over all frames
  count = 0
  windows = []
  sampleList = []

  # Set up hanning with 400 values to smooth edges of our windows
  hanning = np.hanning(400)

  # Iterate over all frames/samples in our audio file
  for num in range (nframes):
    # Read the next sample, convert to an integer, and add to our sample list
    sample = wav.readframes(1)
    sample = (np.frombuffer(sample, dtype='int16'))[0]
    sampleList.append(sample)
    count += 1

    # Once our count is 400, our window is complete, so we want to apply our hanning and add to our list of windows
    if count == 400:
      hanninged = [hanning[i] * sampleList[i] for i in range(len(sampleList))]
      windows.append(hanninged)

      # Simulate moving 10 ms forward in file by not ignoring the 15 ms overlap between windows
      # There are 240 samples in 15 ms, so set count back to 240
      # Add the last 240 samples from the previous sampleList into the new sampleList and add from that point forward
      count = 240
      sampleList = sampleList[-240:]

  # Close audio file and return list of windows containing lists of frequencies in that window
  wav.close()
  return windows


# Compute FFT for all of our windows
def fft(windows):
  fftWindows = []

  # Run every window through the Fast Fourier Transform (FFT) and append to fftWindows
  for list in windows:
    fftWindows.append(np.fft.rfft(list))

  # Now we must compute the magnitudes of each of these indices (ignore the imaginary number part)
  magWindows = []
  count = 0
  for window in fftWindows:
    singleWindow = []

    # Iterate through the current window and calculate the square and log magnitude at each sample using the real and imaginary numbers calculated there
    for frequency in window:
      squareMag = math.sqrt((frequency.imag ** 2) + (frequency.real ** 2))
      logMag = 10 * math.log(squareMag, 10)
      singleWindow.append(logMag)
    magWindows.append(singleWindow)
    count += 1
  return magWindows

# Normalize our frequency magnitudes 
def normalize (magWindows):
  minVal = float("inf")
  maxVal = float("-inf")
  # Find the global maximum and minimum frequency magnitude among all windows
  for list in magWindows:
    listMax = max(list)
    listMin = min(list)
    if listMax > maxVal:
      maxVal = listMax
    if listMin < minVal:
      minVal = listMin

  # Normalize every value in each frequency magnitude list
  normalMagWindows = []
  for list in magWindows:
    normalList = []
    for val in list:
      normalized = (val - minVal) / (maxVal - minVal)
      normalList.append(normalized)
    normalMagWindows.append(normalList)
  print(maxVal)
  print(minVal)
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
  print(windows[50], len(windows), len(windows[50]))
  magWindows = fft(windows) # Contains a list of lists. Outer list is each window and inner list is each magnitude.
  print(magWindows[50], len(magWindows), len(magWindows[50]))
  normalMagWindows = normalize(magWindows)
  print(normalMagWindows[50], len(normalMagWindows), len(normalMagWindows[50]))
  plot(normalMagWindows)

  return

if __name__ == '__main__':
  main()