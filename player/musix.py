
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl


class Music:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        # self.player.setLoops(1) # -1=infinite
        # self.audio_output.setVolume(0)
        ## PLAY EMPTY SOUND WORKAROUND ##
        # at least one music file needed to be played from start to finish
        # before be able to switch tracks without crashing
        self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))
        self.player.play()