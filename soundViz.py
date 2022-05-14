from IPython.display import clear_output
from matplotlib import pyplot as plt
import numpy as np
import pyaudio
import time

from scipy import fft
import warnings
warnings.filterwarnings("ignore")
plt.style.use("dark_background")
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'


def soundplot(datap,figsize=(16,8)):
    data=datap[:]
    clear_output(wait=True)
    fig=plt.figure(" ",figsize=figsize)
    ax1=plt.subplot(3,2,1)
    plt.ylim(-5000,5000)
    plt.plot(data)
    plt.xticks([])
    plt.yticks([])
    for pos in ['top', 'bottom', 'right', 'left']:
        ax1.spines[pos].set_edgecolor('black')
    ax2=plt.subplot(3,2,2)
    for pos in ['top', 'bottom', 'right', 'left']:
        ax2.spines[pos].set_edgecolor('black')
    fftPower = abs(fft.fft(data))
    y = fftPower[:int(len(fftPower)/4)]

    plt.plot(y)
    plt.ylim(1024*15,1024*1000)
    plt.xlim(1024,1024*5)    
    plt.xticks([])
    plt.yticks([])
    
    ax3=plt.subplot(3,1,2)
    for pos in ['top', 'bottom', 'right', 'left']:
        ax3.spines[pos].set_edgecolor('black')
    spec,freq,t,_=plt.specgram(data,NFFT=1024,Fs=CHUNK*4,cmap='hot')
    plt.xticks([])
    plt.yticks([])
    plt.ylim(700,1024*10)
    plt.tight_layout()

    ax4=plt.subplot(3,1,3)
    for pos in ['top', 'bottom', 'right', 'left']:
        ax4.spines[pos].set_edgecolor('black')
    ts=spec.shape[1]
    al=np.arange(0,1,1/ts)
    spec[spec>1024*10]=1024*10
    for i in range(ts):
        plt.plot(-spec[:,i]+i*100,alpha=al[i],c='gray')
    plt.ylim(-1024*10,1024*4)
    plt.xticks([])
    plt.yticks([])
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.pause(.01)
    plt.close()


p=pyaudio.PyAudio()
RATE = int(44100/2)
CHUNK = 1024*3
length=5
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)

totalData=[]


while True: 
    try:
        data=list(np.fromstring(stream.read(CHUNK,exception_on_overflow = False),dtype=np.int16))
        totalData+=data
        soundplot(totalData[-CHUNK*length:])
        totalData=totalData[-CHUNK*length:]
    except:
        try:
            stream.stop_stream()
        except:
            pass
        try:
            stream.close()
        except:
            pass
        p.terminate()
        break