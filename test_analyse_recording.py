import sounddevice as sd
from scipy.io.wavfile import write
import base64
import io
import time
from tqdm import tqdm


def record_audio_base64(duration: int = 5, sample_rate: int = 44100) -> str:
    
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)

    
    for _ in tqdm(range(duration * 10)):
        time.sleep(0.1)
    sd.wait()
    print("Done.")

    
    buf = io.BytesIO()
    write(buf, sample_rate, audio)
    wav_bytes = buf.getvalue()

    return base64.b64encode(wav_bytes).decode("utf-8")


if __name__ == "__main__":
    aud_64 = record_audio_base64()
    print(f"Base64 length: {len(aud_64)} caractères")