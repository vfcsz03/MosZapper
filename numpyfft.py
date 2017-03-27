import numpy as np
from scipy.fftpack import fft , fft2
import matplotlib.pyplot as plt
import time
import Adafruit_ADS1x15

GAIN = 1
ADS1115 = 0x00

adc = Adafruit_ADS1x15.ADS1015()

N = input("Input # of points:     ")
T = 1.0/N

x=np.linspace(0, 2*np.pi*N*T, N)

y1= np.cos(20*x)
y2= np.sin(10*x)
y3= np.sin(5*x)

y= y1+y2+y3
#print (y)
np.savetxt('npyFFTy.txt',y, fmt='%.3f', delimiter = ',')
fy= fft(y)
np.savetxt('npyFFTfy.txt',fy, fmt='%.3f', delimiter = ',')
xf= np.linspace(0.0, 1.0/(2.0*T), N/2)

fig = plt.figure(1)
ax1 = fig.add_subplot(411)
plt.plot(x, y, 'r')
fig = plt.figure(1)
ax1 = fig.add_subplot(412)
plt.plot(xf, (2.0/N)*np.abs(fy[0:N/2]))

def split_array(a_list):
    half= np.hsplit(a_list,2)
    return a_list[half:]

def Start():
    time1 = input("Input sample time (seconds):     ")
    N=64
    period= 1/64
    
    
    datapoints = int(time1*N)
    dataarray=np.zeros([datapoints,2])
    #timearray=np.zeros([datapoints,1])

    adc.start_adc(0,gain=GAIN)
    print "Press ENTER to start sampling"	
    raw_input()

    startTime=time.time()
    t1=startTime
    t2=t1

    for x in range (0,datapoints) :
            dataarray[x,0]= adc.get_last_result()
            dataarray[x,1] = time.time()-startTime
            #timearray[x] = time.time()-startTime
            while (t2-t1 < period) :
                t2=time.time()
            t1+=period
    return (dataarray)

dataSamples = Start()
print "done sampling"
printchoice=raw_input("Do you want to save data to CSV (Y/N): ")
if (printchoice == "Y" or "y") :
		np.savetxt('npyFFT.txt',dataSamples, fmt='%.3f', delimiter = ',')
		
number_samples = len(dataSamples)
sampleIntervals = np.zeros(number_samples-1)

for i in range(0, number_samples-1):
    sampleIntervals[i]=dataSamples[i+1,1]-dataSamples[i,1]

timearray = dataSamples[:,[0]]    
fz = fft(timearray)
fz2= np.abs(fz)
np.savetxt('npyFFTtime.txt',timearray, fmt='%.3f', delimiter = ',')
np.savetxt('npyFFTfz.txt',fz, fmt='%.3f', delimiter = ',')
f = [column[0] for column in dataSamples[1:len(dataSamples)]]
h = (2.0/N)*np.abs(fz[0:N/2])
e = [column[1] for column in dataSamples[1:len(dataSamples)]]
np.savetxt('npyFFTh.txt',h, fmt='%.3f', delimiter = ',')

fig2 = plt.figure(1)
ax2 = fig2.add_subplot(413)
plt.scatter (e,f ,color='g')

fig3 = plt.figure(1)
ax3 = fig3.add_subplot(414)
#plt.plot(h,f)
plt.show()
    
