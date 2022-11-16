import math
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

def readWav(wavFile): # NOT SURE IF I AM ACCOUNTING FOR STEP CORRECTLY.
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
    sample = (np.frombuffer(sample, dtype='int16'))[0] # IS THIS CORRECT?
    sampleList.append(sample)
    count += 1

    # Once our count is 400, our window is complete, so we want to apply our hanning and add to our list of windows
    if count == 400:
      hanninged = [hanning[i] * sampleList[i] for i in range(len(sampleList))] # IS THIS CORRECT?
      windows.append(hanninged)

      # Simulate moving 10 ms forward in file by not ignoring the 15 ms overlap between windows
      # There are 240 samples in 15 ms, so set count back to 240
      # Add the last 240 samples from the previous sampleList into the new sampleList and add from that point forward
      count = 240
      sampleList = sampleList[-240:]

  # Close audio file and return list of windows containing lists of frequencies in that window
  wav.close()
  return windows

def fft(windows):
  fftWindows = []

  # Run every window through the Fast Fourier Transform (FFT) and append to fftWindows
  for list in windows:
    fftWindows.append(np.fft.rfft(list))

  # Now we must compute the magnitudes of each of these indices (ignore the imaginary number part)
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
  print(windows[-1])
  # magWindows = fft(windows) # Contains a list of lists. Outer list is each window and inner list is each magnitude.
  # normalMagWindows = normalize(magWindows)
  # plot(normalMagWindows)

  return

if __name__ == '__main__':
  main()