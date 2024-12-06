import os
import time
import random
import pygame
from typing import List
import json
import threading

FILES_DIR = "../Files"
SETTINGS_FILE = 'settings.json'
MUSIC_DIR = ''

with open(os.path.join(FILES_DIR,SETTINGS_FILE), 'r') as f:
    settings = json.load(f)
    MUSIC_DIR = settings['music_dir']
    f.close()
print(MUSIC_DIR)
FILES = [os.path.join(MUSIC_DIR,f) for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3','.ogg','.wav'))]

class MusicPlayer:
    def __init__(self):
        self.playlist = FILES # List of music file paths
        self.current_track_index = 0
        self.is_playing = False
        self.thread = None
        self.directory = MUSIC_DIR
        pygame.mixer.init()

    def play(self, shuffle: bool = False):
        """Play the music playlist."""
        if not self.playlist:
            print("Playlist : inside play",self.playlist)
            print("No music files found in the directory.")
            return

        if shuffle:
            random.shuffle(self.playlist)

        self.is_playing = True
        try:
            while self.is_playing:
                current_track = self.playlist[self.current_track_index]
                print(f"Playing: {os.path.basename(current_track)}")
                
                pygame.mixer.music.load(current_track)
                pygame.mixer.music.play()

                # Wait for the track to finish
                while pygame.mixer.music.get_busy() and self.is_playing:
                    time.sleep(1)

                # Move to next track
                self.current_track_index = (self.current_track_index + 1) % len(self.playlist)

        except KeyboardInterrupt:
            print("\nPlayback stopped.")
        finally:
            pygame.mixer.quit()

    def stop(self):
        """Stop the music playback."""
        self.is_playing = False
        pygame.mixer.music.stop()
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def play_in_thread(self, shuffle: bool = False):
        """Start music playback in a separate thread."""
        if self.is_playing:
            print("Music is already playing.")
            return

        self.thread = threading.Thread(target=self.play, args=(shuffle,), daemon=True)
        self.thread.start()
        print("Music playback started in a separate thread.")
# Example usage
def main():
    # Replace with your actual music directory path
    music_dir = "/run/media/spidey/0F56533E3399A505/Music"
    player = MusicPlayer()
    player.play_in_thread()
    
if __name__ == "__main__":
    main()
    while True:
        pass
