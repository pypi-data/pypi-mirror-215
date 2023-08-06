import RPi.GPIO as GPIO
import time
#import sys
import numpy as np

GPIO.setmode(GPIO.BOARD)

# Raspberry Pi Pin-Belegung fur TB6600 Treiber
DIR = 33
PUL = 35
ENA = 37

DIR_Left = GPIO.HIGH
DIR_Right = GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

def rotate(degree,slope=0.5,rpm_max=200): #degree: rotation of plate in degree, slope: how fast motor starts [0,1] 0=slow, 1=fast, max_rpm: max rpm of motor
    if degree==0:
        exit()
    if degree<0:
        GPIO.output(DIR, DIR_Left)
    if degree>0:
        GPIO.output(DIR, DIR_Right)
        
    if rpm_max > 1000:
        rpm_max = 1000
    if rpm_max < 100:
        rpm_max = 100
    if slope > 1:
        slope = 1
    if slope < 0:
        slope = 0
        
    # Motor aktivieren und halten
    GPIO.output(ENA, ENA_Locked)

    #1 motor turn equals 400 steps. With i = 1:15, 1 table turn is 15*400 = 6000 steps
    steps=int(abs(degree)*6000/360)
    RPM_of_step = np.zeros(steps)
    slope = 0.8*slope + 0.2 #min slope is 0.2, max slope is 1.0
    rpm_min = 100 #might adapt in future
    steps_until_max_rpm = int((rpm_max-rpm_min)/slope)
    
    if steps<=2*steps_until_max_rpm:
        #slope up and down
        for i in range(0,int(steps/2)):
            RPM_of_step[i]=rpm_min+i*slope
            RPM_of_step[steps-i-1]=rpm_min+i*slope
    else:
        
        #slope up, stay up and then and down
        for i in range(0,steps_until_max_rpm):
            RPM_of_step[i]=rpm_min+i*slope
            RPM_of_step[steps-i-1]=rpm_min+i*slope
        for i in range(steps_until_max_rpm,(steps-steps_until_max_rpm)):
            RPM_of_step[i]=rpm_max
    
    for i in range(0,len(RPM_of_step)):
        currentfrequency=0.3/(RPM_of_step[i])
        # Puls modulieren
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(currentfrequency/2)#(0.0001875)

        GPIO.output(PUL, GPIO.LOW)
        time.sleep(currentfrequency/2)

    # Motor freigeben
    GPIO.output(ENA, ENA_Released)