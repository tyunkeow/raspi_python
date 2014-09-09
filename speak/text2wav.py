import os
import sys
import base64
import time


DEFAULT_VOLUME = 50
DEFAULT_SPEED = 1
AUDIO_DIR = '~/data/audio/'
MPLAYER = '/opt/local/bin/mplayer'  # /usr/bin/mplayer
WORD_DB_DIR = AUDIO_DIR + 'word_db/'
words = ['eins', 'zwei', 'drei', 'vier', "fuenf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwoelf",
         'dreizehn', "zwanzig", "dreissig", "vierzig", "fuenfzig", "sechszig", "siebzig", "achtzig", "neunzig",
         "hundert", "tausend", "uhr", "hallo"]


# volume = 0.1 - 100
# speed = 0 - 100 (2 = verdoppelte geschw.)
def text2wav_google(text, filename):
    url = "http://translate.google.com/translate_tts?tl=de&q=" + text
    #os.system(MPLAYER + ' -ao pcm:file={} -speed {} -volume {} -noconsolecontrols "{}"'.format(filename, speed, volume, url))
    user_agent = '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.73.11 (KHTML, like Gecko) ' \
                 'Version/6.1.1 Safari/537.73.11"'
    os.system('wget --user-agent {} -O {} "{}"'.format(user_agent, filename, url))
    # TODO use Timestamp
    time.sleep(1.5)  # avoid getting blocked by google
    print "Soundfile written to " + filename


def text2wav_espeak(text, filename):
    os.system('espeak -vde -w {} "{}"'.format(filename, text))


def text2aiff_mac(text, filename):
    os.system('say -v Anna -o {} --file-format=AIFF "{}"'.format(filename, text))


def text2soundfile(text, filename, overwrite=False):
    filename = os.path.expanduser(filename)
    file_exists = os.path.exists(filename)
    if not overwrite and file_exists:
        print "Soundfile {} already exists and overwrite flag was not set. Skipping...".format(filename)
    else:
        text2aiff_mac(text, filename, overwrite)


def get_filename(text):
    return WORD_DB_DIR + base64.b64encode(text) + '.wav'


def digit2text(digit):
    digit_words = [ "null", "eins", "zwei", "drei", "vier", "fuenf", "sechs", "sieben", "acht", "neun", "zehn", "elf",
                    "zwoelf" ]
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
        for f in files:
            play_wav(f)
    else:
        filename = get_filename(text)
        if not os.path.exists(filename):
            filename = "/tmp/myspeak.wav"
        text2wav(text, filename, volume, speed)
        play_wav(filename)


def play_sound(filename):
    filename = os.path.expanduser(filename)
    print "Playing file ", filename
    #os.system('aplay -D sysdefault:CARD=Device {}'.format(filename))
    os.system('play {} pitch 1'.format(filename))


def build_word_db(overwrite=False):
    print "Building WAV database for basic words..."
    for word in words:
        filename = get_filename(word)
        text2wav(word, filename, overwrite)

if __name__ == "__main__":
    build_word_db()


