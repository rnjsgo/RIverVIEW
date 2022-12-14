from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec, KeyedVectors
from gensim.models import FastText
import gensim

import tensorflow as tf
import pickle
import keras

import pandas as pd
import numpy as np

from .data_preprocess import *
from .time_check import *
from pathlib import Path
import os

NOT_IN_W2V = -999999
_T_DEBUG = 1

_t_debug = time_chk('모델 로드', _T_DEBUG)
_start = _t_debug.start()
#model load


GRU_model = tf.keras.models.load_model(os.path.join(Path(__file__).resolve().parent, 'load/GRU_Model.h5'), compile=False)
GRU_tokenizer = Tokenizer()
with open(os.path.join(Path(__file__).resolve().parent, 'load/GRU_tokenizer.pickle'), 'rb') as handle:
    GRU_tokenizer = pickle.load(handle)
_t_debug.eend(_start, _t_debug.end())

def w2v_fintune(tokenized_data):
    model_pretrained = gensim.models.Word2Vec.load(os.path.join(Path(__file__).resolve().parent, 'load/only_review.model'))
    model_finetuned = Word2Vec(vector_size=200,min_count=0,sg=1)
    model_finetuned.build_vocab(tokenized_data)
    total_examples = model_finetuned.corpus_count
    model_finetuned.build_vocab([list(model_pretrained.wv.key_to_index.keys())], update=True)
    model_finetuned.train(tokenized_data, total_examples= total_examples, epochs= 1)
    model_finetuned.save(os.path.join(Path(__file__).resolve().parent, 'load/only_review.model'))
    return model_finetuned.wv

def ft_fintune(tokenized_data):
    #model_pretrained = gensim.models.Word2Vec.load(os.path.join(Path(__file__).resolve().parent, 'load/fast_text.model'))
    model_finetuned = FastText(tokenized_data,vector_size=200,min_count=5,window=5,workers=4,sg=1)
    #model_finetuned.build_vocab(tokenized_data)
    total_examples = model_finetuned.corpus_count
    #model_finetuned.build_vocab([list(model_pretrained.wv.key_to_index.keys())], update=True)
    #model_finetuned.train(tokenized_data, total_examples= total_examples, epochs= 1)
    #model_finetuned.save(os.path.join(Path(__file__).resolve().parent, 'load/fast_text.model'))
    return model_finetuned.wv

#w2v 유사도 확인
#단어끼리 비슷한 정도 반환
def get_word_similarity(w1,w2,w2v):
    if w1 in w2v and w2 in w2v:
        return w2v.similarity(w1,w2)
    return NOT_IN_W2V

#GRU Model을 이용해서
#새로 들어온 문장에 대해서 데이터 전처리 이후
#0~1사이의 예측값(1: 긍정 0: 부정)을 100을 곱해 반환
def get_sentence_score(new_sentence, max_len = 80):
    sentence = tok_concat_str(new_sentence)
    if len(sentence) ==0:
        return -999
    encoded = GRU_tokenizer.texts_to_sequences([sentence])
    pad_new = pad_sequences(encoded, maxlen = max_len)
    score = float(GRU_model.predict(pad_new, verbose= 0))
    '''
    if(score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))
    '''
    return score * 100
