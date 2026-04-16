import pygame
import os

class MusicPlayer:
    def __init__(self):
        """
        Initializes the music player by locating the music directory 
         and loading available audio files into a playlist.
        """
        # 1. Get the directory path of the current script
        current_dir = os.path.dirname(__file__)
        
        # 2. Define the path to the 'music' subfolder
        self.music_dir = os.path.join(current_dir, "music")
        
        # 3. Verify directory existence and filter for supported audio formats
        if os.path.exists(self.music_dir):
            self.playlist = [f for f in os.listdir(self.music_dir) if f.endswith(('.mp3', '.wav'))]
        else:
            self.playlist = []
            print(f"Error: Music folder not found at {self.music_dir}")
            
        self.current_index = 0

    def play(self):
        """Loads and plays the track at the current playlist index."""
        if self.playlist:
            track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()

    def stop(self):
        """Stops the current playback."""
        pygame.mixer.music.stop()

    def next(self):
        """Advances to the next track in the playlist with automatic wrap-around."""
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def previous(self):
        """Moves to the previous track in the playlist with automatic wrap-around."""
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def get_current_track(self):
        """Returns the filename of the current track or a status message."""
        if self.playlist:
            return self.playlist[self.current_index]
        return "No tracks found"

    def is_playing(self):
        """Checks if the mixer is currently busy playing audio."""
        return pygame.mixer.music.get_busy()