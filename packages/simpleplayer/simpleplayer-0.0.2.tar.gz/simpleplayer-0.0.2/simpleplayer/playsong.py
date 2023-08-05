import subprocess
import sys

class PlaySong:
    # Kelas ini akan memutar lagu
    def __init__(self, song):
        self.song = song
        self.player = None

    def play(self):
        if self.player is None or self.player.poll() is not None:
            command = [sys.executable, "-m", "simpleplayer.longplayer", self.song]
            self.player = subprocess.Popen(command)

    def stop(self):
        if self.player is not None and self.player.poll() is None:
            self.player.terminate()
            self.player.wait()