#!/usr/bin/python
# Insulter.py

import json
import random
from Text2Wav import text2wav, play_wav


ins_data = {
    "adjektive": [
        {
            'm': "schoener",
            "f": "schoene",
            "n": "schoenes"
        },
        {
            "m": "buckliger",
            "f": "bucklige",
            "n": "buckliges"
        },
        {
            "m": "besoffener",
            "f": "besoffene",
            "n": "besoffenes"
        },
        {
            "m": "fieser",
            "f": "fiese",
            "n": "fieses"
        },
        {
            "m": "tollpatschiger",
            "f": "tollpatschige",
            "n": "tollpatschiges"
        },
        {
            "m": "grosser",
            "f": "grosse",
            "n": "grosses"
        },
        {
            "m": "unverschaemter",
            "f": "unverschaemte",
            "n": "unverschaemtes"
        },
        {
            "m": "vorlauter",
            "f": "vorlaute",
            "n": "vorlautes"
        },
        {
            "m": "brutaler",
            "f": "brutale",
            "n": "brutales"
        },
        {
            "m": "schlechter",
            "f": "schlechte",
            "n": "schlechters"
        },
        {
            "m": "gewissenloser",
            "f": "gewissenlose",
            "n": "gewissenloses"
        },
        {
            "m": "ruecksichtsloser",
            "f": "ruecksichtslose",
            "n": "ruecksichtsloses"
        },
        {
            "m": "bemitleidenswerter",
            "f": "bemitleidenswerte",
            "n": "bemitleidenswertes"
        },
        {
            "m": "haariger",
            "f": "haarige",
            "n": "haariges"
        },
        {
            "m": "verstrahlter",
            "f": "verstrahlte",
            "n": "verstrahltes"
        },
        {
            "m": "kleiner",
            "f": "kleine",
            "n": "kleines"
        }
    ],
    "steigerungen": ["leicht", "sehr", "massiv", "extrem", "besonders", "voll", "super"],
    "substantive": [
        {
            "geschlecht": "m",
            "wert": "Affe"
        },
        {
            "geschlecht": "n",
            "wert": "Stinktier"
        },
        {
            "geschlecht": "m",
            "wert": "Hosch"
        },
        {
            "geschlecht": "m",
            "wert": "Heckenpenner"
        },
        {
            "geschlecht": "m",
            "wert": "Asi"
        },
        {
            "geschlecht": "m",
            "wert": "Luegenbaron"
        },
        {
            "geschlecht": "m",
            "wert": "Doedel"
        },
        {
            "geschlecht": "m",
            "wert": "Erbsenzaehler"
        },
        {
            "geschlecht": "m",
            "wert": "Ruepel"
        },
        {
            "geschlecht": "n",
            "wert": "Schwein"
        },
        {
            "geschlecht": "n",
            "wert": "Ferkel"
        },
        {
            "geschlecht": "n",
            "wert": "Froschgesicht"
        },
        {
            "geschlecht": "n",
            "wert": "Pupsgesicht"
        },
        {
            "geschlecht": "n",
            "wert": "Huhn"
        },
        {
            "geschlecht": "f",
            "wert": "Hexe"
        },
        {
            "geschlecht": "m",
            "wert": "Sesselfurzer"
        },
        {
            "geschlecht": "f",
            "wert": "Sesselfurzerin"
        },
        {
            "geschlecht": "f",
            "wert": "Sau"
        },
        {
            "geschlecht": "f",
            "wert": "Kartoffelnase"
        },
        {
            "geschlecht": "f",
            "wert": "Flachzange"
        },
        {
            "geschlecht": "f",
            "wert": "Dumpfbacke"
        }
    ]
}

#f = open("/home/pi/python/insults2.json", 'w')
#ensure_ascii = False
#ins_data = ins_data.replace('\n', '')
#print ins_data
#json.dump(ins_data, f, ensure_ascii, True, True, 0)
#f.close()


filename = '/home/pi/data/audio/insult{}.wav'


def pickRandom(list):
    return 0


def pickAdjektiv(g, idx):
    arr = ins_data['adjektive']
    rnd = random.randint(0, len(arr) - 1)
    return arr[rnd][g]


def pickSubstantiv(idx):
    arr = ins_data['substantive']
    if idx < 0:
        rnd = random.randint(0, len(arr) - 1)
    return (arr[rnd]['wert'], arr[rnd]['geschlecht'])


def pickSteigerung(g, idx):
    arr = ins_data['steigerungen']
    rnd = random.randint(0, len(arr) - 1)
    return arr[rnd]


def get_insult(idx_steig, idx_adj, idx_sub):
    subst, g = pickSubstantiv(idx_sub)
    return "Du " + pickSteigerung(g, idx_steig) + " " + pickAdjektiv(g, idx_adj) + " " + subst


def speak_next_insult():
    max = len(ins_data['steigerungen']) * len(ins_data['adjektive']) * len(ins_data['substantive'])
    fn = filename.format(random.randint(0, max))
    print "speaking insult " + str(fn)
    play_wav(fn)


def create_insult_audio_db():
    i = 0
    for steig in ins_data['steigerungen']:
        for adj in ins_data['adjektive']:
            for subs in ins_data['substantive']:
                g = subs['geschlecht']
                substantiv = subs['wert']
                i += 1
                filename = '/home/pi/data/audio/insult{}.wav'.format(i)
                adjektiv = adj[g]
                steigerung = steig
                text = "Du {} {} {}".format(steigerung, adjektiv, substantiv)
                #print "Writing {} to {}".format(text, filename)
                text2wav(text, filename, 30, 1.2)


if __name__ == "__main__":
    insult = get_insult(-1, -1, -1)
    print insult
    speak_next_insult()
    create_insult_audio_db()
