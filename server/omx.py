# -*- coding: utf-8 -*-
#Mirrorcast Server Version 0.7.2b

from omxplayer.player import OMXPlayer
import mpv
import subprocess
import time
import os

NAMED_PIPE = "/tmp/input_stream.ts"

class Omx():
    def __init__(self):
        self.url = "None"
        self.player = None
        self.srt = None
        self.dvdplayer = None
        self.subs = 0
        self.audio_tracks = 0
        self.titles = 0
        return
        
    def youtube(self):
        proc = subprocess.Popen(['youtube-dl', '-g', '-f', 'mp4', self.url], stdout=subprocess.PIPE)
        url = proc.stdout.read()
        if url.decode("utf-8") == '':
            return False
        self.player = OMXPlayer(url.decode("utf-8", "strict")[:-1], args=['-o', 'hdmi'])
        return True

    def start_media(self, host, file):
        address = "http://" + str(host) + ":8090/" + file
        self.player = OMXPlayer(address.replace(" ", "%20"), args=['-o', 'hdmi'])
        i = 0
        while not self.player.is_playing():
            time.sleep(1)
            i+=1
            if i >= 40:
                break
            return False
        return True

    def start_dvd(self):
        self.dvdplayer = mpv.MPV()
        self.dvdplayer.fullscreen = True
        self.dvdplayer['vo'] = 'rpi'
        self.dvdplayer['rpi-osd'] = 'yes'
        self.dvdplayer['osd-bar'] = 'yes'
        self.dvdplayer['osd-on-seek'] = 'msg-bar'
        self.dvdplayer['osd-level'] = '1'
        self.dvdplayer['osd-duration'] = '8000'
        self.dvdplayer['loop-file'] = 'no'
        self.dvdplayer['end'] = '-5'
        self.dvdplayer['osd-playing-msg'] = 'Now Playing Your DVD'
        self.dvdplayer['dvd-device'] = '/dev/nbd0'
        self.dvdplayer.play('dvd://')
        self.audio_tracks = 0
        self.subs = 0
        self.titles = 0
        return True
        
    def get_tracks(self):
        #Get the amount of audio tracks and subtitles avaible on DVD(May cause issues when more than 1 movie on DVD)
        self.subs = 0
        self.audio_tracks = 0
        print(self.dvdplayer._get_property('disc-titles', 'length'))
        for item in self.dvdplayer._get_property("track-list"):
            if item['type'] == 'sub':
                self.subs += 1
            if item['type'] == 'audio':
                self.audio_tracks += 1
        return

    def close_srt(self):
        if self.srt and self.srt.poll() is None:
            self.srt.terminate()
            self.srt.wait()

    def pause(self):
        if self.player:
            time.sleep(1)
            self.player.pause()
        self.close_srt()

    def mirror(self):
        self.make_pipe()
        self.player = OMXPlayer(NAMED_PIPE, args=['-o', 'hdmi', '--lavfdopts', 'probesize:8000', '--timeout', '0', '--threshold', '0'])
        with open(NAMED_PIPE, "wb", 0) as output_stream:
            self.srt = subprocess.Popen(["stransmit", "srt://:8090?mode=server&pbkeylen=0", "file://con"], stdout=output_stream)
        return

    def make_pipe(self):
        if os.path.exists(NAMED_PIPE):
            os.remove(NAMED_PIPE)
        os.mkfifo(NAMED_PIPE)
