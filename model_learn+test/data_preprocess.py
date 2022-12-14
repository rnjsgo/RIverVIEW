from konlpy.tag import Mecab

import pandas as pd
import numpy as np
import re

#mecab 윈도우
#mecab = Mecab("C:/mecab/mecab-ko-dic")
#mecab 맥
#mecab = Mecab

#stopwords위치 지정
#useless_word_dic = pd.read_csv('./stop_word.csv')


mecab = Mecab("C:/mecab/mecab-ko-dic")

stopwords = set(['JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC'])
get_words = set(['NNG','NNP','VV','VA',])
useless_word = set(['만족', '구입', '구매', '생각', '때', '주문', '정도', '느낌', '맘', '마음', '상품', '제품', '물건','아서','어서','해요','감사','세요','기대','모르','예요', '사용','후기','빠르','괜찮','리뷰','처음'])
useless_word_dic = pd.read_csv('./save_data/stop_word.csv')
useless_word_dic = useless_word_dic.values.tolist()
tmp = []
for w in useless_word_dic:
    tmp.append(*w)
useless_word_dic = tmp

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
    text = re.sub("\n", repl=' ', string=text)#\n 제거
    return text   

def dataframe_str_clean(df, col_name):
    k = 0
    data_frame = df.copy()
    for text in data_frame[col_name]:
        text = clean_str(text)
        data_frame.loc[k, col_name] = ''.join(text).strip()
        k = k + 1
    return data_frame

def dataframe_clean_NA(data_frame, col_name):
    drop_idx = data_frame[data_frame[col_name]==''].index
    data_frame = data_frame.drop(drop_idx)
    return data_frame

def dataframe_clean(df, col_name):
    df = dataframe_clean_NA(df, col_name)
    df.drop_duplicates(subset=[col_name], inplace = True)
    return df

def not_useless(word):
    return (word not in useless_word) and (word not in useless_word_dic)

def not_stopword(tag):
    return tag not in stopwords

def mecab_tokenizer(raw, pos=get_words, stopword=stopwords): 
    from konlpy.tag import Mecab 
    m = Mecab("C:/mecab/mecab-ko-dic")
    return [word for word, tag in m.pos(raw) \
        if len(word) > 1 and \
            tag in pos and \
                tag not in stopword and\
                    not_useless(word)
                    ]

def mecab_morphs(sentence):
    return mecab.morphs(sentence)

def mecab_pos(sentence):
    return mecab.pos(sentence)

def tok_concat_str(sentence):
    return ' '.join(mecab_tokenizer(sentence))
