from konlpy.tag import Mecab

import pandas as pd
import numpy as np
import re
from pathlib import Path
import os


#windows면  0, 유닉스계열 1
__OS_MODE = 0

stopwords = set(['JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC'])
get_words = set(['NNG','NNP',])
nn_v_words = set(['NNG','NNP','VV','VA',])
useless_word = set(['만족', '구입', '구매', '생각', '때', '주문', '정도', '느낌', '맘', '마음', '상품', '제품', '물건','아서','어서','해요','감사','세요','기대','모르','예요', '사용','후기','빠르','괜찮','리뷰','처음','부분'])
useless_word_dic = pd.read_csv(os.path.join( Path(__file__).resolve().parent, 'load/stop_word.csv'))
useless_word_dic = useless_word_dic.values.tolist()
tmp = []
for w in useless_word_dic:
    tmp.append(*w)
useless_word_dic = tmp

if __OS_MODE == 0:
    #windows
    mecab = Mecab('C:/mecab/mecab-ko-dic')
elif __OS_MODE == 1:
    #unix
    mecab = Mecab()



####################################################################################
#                             데이터프레임 관련 함수
####################################################################################
def dataframe_make_tokenized_col(df: pd.DataFrame):
    data = df.copy()
    data['tokenized_data'] = data['review'].apply(mecab_tokenizer)
    return data

def dataframe_get_col_to_list(df: pd.DataFrame, col):
    data = df.copy()
    ret = data[col].tolist()
    ret = list(filter(None, ret))
    return ret
    
def dataframe_cut(df: pd.DataFrame, size):
    data_frame = df.copy()
    return data_frame.truncate(before=0,after=size)

#데이터프레임의 문자열의 특수기호등 모두 제거
def dataframe_make_clean_str_col(df: pd.DataFrame, col_name: str):
    data_frame = df.copy()
    data_frame['clean_str'] = data_frame[col_name].apply(clean_str)
    return data_frame

#데이터프레임 none값 제거
def dataframe_clean_NA(df: pd.DataFrame, col_name: str):
    data_frame = df.copy()
    drop_idx = data_frame[data_frame[col_name]==''].index
    data_frame = data_frame.drop(drop_idx)
    return data_frame

#데이터프레임에서
def dataframe_clean(df: pd.DataFrame, col_name: str):
    data_frame = df.copy()
    data_frame = dataframe_clean_NA(data_frame, col_name)
    data_frame.drop_duplicates(subset=[col_name], inplace = True)

    return data_frame
#
def dataframe_limit_string_len(df: pd.DataFrame, col_name: str, str_len):
    data_frame = df.copy()
    data_frame['len'] = data_frame[col_name].apply(len)
    drop_idx = data_frame[data_frame['len'] > str_len].index
    data_frame.drop(drop_idx,axis=0,inplace=True)
    data_frame.drop(['len'],axis=1,inplace=True)
    return data_frame

####################################################################################
#                               문자열 관련 함수
####################################################################################
def not_useless(word):
    return (word not in useless_word) and (word not in useless_word_dic)

def not_stopword(tag):
    return tag not in stopwords

def mecab_morphs(sentence: str):
    return mecab.morphs(sentence)

def mecab_pos(sentence: str):
    return mecab.pos(sentence)

#메캅 형태소 분리기

def mecab_tokenizer(raw,pos=nn_v_words, stopword=stopwords):
    return [word for word, tag in mecab_pos(raw) \
        if len(word) > 1 and\
            tag in pos and \
            tag not in stopword]

#기본적으로 형태를 분리하나
#   한글자 미만인 형태소,
#   미리 지정해두지 않은 단어,
#   미리 설정한 의미없는 단어를 제외하고
#   형태소를 분ㄹ하여 반환
def mecab_get_useful_word(raw, pos=nn_v_words, stopword=stopwords):
    return [word for word, tag in mecab_pos(raw) \
            if len(word) > 1 and \
                tag in pos and \
                tag not in stopword and\
                    not_useless(word)]

#형태소분리 -> 다시 이어붙이기
def tok_concat_str(sentence: str):
    sentence = clean_str(sentence)
    return ' '.join(mecab_morphs(sentence))

def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s\\n]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    text = re.sub("\n", repl=' ', string=text)
    return text   

def print_pretty(st, trg):
    print()
    print('*'*60)
    print(st.center(50), end = '\n\n')
    if  isinstance(trg, dict):
        for k, v in trg.items():
            print(k,' : ',v)
    else:
        print(trg)
    print('*'*60)
    print()
