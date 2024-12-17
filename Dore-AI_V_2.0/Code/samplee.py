
# import os
# import sys
# import json
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
#     QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QTreeWidget, QTreeWidgetItem
# )
# from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
# from PyQt5.QtCore import Qt, QTimer
# import vlc
# import mutagen

# class MusicPlayer(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#         self.init_player()
#         self.init_timer()
#         self.load_saved_directories()
#         self.playlist = []
#         self.current_track_index = 0

#     def init_ui(self):
#         self.setWindowTitle("Music Pocket")
#         self.setGeometry(100, 100, 800, 650)
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #121212;
#             }
#             QLabel, QPushButton, QListWidget, QTreeWidget {
#                 color: white;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#             QPushButton {
#                 background-color: #1DB954;
#                 color: black;
#                 border: none;
#                 padding: 10px;
#                 border-radius: 20px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #1ED760;
#             }
#             QTreeWidget {
#                 background-color: #282828;
#                 border: none;
#                 color: white;
#             }
#             QTreeWidget::item {
#                 padding: 8px;
#                 border-bottom: 1px solid #333;
#             }
#             QTreeWidget::item:selected {
#                 background-color: #383838;
#             }
#         """)

#         # Main layout
#         central_widget = QWidget()
#         main_layout = QHBoxLayout()
#         central_widget.setLayout(main_layout)
#         self.setCentralWidget(central_widget)

#         # Left sidebar - Directory and Playlists
#         sidebar_layout = QVBoxLayout()
#         self.directory_tree = QTreeWidget()
#         self.directory_tree.setHeaderLabel("Music Directories")
#         self.directory_tree.itemDoubleClicked.connect(self.load_directory_tracks)
#         sidebar_layout.addWidget(self.directory_tree)

#         # Add directory button
#         add_dir_btn = QPushButton("Add Music Directory")
#         add_dir_btn.clicked.connect(self.add_music_directory)
#         sidebar_layout.addWidget(add_dir_btn)

#         # Right main content layout
#         content_layout = QVBoxLayout()

#         # Album art and track info
#         art_info_layout = QHBoxLayout()
        
#         # Album art
#         self.album_art = QLabel()
#         self.album_art.setFixedSize(300, 300)
#         self.album_art.setAlignment(Qt.AlignCenter)
#         default_pixmap = QPixmap(300, 300)
#         default_pixmap.fill(QColor('#333333'))
#         self.album_art.setPixmap(default_pixmap)
#         art_info_layout.addWidget(self.album_art)

#         # Track and playlist info
#         track_info_layout = QVBoxLayout()
#         self.track_label = QLabel("No Track Playing")
#         self.track_label.setStyleSheet("font-size: 18px; font-weight: bold;")
#         track_info_layout.addWidget(self.track_label)

#         # Playlist
#         self.playlist_widget = QListWidget()
#         self.playlist_widget.itemDoubleClicked.connect(self.play_selected_track)
#         track_info_layout.addWidget(self.playlist_widget)

#         art_info_layout.addLayout(track_info_layout)
#         content_layout.addLayout(art_info_layout)

#         # Progress slider
#         self.progress_slider = QSlider(Qt.Horizontal)
#         self.progress_slider.setStyleSheet("""
#             QSlider::groove:horizontal {
#                 background: #404040;
#                 height: 5px;
#             }
#             QSlider::handle:horizontal {
#                 background: #1DB954;
#                 width: 15px;
#                 height: 15px;
#                 border-radius: 7px;
#             }
#         """)
#         self.progress_slider.sliderMoved.connect(self.seek_track)
#         content_layout.addWidget(self.progress_slider)

#         # Time labels
#         time_layout = QHBoxLayout()
#         self.current_time_label = QLabel("0:00")
#         self.total_time_label = QLabel("0:00")
#         time_layout.addWidget(self.current_time_label)
#         time_layout.addStretch()
#         time_layout.addWidget(self.total_time_label)
#         content_layout.addLayout(time_layout)

#         # Control buttons
#         controls_layout = QHBoxLayout()
#         buttons = [
#             ("Previous", self.previous_track),
#             ("Play", self.play_track),
#             ("Pause", self.pause_track),
#             ("Next", self.next_track)
#         ]

#         for text, method in buttons:
#             btn = QPushButton(text)
#             btn.clicked.connect(method)
#             controls_layout.addWidget(btn)
#         content_layout.addLayout(controls_layout)

#         # Add layouts to main layout
#         main_layout.addLayout(sidebar_layout, 1)
#         main_layout.addLayout(content_layout, 3)

#     def init_player(self):
#         """Initialize VLC media player"""
#         self.instance = vlc.Instance('--aout=directsound')
#         self.player = self.instance.media_player_new()
        
#         # Event manager for track end
#         events = self.player.event_manager()
#         events.event_attach(vlc.EventType.MediaPlayerEndReached, self.track_ended)

#     def init_timer(self):
#         """Initialize timer for progress tracking"""
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_progress)
#         self.timer.start(1000)  # Update every second

#     def load_saved_directories(self):
#         """Load previously saved music directories"""
#         try:
#             with open('saved_directories.json', 'r') as f:
#                 directories = json.load(f)
#                 for directory in directories:
#                     self.add_directory_to_tree(directory)
#         except FileNotFoundError:
#             pass

#     def add_music_directory(self):
#         """Add a new music directory"""
#         directory = QFileDialog.getExistingDirectory(self, "Select Music Directory")
#         if directory:
#             # Save directory
#             try:
#                 with open('saved_directories.json', 'r') as f:
#                     directories = json.load(f)
#             except FileNotFoundError:
#                 directories = []

#             if directory not in directories:
#                 directories.append(directory)

#             with open('saved_directories.json', 'w') as f:
#                 json.dump(directories, f)

#             # Add to directory tree
#             self.add_directory_to_tree(directory)

#     def add_directory_to_tree(self, directory):
#         """Add directory to the directory tree"""
#         dir_item = QTreeWidgetItem(self.directory_tree, [os.path.basename(directory)])
#         dir_item.setData(0, Qt.UserRole, directory)

#     def load_directory_tracks(self, item):
#         """Load tracks from selected directory"""
#         directory = item.data(0, Qt.UserRole)
#         if directory:
#             self.playlist.clear()
#             self.playlist_widget.clear()

#             supported_formats = ['.mp3', '.wav', '.ogg', '.flac']
#             for filename in sorted(os.listdir(directory)):
#                 if os.path.splitext(filename)[1].lower() in supported_formats:
#                     full_path = os.path.join(directory, filename)
#                     self.playlist.append(full_path)
#                     self.playlist_widget.addItem(filename)

#     def extract_album_art(self, track_path):
#         """Extract album art from music file"""
#         try:
#             audio = mutagen.File(track_path, easy=True)
#             if audio and 'covr' in audio:
#                 # For MP4/M4A
#                 artwork = audio['covr'][0]
#                 pixmap = QPixmap()
#                 pixmap.loadFromData(artwork)
#                 return pixmap
#             elif audio and 'APIC:' in audio:
#                 # For MP3
#                 artwork = audio['APIC:'].data
#                 pixmap = QPixmap()
#                 pixmap.loadFromData(artwork)
#                 return pixmap
#         except Exception:
#             pass

#         # Default album art if no artwork found
#         default_pixmap = QPixmap(300, 300)
#         default_pixmap.fill(QColor('#333333'))
#         return default_pixmap

#     def play_selected_track(self, item):
#         """Play selected track"""
#         self.current_track_index = self.playlist_widget.row(item)
#         self.play_track()

#     def play_track(self):
#         """Play current track"""
#         if not self.playlist:
#             return

#         track = self.playlist[self.current_track_index]
#         media = self.instance.media_new(track)
#         self.player.set_media(media)
#         self.player.play()
        
#         # Update track label
#         self.track_label.setText(os.path.basename(track))
        
#         # Extract and set album art
#         album_art = self.extract_album_art(track)
#         scaled_art = album_art.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         self.album_art.setPixmap(scaled_art)
        
#         # Set total time
#         media_info = self.player.get_media()
#         duration = media_info.get_duration()
#         self.progress_slider.setRange(0, duration)
#         self.total_time_label.setText(self.format_time(duration))

#     def pause_track(self):
#         """Pause current track"""
#         self.player.pause()

#     def next_track(self):
#         """Play next track"""
#         if not self.playlist:
#             return
#         self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
#         self.play_track()

#     def previous_track(self):
#         """Play previous track"""
#         if not self.playlist:
#             return
#         self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
#         self.play_track()

#     def track_ended(self, event):
#         """Automatically play next track when current track ends"""
#         self.next_track()

#     def update_progress(self):
#         """Update progress slider and current time"""
#         if self.player.is_playing():
#             current_time = self.player.get_time()
#             self.progress_slider.setValue(current_time)
#             self.current_time_label.setText(self.format_time(current_time))

#     def seek_track(self, position):
#         """Seek to a specific position in the track"""
#         self.player.set_time(position)

#     def format_time(self, milliseconds):
#         """Convert milliseconds to minutes:seconds format"""
#         seconds = milliseconds // 1000
#         minutes, secs = divmod(seconds, 60)
#         return f"{minutes}:{secs:02d}"

# def main():
#     app = QApplication(sys.argv)
#     player = MusicPlayer()
#     player.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

import pyautogui
import time

def control_media(command):
    try:
        if "play" in command or "pause" in command:
            pyautogui.press('playpause')
            return "Media playback toggled."
        elif "next" in command:
            pyautogui.press('nexttrack')
            return "Next track."
        elif "previous" in command:
            pyautogui.press('prevtrack')
            return "Previous track."
        return "Command not recognized."
    except Exception as e:
        # log_error(f"control_media: {e}")
        return "An error occurred in media control."
    
if __name__ == '__main__':
    time.sleep(5)
    print(control_media('play')) 
    time.sleep(5)
    print(control_media('next'))
    time.sleep(5)
    print(control_media('pause'))
    time.sleep(5)
    print(control_media('previous'))
    time.sleep(5)  # Keep the window open for 5 seconds before closing