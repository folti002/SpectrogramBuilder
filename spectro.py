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
  for window in fftWindows:
    singleWindow = []

    # Iterate through the current window and calculate the square and log magnitude at each sample using the real and imaginary numbers calculated there
    for frequency in window:
      squareMag = math.sqrt((frequency.imag ** 2) + (frequency.real ** 2))
      logMag = 10 * math.log(squareMag, 10)
      singleWindow.append(logMag)
    magWindows.append(singleWindow)
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
  return normalMagWindows

# Plot our frequency magnitudes
def plot (magWindows):
  plt.figure()

  # Converts our normalized list of lists of magnitude frequnecies into a np array and then transposes for correct format
  magnitudes = np.array(magWindows)
  magnitudes = magnitudes.transpose()

  # Create and show plot of pixels with higher intensities being darker colors
  plt.imshow(magnitudes, cmap = 'binary', interpolation='nearest', origin='lower')
  plt.show()

def main():
  # Read in the name of the wave file
  wavFile = sys.argv[1]

  # Create our windows by reading our waves 
  windows = readWav(wavFile) # Contains a list of lists. Outer list is each window and inner list is each sample.

  # Calculate the frequency magnitudes of our windows through the FFT
  magWindows = fft(windows) # Contains a list of lists. Outer list is each window and inner list is each magnitude.

  # Normalize our frequency magnitudes
  normalMagWindows = normalize(magWindows)

  # Plot our magnitudes!
  plot(normalMagWindows)
  return

if __name__ == '__main__':
  main()