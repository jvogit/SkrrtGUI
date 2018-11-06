#ffpyplayer for playing audio
from ffpyplayer.player import MediaPlayer
video_path="sample.mp4"
def PlayVideo(video_path):
    player = MediaPlayer(video_path)
    val = ''
    while val != 'eof':
        audio_frame, val = player.get_frame()
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
