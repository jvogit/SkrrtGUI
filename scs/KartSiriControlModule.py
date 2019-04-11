from siricontrol import Control
from gtts import gTTS
from audioplayer import AudioPlayer
import threading
import json

class KartSiriControlModule():
    def __init__(self, kartapp):
        self.load_config()
        self.app = kartapp
        self.audioplayer = AudioPlayer()
        
    def load_config(self):
        default_config = json.dumps({"email": "", "password": ""},
                            indent=4, sort_keys=True)
        try:
            config = open("config.txt", "r")
        except OSError:
            config = open("config.txt", "w+")
            config.write(default_config)
        config.seek(0)
        self.loaded = json.loads(config.read())
        config.close()
        
    @staticmethod
    def tts(audioplayer, tosay):
        encoded = hashlib.sha224(tosay.encode()).hexdigest()
        dire = Path("tts")
        file = Path("tts/"+encoded + ".mp3")
        if not dire.exists():
            dire.mkdir()
        if not file.is_file():
            gTTS(tosay, lang='en').save("tts/"+encoded + ".mp3")
        audioplayer.inde_play("tts/"+encoded+".mp3")
        
class SiriListenThread(threading.Thread):
    def __init__(self, kartmodule):
        super().__init__()
        self.kartmodule = kartmodule
        
    def run(self):
        config = self.kartmodule.loaded
        self.control = Control(config["email"], config["password"], self.kartmodule)
        self.control.start()

    def stop(self):
        self.control.exit_flag = True
