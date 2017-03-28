import numpy as np
from scipy.fftpack import fft , fft2 , rfft
import matplotlib.pyplot as plt
import time

freq = 32
sampling_rate=55

t= np.linspace (0, 2, 2 *sampling_rate, endpoint=False)
x1= np.sin(freq* 2* np.pi * t)
x2= np.cos(5* 2* np.pi * t)
x3= np.sin(25* 2* np.pi * t)

x=x1+x2+x3

fig = plt.figure(1)
ax1 = fig.add_subplot(211)
ax1.plot(t, x)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Signal amplitude');

fx = fft(x)
freqs = np.fft.fftfreq(len(x)) * sampling_rate


ax2 = fig.add_subplot(212)
ax2.stem(freqs, np.abs(fx))
ax2.set_xlabel('Frequency in Hertz [Hz]')
ax2.set_ylabel('Frequency Domain (Spectrum) Magnitude')


plt.show()
