#*****************************************************FasterWhisper*****************************************************
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import torch
from collections import deque
import threading
import queue
import signal
import logging


class WhisperTranscriber:
    def __init__(self, model_size="medium", device=None, compute_type="float16"):
        # Set up logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Automatically detect the best available device
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Audio settings
        self.SAMPLE_RATE = 16000
        self.BLOCK_SIZE = 8000
        self.CHANNELS = 1

        # Initialize the model
        self.model = WhisperModel(
            model_size,
            device=self.device,
            compute_type=compute_type
        )

        # Buffer for storing audio data
        self.audio_buffer = deque(maxlen=100)
        self.processing_queue = queue.Queue()
        self.is_running = False
        self.transcriptions = []  # List to store transcription segments

        # Add debug counter
        self.processed_chunks = 0

    def audio_callback(self, indata, frames, time, status):
        if status:
            self.logger.error(f"Audio stream error: {status}")
            return

        # Check for silent input
        audio_chunk = indata[:, 0].astype(np.float32)
        if np.max(np.abs(audio_chunk)) < 0.01:  # Adjust threshold as needed
            self.logger.debug("Low audio input detected")
            return

        self.audio_buffer.append(audio_chunk)

        if len(self.audio_buffer) >= 3:
            audio_data = np.concatenate(list(self.audio_buffer))
            self.processing_queue.put(audio_data)
            self.audio_buffer.clear()
            self.logger.debug(f"Added chunk to processing queue. Queue size: {self.processing_queue.qsize()}")

    def process_audio(self):
        while self.is_running:
            try:
                audio_data = self.processing_queue.get(timeout=1.0)
                self.processed_chunks += 1

                # Log audio characteristics
                self.logger.debug(f"Processing chunk {self.processed_chunks}")
                self.logger.debug(f"Audio range: {np.min(audio_data):.4f} to {np.max(audio_data):.4f}")

                # Normalize audio
                audio_data = self.normalize_audio(audio_data)

                # Ignore chunks with very low amplitude (likely noise)
                if np.max(np.abs(audio_data)) < 0.05:
                    self.logger.debug("Ignoring low amplitude chunk (likely noise)")
                    continue

                # Transcribe with English language specified
                segments, info = self.model.transcribe(
                    audio_data,
                    beam_size=5,
                    word_timestamps=True,
                    vad_filter=True,
                    vad_parameters=dict(
                        min_silence_duration_ms=1000,
                        speech_pad_ms=200
                    )
                    ,
                    language="en",  # Force transcription to English
                    task="transcribe"  # Strict transcription, no guessing
                )

                # Process and store results
                for segment in segments:
                    self.transcriptions.append(segment.text)

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Processing error: {e}", exc_info=True)

    def normalize_audio(self, audio_data):
        # Remove DC offset
        audio_data = audio_data - np.mean(audio_data)

        # Normalize amplitude
        max_amplitude = np.max(np.abs(audio_data))
        if max_amplitude > 0:
            audio_data = audio_data / max_amplitude

        self.logger.debug(f"Normalized audio range: {np.min(audio_data):.4f} to {np.max(audio_data):.4f}")
        return audio_data

    def start(self):
        self.is_running = True
        self.logger.info("Starting transcription service...")

        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.stop_signal_handler)

        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_audio)
        self.processing_thread.start()

        # Start audio stream
        try:
            with sd.InputStream(
                    callback=self.audio_callback,
                    channels=self.CHANNELS,
                    samplerate=self.SAMPLE_RATE,
                    blocksize=self.BLOCK_SIZE
            ):
                self.logger.info(f"Listening... (Using {self.device} device)")
                self.logger.info("Press Ctrl+C to stop")
                while self.is_running:
                    threading.Event().wait(0.1)
        except Exception as e:
            self.logger.error(f"Error in audio stream: {e}", exc_info=True)
        finally:
            self.stop()

    def stop_signal_handler(self, signum, frame):
        self.logger.info("Keyboard interrupt detected. Stopping...")
        self.stop()

    def stop(self):
        self.is_running = False
        if hasattr(self, 'processing_thread'):
            self.processing_thread.join()
        full_transcription = " ".join(self.transcriptions)  # Combine all segments into a single string
        self.logger.info(f"\nTranscription stopped. Processed {self.processed_chunks} chunks.")
        self.logger.info(f"Final transcription: {full_transcription}")
        print(full_transcription)
        return full_transcription


if __name__ == "__main__":
    transcriber = WhisperTranscriber(model_size="medium")
    transcriber.start()




#***************************************VOSK*******************************************************
#
# import vosk
# import pyaudio
# import json
#
# # Initialize Vosk model (Ensure the correct path to the model)
# model = vosk.Model(r"../models/vosk-model-en-in-0.5")  # Update the path to your model
# recognizer = vosk.KaldiRecognizer(model, 16000)
#
# # Function to listen and transcribe in real-time
# def listen_for_command():
#     p = pyaudio.PyAudio()
#
#     # Open the microphone stream
#     stream = p.open(format=pyaudio.paInt16,
#                     channels=1,
#                     rate=16000,
#                     input=True,
#                     frames_per_buffer=8000)
#
#     print("Listening for command...")
#
#     # Start the stream and continuously listen for audio input
#     while True:
#         data = stream.read(4000, exception_on_overflow=False)  # Read chunks of audio data
#         if recognizer.AcceptWaveform(data):  # Check if the recognizer has a valid result
#             result = recognizer.Result()  # Get the result in JSON format
#             text = json.loads(result)["text"]  # Extract the transcribed text
#             print(f"Command received: {text}")
#
#             # If a specific stop command is detected, break the loop
#             if "stop" in text.lower():
#                 print("Stop command detected. Exiting...")
#                 break
#
#         else:
#             # For partial results (while audio is being processed)
#             partial_result = recognizer.PartialResult()  # Get partial transcription result
#             partial_text = json.loads(partial_result)["partial"]
#             print(f"Partial transcription: {partial_text}", end="\r")  # Overwrite line for real-time feedback
#
#     # Close the audio stream after exiting
#     stream.stop_stream()
#     stream.close()
#
# # Main entry point
# if __name__ == "__main__":
#     listen_for_command()
#
# #***************************************************VOSK-upgrade
# import vosk
# import pyaudio
# import json
# import threading
# import numpy as np
# import wave
# import logging
# import os
# from datetime import datetime
# from typing import Optional, Dict, List
# import webrtcvad
# from queue import Queue
# import queue
# import time
#
#
# class AudioProcessor:
#     def __init__(self, model_path: str, sample_rate: int = 16000):
#         # Set up logging
#         self._setup_logging()
#
#         # Audio parameters
#         self.sample_rate = sample_rate
#         self.chunk_size = 480  # Optimal for WebRTC VAD
#         self.channels = 1
#
#         # Initialize components
#         self._init_audio_components(model_path)
#         self._init_processing_tools()
#
#         # Processing flags and state
#         self.is_running = False
#         self.pause_processing = False
#
#         # Audio statistics
#         self.audio_stats = {
#             "peak_level": 0.0,
#             "noise_floor": float('inf'),
#             "clipping_count": 0
#         }
#
#     def _setup_logging(self):
#         """Configure logging system"""
#         log_dir = "logs"
#         os.makedirs(log_dir, exist_ok=True)
#
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s',
#             handlers=[
#                 logging.FileHandler(f"{log_dir}/transcriber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
#                 logging.StreamHandler()
#             ]
#         )
#         self.logger = logging.getLogger(__name__)
#
#     def _init_audio_components(self, model_path: str):
#         """Initialize Vosk and audio components"""
#         try:
#             self.model = vosk.Model(model_path)
#             self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
#             self.vad = webrtcvad.Vad(3)  # Aggressive VAD mode
#             self.audio_queue = Queue()
#             self.result_queue = Queue()
#
#             # Initialize PyAudio with error checking
#             self.audio = pyaudio.PyAudio()
#             self._check_audio_devices()
#
#         except Exception as e:
#             self.logger.error(f"Failed to initialize audio components: {e}")
#             raise
#
#     def _init_processing_tools(self):
#         """Initialize audio processing tools and buffers"""
#         self.audio_buffer = []
#         self.silence_threshold = 0.01
#         self.gain_factor = 1.0
#         self.noise_reduction_strength = 0.1
#
#     def _check_audio_devices(self) -> int:
#         """Check available audio devices and select the best one"""
#         best_device_index = None
#         best_channels = 0
#
#         for i in range(self.audio.get_device_count()):
#             try:
#                 device_info = self.audio.get_device_info_by_index(i)
#                 if device_info['maxInputChannels'] > best_channels:
#                     best_channels = device_info['maxInputChannels']
#                     best_device_index = i
#             except Exception as e:
#                 self.logger.warning(f"Error checking device {i}: {e}")
#
#         if best_device_index is None:
#             raise RuntimeError("No suitable audio input device found")
#
#         return best_device_index
#
#     def _process_audio_chunk(self, audio_data: bytes) -> np.ndarray:
#         """Process audio chunk with noise reduction and gain control"""
#         # Convert bytes to numpy array
#         audio_array = np.frombuffer(audio_data, dtype=np.int16)
#
#         # Calculate audio statistics
#         self._update_audio_stats(audio_array)
#
#         # Apply noise reduction
#         audio_array = self._reduce_noise(audio_array)
#
#         # Apply automatic gain control
#         audio_array = self._apply_gain_control(audio_array)
#
#         return audio_array
#
#     def _reduce_noise(self, audio_array: np.ndarray) -> np.ndarray:
#         """Apply simple noise reduction"""
#         # Spectral subtraction-based noise reduction
#         noise_floor = self.audio_stats["noise_floor"]
#         return np.where(
#             np.abs(audio_array) < noise_floor,
#             audio_array * self.noise_reduction_strength,
#             audio_array
#         )
#
#     def _apply_gain_control(self, audio_array: np.ndarray) -> np.ndarray:
#         """Apply automatic gain control"""
#         current_peak = np.max(np.abs(audio_array))
#         if current_peak > 0:
#             target_peak = 0.7 * 32767  # Target 70% of max value for 16-bit audio
#             self.gain_factor = min(target_peak / current_peak, 2.0)  # Limit maximum gain
#             audio_array = audio_array * self.gain_factor
#
#         return audio_array.astype(np.int16)
#
#     def _update_audio_stats(self, audio_array: np.ndarray):
#         """Update audio statistics for monitoring"""
#         current_peak = np.max(np.abs(audio_array))
#         self.audio_stats["peak_level"] = max(current_peak, self.audio_stats["peak_level"] * 0.95)
#         self.audio_stats["noise_floor"] = min(current_peak, self.audio_stats["noise_floor"] * 1.1)
#         self.audio_stats["clipping_count"] += np.sum(np.abs(audio_array) > 32700)
#
#     def _audio_callback(self, in_data, frame_count, time_info, status):
#         """Handle incoming audio data"""
#         if status:
#             self.logger.warning(f"Audio callback status: {status}")
#
#         try:
#             self.audio_queue.put(in_data)
#             return (None, pyaudio.paContinue)
#         except Exception as e:
#             self.logger.error(f"Audio callback error: {e}")
#             return (None, pyaudio.paAbort)
#
#     def _process_audio_thread(self):
#         """Process audio data in a separate thread"""
#         while self.is_running:
#             try:
#                 if self.pause_processing:
#                     time.sleep(0.1)
#                     continue
#
#                 audio_data = self.audio_queue.get(timeout=1.0)
#                 processed_audio = self._process_audio_chunk(audio_data)
#
#                 # Check for voice activity
#                 if self.vad.is_speech(audio_data, self.sample_rate):
#                     if self.recognizer.AcceptWaveform(processed_audio.tobytes()):
#                         result = json.loads(self.recognizer.Result())
#                         if result["text"]:
#                             self.result_queue.put(result)
#
#             except Queue.Empty:
#                 continue
#             except Exception as e:
#                 self.logger.error(f"Audio processing error: {e}")
#                 time.sleep(0.1)
#
#     def start(self):
#         """Start the audio processing system"""
#         self.is_running = True
#
#         # Start processing thread
#         self.processing_thread = threading.Thread(target=self._process_audio_thread)
#         self.processing_thread.start()
#
#         try:
#             device_index = self._check_audio_devices()
#             self.stream = self.audio.open(
#                 format=pyaudio.paInt16,
#                 channels=self.channels,
#                 rate=self.sample_rate,
#                 input=True,
#                 input_device_index=device_index,
#                 frames_per_buffer=self.chunk_size,
#                 stream_callback=self._audio_callback
#             )
#
#             self.logger.info("Audio processing started successfully")
#
#         except Exception as e:
#             self.logger.error(f"Failed to start audio stream: {e}")
#             self.stop()
#             raise
#
#     def stop(self):
#         """Stop the audio processing system"""
#         self.is_running = False
#
#         if hasattr(self, 'processing_thread'):
#             self.processing_thread.join()
#
#         if hasattr(self, 'stream'):
#             self.stream.stop_stream()
#             self.stream.close()
#
#         self.audio.terminate()
#         self.logger.info("Audio processing stopped")
#
#     def get_next_result(self, timeout: float = None) -> Optional[Dict]:
#         """Get the next transcription result"""
#         try:
#             return self.result_queue.get(timeout=timeout)
#         except queue.Empty:
#             return None
#
#
# def main():
#     # Update the model path to the correct location
#     processor = AudioProcessor(model_path=r"/run/media/drackko/022df0a1-27b0-4c14-ad57-636776986ded/drackko/PycharmProjects/Dore-AI/models/vosk-model-en-in-0.5")
#
#     try:
#         processor.start()
#         print("Listening... Press Ctrl+C to stop")
#
#         while True:
#             # Attempt to fetch the next transcription result
#             result = processor.get_next_result(timeout=0.1)
#             if result:
#                 # Print the transcribed text to the console
#                 print(f"Transcription: {result['text']}")
#
#                 # Optionally stop if specific keywords are detected
#                 if "stop" in result['text'].lower():
#                     print("Detected 'stop' in transcription. Exiting...")
#                     break
#
#     except KeyboardInterrupt:
#         print("\nStopping...")
#     finally:
#         processor.stop()
#
#
#
# if __name__ == "__main__":
#     main()