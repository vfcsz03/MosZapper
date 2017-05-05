import Adafruit_ADS1x15
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft , fft2
import RPi.GPIO as GPIO

#Pin Def
detect = 24 #BCM, actual pin 18
zapOpen = 23 #BCM, actual pin 16

#Pin Config
GPIO.setmode(GPIO.BCM)
GPIO.setup(detect, GPIO.IN)
GPIO.setup(zapOpen, GPIO.OUT)

GAIN = 1
adc = Adafruit_ADS1x15.ADS1015()
sps = input("Input Sampling Rate:     ")
time1 = input("Input sample time (seconds):     ")

def logdata():
    period = 1.0 / sps

    datapoints = int(time1*sps)
    dataarray=np.zeros([datapoints,2])

    adc.start_adc(0,gain=GAIN)

    #print "Press ENTER to start sampling"	
    #raw_input()
    
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
    time.sleep(.05)

def feedback():
    GPIO.output(zapOpen, GPIO.HIGH)
    time.sleep(.1)
    zap = GPIO.input(detect)
    time.sleep(20)
    GPIO.output(zapOpen, GPIO.LOW)
    
##    zapArray[i]=zap
##    np.savetxt('zap.txt',zapArray, fmt='%.3f', delimiter = ',')
    

def main():
    #while(1):
        dataSamples = logdata()
        signal = [column[0] for column in dataSamples[1:len(dataSamples)]]
        timeX = [column[1] for column in dataSamples[1:len(dataSamples)]]
        
        transformedSignal = fft(signal)
        frequencyMagnitude = np.abs(transformedSignal)
        frequencyAxis = np.fft.fftfreq(len(signal)) * sps
        
        filteredFreqAxis = frequencyAxis[(frequencyAxis> 400)]
        filteredMagAxis = frequencyMagnitude[np.where(frequencyAxis > 400)]
        
        zapOn = False
        maximum = 0
        index = 0
        for i in range(0,len(filteredMagAxis)):
            if filteredMagAxis[i] > maximum:
                maximum = filteredMagAxis[i]
                index = i
                
        if filteredFreqAxis[index] > 500 and filteredFreqAxis[index] < 600:
            print (filteredFreqAxis[index])
            zapOn = True

        print "Plotting on Matlab"	
	
        fig = plt.figure(1)
        ax1 = fig.add_subplot(211)
        ax1.plot(timeX,signal)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Signal amplitude');

        ax2 = fig.add_subplot(212)
        ax2.stem(filteredFreqAxis, filteredMagAxis)
        ax2.set_xlabel('Frequency in Hertz [Hz]')
        ax2.set_ylabel('Frequency Domain (Spectrum) Magnitude')
        plt.show()
                
##        if zapOn == True:
##            feedback()
            
        time.sleep(.05)
        GPIO.cleanup()
        print ('Done')
    
main()
