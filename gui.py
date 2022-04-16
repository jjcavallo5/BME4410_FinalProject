import heartpy as hp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import serial
import tkinter as tk
import time

try:
    arduino = serial.Serial('COM4', 9600)
except:
    pass
sampling_rate = 1000
index = 0

def get_file():
    filename = 'ECGSignal_Text.txt'

    with open(filename) as f:
        lines = f.readlines()
        temp_data = lines[13:]

    df = pd.DataFrame(
            [x.split('\t') for x in temp_data],
            columns=['CH1', 'CH2', 'CH40', 'tobedropped']
            )

    df = df.drop(['tobedropped'], axis=1)
    df['CH1'] = df['CH1'].astype('float')
    df['CH40'] = df['CH40'].astype('float')

    return df['CH1'].to_numpy()

df = get_file()
print(df.shape)
data, measures = hp.process_segmentwise(df, sample_rate=1000, segment_width=3)
#hp.plotter(data, measures)
print(measures['bpm'])
for bpm in measures['bpm']:
    bpm_s = round(bpm)
    # if bpm > 100:
    arduino.write(str.encode(str(bpm_s)))
    # else:
    #     arduino.write(str.encode('0'))
    print(bpm)
    time.sleep(1)
    
# fig = plt.figure()
# ax = plt.subplot(111)
# plt.plot(df[0:10000])
# plt.show()