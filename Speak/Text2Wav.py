import os
import pygame.mixer
import base64
from pydub import AudioSegment

pygame.mixer.init(48000, -16, 1, 1024)

DEFAULT_VOLUME = 50
DEFAULT_SPEED = 1
AUDIO_DIR = '/home/pi/data/audio/'
WORD_DB_DIR = AUDIO_DIR + 'word_db/'
words = [ "eins", "zwei", "drei", "vier", "fuenf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwoelf", "dreizehn",
"zwanzig", "dreissig", "vierzig", "fuenfzig", "sechszig", "siebzig", "achtzig", "neunzig", "hundert", "tausend", 
"uhr", "hallo"]

# volume = 0.1 - 100
# speed = 0 - 100 (2 = verdoppelte geschw.)
def text2wav_google(text, filename, volume=DEFAULT_VOLUME, speed=DEFAULT_SPEED, overwrite=False):
    if overwrite or not os.path.exists(filename):
        url = "http://translate.google.com/translate_tts?tl=de&q=" + text
        #os.system('/usr/bin/mplayer -ao alsa -speed 1.5 -dumpaudio -dumpfile {} -noconsolecontrols "{}"'.format(filename, url))
        os.system('/usr/bin/mplayer -ao pcm:file={} -speed {} -volume {} -noconsolecontrols "{}"'.format(filename, speed, volume, url))
        print "Soundfile written to " + filename


def text2wav_espeak(text, filename): 
    os.system('espeak -vde -w {} "{}"'.format(filename, text))

def text2wav(text, filename, volume=DEFAULT_VOLUME, speed=DEFAULT_SPEED):
    text2wav_google(text, filename, volume, speed)

def get_filename(text):
    return WORD_DB_DIR + base64.b64encode(text) + '.wav'

def digit2text(digit):
    digit_words = [ "null", "eins", "zwei", "drei", "vier", "fuenf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwoelf" ]
    return digit_words[digit]

def num2text(integer):
    s = []
    for digit in str(integer):
        s.append(digit2text(int(digit)))
    return s

def speak(text, volume=DEFAULT_VOLUME, speed=DEFAULT_SPEED):
    if isinstance(text, (int, long)):
        parts = num2text(int(text))
	files = [get_filename(w) for w in parts]
        print "files: " + str(files)
	#wavs = [AudioSegment.from_wav(f) for f in files]
        #for w in wavs:
        #    w.
        for f in files:
            playWav(f)
    else:
        filename = get_filename(text)
        if not os.path.exists(filename):
            filename = "/tmp/myspeak.wav"
        text2wav(text, filename, volume, speed)
        playWav(filename)

def playWav(filename):
    if True:
        sound = pygame.mixer.Sound(filename)
        channelA = pygame.mixer.Channel(1)
        channelA.play(sound)
    else:
        os.system('aplay -D sysdefault:CARD=Device {}'.format(filename))

def build_word_db(volume, speed):
    for word in words:
        filename = get_filename(word)
        text2wav(word, filename, volume, speed)

if __name__ == "__main__":
    build_word_db(30, 1)
    speak(15)
