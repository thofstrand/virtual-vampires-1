from django.http import JsonResponse
from django.shortcuts import render
import random
import pandas as pd
# Create your views here.
from django.shortcuts import render
from phrase_table.models import MyVerb, Pronoun
from phrase_table.serializer import VerbSerializer, PronounSerializer

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from backend_scripts.converters.english import EnglishConverter
from backend_scripts.utils import exc_to_dict
import logging
logger = logging.getLogger('django')

class VerbViewSet(viewsets.ModelViewSet):
    queryset = MyVerb.objects.all()
    serializer_class = VerbSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class PronounViewSet(viewsets.ModelViewSet):
    queryset = Pronoun.objects.all()
    serializer_class = PronounSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
 
 
def get_random_verb_pair(request):
    items = list(MyVerb.objects.all())
    if len(items) > 0:
        random_item = random.choice(items)

        return JsonResponse({'en': random_item.english, 'sp': random_item.spanish})
    return JsonResponse({'en': 'Null', 'sp': 'Null'})


def get_random_english_sentence(request):
    with open("data/test_english_sentences.tsv", "r") as f:
        en_feats = f.read().splitlines()
    en_feats = [feats.strip().split("\t")[0] for feats in en_feats]
    past_tense_exc = exc_to_dict("data/past_tense_exceptions.csv")
    past_part_exc = exc_to_dict("data/irregular_verbs_past_participle.csv")

    english_converter = EnglishConverter(past_tense_exc, past_part_exc)

    random.shuffle(en_feats)
    rand_en_sentence = english_converter.generate_sentence(en_feats[0])
    return JsonResponse({'en':rand_en_sentence})

def get_en_es_translation(request):
    # Provide random sentence with proper translation.
    # call random english sentence to get other incorrect translations
    en_word, es_word = get_random_word_pair("en", "es")
    feats, rand_sentence = get_random_sentence(en_word)
    rand_sentence_translated = translate(es_word,feats,  "en", "sp")

    return JsonResponse({'en': rand_sentence, 'sp': rand_sentence_translated.split(" ")}, json_dumps_params={'ensure_ascii': False})

def get_es_right_verb(request):
    # provide verb tense
    return JsonResponse({'sentence': 'he ____',
                         'verb': 'jump',
                         'correct': 'jumped' ,
                         'wrong': ['will run', 'eats', 'laughs']
                         })


def get_random_word_pair(src, tgt):
    with open("../data/verbs.tsv", "r", encoding="utf-8") as f:
        verbs = f.read().splitlines()
    verbs = [verb.split() for verb in verbs]
    
    res = random.choice(verbs)
    return res[0], res[1]


def get_random_sentence(word):
    
    sp = ["1s", "2s", "3s", "1p", "2p", "3p"]
    tense = ["PAST", "FUT", "IMP", "PRES"]
    neg = ["NEG+", ""]
    
    past_tense_exc = exc_to_dict("../data/past_tense_exceptions.csv")
    past_part_exc = exc_to_dict("../data/irregular_verbs_past_participle.csv")

    english_converter = EnglishConverter(past_tense_exc, past_part_exc)
    feats = random.choice(neg)  + random.choice(sp) + "+" + random.choice(tense) + "+" + word
    sentence = english_converter.generate_sentence(feats)
    return feats, sentence

def translate(word, feats, src, tgt):
    """
    word: word to translate in target lang
    feats: features of the word (incuding word)
    
    """
    feats = feats[:feats.rindex("+")]+ "+" + word
    df = pd.read_csv("../data/test_spanish_sentences.tsv", sep="\t", header = None, encoding="utf-8")
    df = df[df[0] == feats]
    return df[1].values[0]

    
