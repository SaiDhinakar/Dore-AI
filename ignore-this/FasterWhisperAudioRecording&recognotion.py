import pyaudio
from faster_whisper import WhisperModel
import wave
import os

# NEON_GREEN = "\033[92m"
# RESET_COLOR = "\033[0m"


def record_chunk(p, stream, file_path, chunk_length):
    print("Recording...")
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()


def transcribe_chunk(model, chunk):
    chunk, _ = model.transcribe(chunk,beam_size= 5, vad_filter=True)
    return chunk


def main2():
    model_size = "medium.en"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    accumulated_transcription = ""

    # Initialize an empty string to accumulate transcriptions
    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file, 5)
            transcription = transcribe_chunk(model, chunk_file)
            for transcript in transcription:
                accumulated_transcription += transcript.text
            os.remove(chunk_file)

    except KeyboardInterrupt:
        print("stopping")
        with open("log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)
    finally:
        print("Log: " + accumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    main2()
