import Adafruit_ADS1x15
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft , fft2

GAIN = 1
adc = Adafruit_ADS1x15.ADS1015()

sps = input("Input Sampling Rate:     ")
time1 = input("Input sample time (seconds):     ")

def logdata():
    period = 1.0 / sps

    datapoints = int(time1*sps)
    dataarray=np.zeros([datapoints,2])

    adc.start_adc(0,gain=GAIN)

    print "Press ENTER to start sampling"	
    raw_input()

    startTime=time.time()
    t1=startTime
    t2=t1

    for x in range (0,datapoints) :
        dataarray[x,0]= adc.get_last_result()
        dataarray[x,1] = time.time()-startTime

        while (t2-t1 < period) :
            t2=time.time()
        t1+=period
    return (dataarray)

dataSamples = logdata()

xdata = [column[1] for column in dataSamples[1:len(dataSamples)]]
ydata = [column[0] for column in dataSamples[1:len(dataSamples)]]

printchoice=raw_input("Do you want to save data to CSV (Y/N): ")

if (printchoice == "Y" or "y") :
		np.savetxt('dataSamples4.txt',dataSamples, fmt='%.3f', delimiter = ',')

t= np.linspace (0, 2, 2 *sps, endpoint=False)
test=np.sin(25* 2* np.pi * t)
fy = fft(ydata)
freqs = np.fft.fftfreq(len(ydata)) * sps

print "Press ENTER to start plotting on Matlab"	
raw_input()
	
fig = plt.figure(1)
ax1 = fig.add_subplot(211)
ax1.plot(xdata,ydata)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Signal amplitude');

ax2 = fig.add_subplot(212)
ax2.stem(freqs, np.abs(fy))
ax2.set_xlabel('Frequency in Hertz [Hz]')
ax2.set_ylabel('Frequency Domain (Spectrum) Magnitude')

plt.show()

