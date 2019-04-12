try:
    from scs.siricontrol import Control
    from scs.audioplayer import AudioPlayer
except:
    from siricontrol import Control
    from audioplayer import AudioPlayer
from gtts import gTTS
from pathlib import Path
import threading
import json
import hashlib
import os

class KartSiriControlModule():
    def __init__(self, kartapp):
        self.load_config()
        self.app = kartapp
        self.audioplayer = AudioPlayer()
        
    def load_config(self):
        default_config = json.dumps({"email": "", "password": ""},
                            indent=4, sort_keys=True)
        try:
            config = open(os.path.join(os.path.dirname(__file__), "config.txt"), "r")
        except OSError:
            config = open(os.path.join(os.path.dirname(__file__), "config.txt"), "w+")
            config.write(default_config)
        config.seek(0)
        self.loaded = json.loads(config.read())
        config.close()
        
    @staticmethod
    def tts(audioplayer, tosay):
        encoded = hashlib.sha224(tosay.encode()).hexdigest()
        root_path = os.path.join(os.path.dirname(__file__), "tts")
        dire = Path(root_path)
        file = Path(root_path + "/tts/"+encoded + ".mp3")
        if not dire.exists():
            dire.mkdir()
        if not file.is_file():
            gTTS(tosay, lang='en').save(root_path + "/tts/"+encoded + ".mp3")
        audioplayer.inde_play(root_path+"/tts/"+encoded+".mp3")
        
class SiriListenThread(threading.Thread):
    exit_flag = False
    
    def __init__(self, kartmodule):
        super().__init__()
        self.kartmodule = kartmodule
        
    def run(self):
        config = self.kartmodule.loaded
        self.control = Control(config["email"], config["password"], self.kartmodule)
        if self.exit_flag:
            return
        self.control.start()

    def stop(self):
        self.exit_flag = True
        self.control.exit_flag = True
