import heartpy as hp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import serial
import tkinter as tk
import time

SAMPLING_RATE = 1000
SAMPLING_FREQ = 50
SEGMENT_WIDTH = 3

try:
    arduino = serial.Serial('COM4', 9600)
except:
    pass
sampling_rate = 1000

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

y = []
x = []
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

data, measures = hp.process_segmentwise(df, sample_rate=SAMPLING_RATE, segment_width=SEGMENT_WIDTH)
print(measures['segment_indices'])

def update(i):
    for j in range(SAMPLING_FREQ):
        yi = df[i * SAMPLING_FREQ + j]
        y.append(yi)
        x.append(i * SAMPLING_FREQ + j)
        if (i * SAMPLING_FREQ > 1000):
            y.pop(0)
            x.pop(0)
        if (i * SAMPLING_FREQ + j) % (1000 * SEGMENT_WIDTH) == 0:
            bpm_s = measures['bpm'][int((i * SAMPLING_FREQ + j) / 1000)]
            arduino.write(str.encode(str(bpm_s)))
            
        
    ax.clear()
    ax.plot(x, y)
    temp_bpm = measures['bpm'][int((i * SAMPLING_FREQ + j) / 1000)]
    ax.set_xlabel(f'bpm\nbpm: {temp_bpm}')
    # print (i, ': ', yi)

a = FuncAnimation(fig, update, interval=SAMPLING_FREQ, frames=int(len(df) / SAMPLING_FREQ), repeat=False)
plt.show()


# for bpm in measures['bpm']:
#     bpm_s = round(bpm)
#     # arduino.write(str.encode(str(bpm_s)))
#     print(bpm)