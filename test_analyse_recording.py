import sounddevice as sd
from scipy.io.wavfile import write
import base64
import io
import time
from tqdm import tqdm

#Recording settings
duration = 5 #seconds
sample_rate = 44100

print("Recording...")
audio = sd.rec(int(duration*sample_rate, channels=1))

#Progress bar for the duration
for _ in tqdm[int](range(duration*10)): #update 10x per second
    time.sleep(0.1)
sd.wait()
print("Done.")

#Write WAV to an in-memory buffer
buf = io.ByteIO()
write(buf, sample_rate, audio)
wav_bytes = buf. getvalue()

aud_64 = base64.b64encode(wav_bytes).decode("utf-8")