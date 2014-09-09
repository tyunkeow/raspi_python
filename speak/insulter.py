#!/usr/bin/python
# insulter.py

import json
import random
from text2wav import play_sound, text2soundfile, AUDIO_DIR


ins_data = {
    "adjektive": [
        {
            'm': "haesslicher",
            "f": "haessliche",
            "n": "haessliches"
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
            "n": "schlechtes"
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
    "steigerungen": ["sehr", "massiv", "extrem", "besonders", "ausserordentlich", "super"],
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
            "wert": "Heckenpenner"
        },
        {
            "geschlecht": "m",
            "wert": "Schweinepriester"
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
            "geschlecht": "m",
            "wert": "Idiot"
        },
        {
            "geschlecht": "m",
            "wert": "Trottel"
        },
        {
            "geschlecht": "m",
            "wert": "Grotten-olm"
        },
        {
            "geschlecht": "m",
            "wert": "Pimmelbaer"
        },
        {
            "geschlecht": "n",
            "wert": "Schwein"
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
            "geschlecht": "n",
            "wert": "Luder"
        },
        {
            "geschlecht": "n",
            "wert": "Horrt-kind"
        },
        {
            "geschlecht": "f",
            "wert": "Hexe"
        },
        {
            "geschlecht": "f",
            "wert": "Made"
        },
        {
            "geschlecht": "f",
            "wert": "Schlampe"
        },
        {
            "geschlecht": "f",
            "wert": "Flachzange"
        },
        {
            "geschlecht": "f",
            "wert": "Hackfresse"
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


FILENAME_PATTERN = AUDIO_DIR + 'insult{}.aiff'


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
    fn = FILENAME_PATTERN.format(random.randint(0, max))
    print "speaking insult " + str(fn)
    play_sound(fn)


def create_insult_audio_db():
    i = 0
    for steig in ins_data['steigerungen']:
        for adj in ins_data['adjektive']:
            for subs in ins_data['substantive']:
                g = subs['geschlecht']
                substantiv = subs['wert']
                i += 1
                filename = FILENAME_PATTERN.format(i)
                adjektiv = adj[g]
                steigerung = steig
                text = "Du {} {} {}".format(steigerung, adjektiv, substantiv)
                #print "Writing {} to {}".format(text, filename)
                text2soundfile(text, filename)


if __name__ == "__main__":
    #create_insult_audio_db()

    insult = get_insult(-1, -1, -1)
    print insult
    speak_next_insult()
