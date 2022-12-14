import pandas as pd
from tqdm import tqdm

from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

from .data_preprocess import *
from .AI import *
from .time_check import *

#같은 단어라면 SAMELITY보다 높아야함
_SAMELITY_ = 0.9
#비슷한 정도
_SIMILARITY_ = 0.7
#문장에서 중요한 정도 tfidf수치
_IMPORTANCE_ = 0.2
_DEFAULT_SIZE_ = 200

_T_DEBUG = 0


def get_keyword(df: pd.DataFrame, product_name, wv, col='review'):
    data_frame = df.copy()
    # 리뷰세트마다 tfidf적용해서 중요도 뽑아야함
    tfidfv = TfidfVectorizer(stop_words=stopwords, tokenizer=mecab_tokenizer, \
                             ngram_range=(1, 3), min_df=3, sublinear_tf=True)
    tfidf = tfidfv.fit_transform(data_frame[col])

    word2id = dict()
    for idx, feature in enumerate(tfidfv.get_feature_names()):
        word2id[feature] = idx

    #문장 랭킹 구하기
    entire_txt = data_frame[col].apply(normalize)
    min_count = 3
    max_length = 10
    wordrank_extractor = KRWordRank(min_count, max_length)

    beta = 0.85  # PageRank의 decaying factor beta
    max_iter = 10
    keywords, rank, graph = wordrank_extractor.extract(entire_txt, beta, max_iter)
    keyword = {}

    #tfidf를 이용해서 중요한 단어만 추출
    for i in range(len(entire_txt)):
        for w,r in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
            if w in word2id and w in wv:
                    if tfidf[i, word2id[w]] > _IMPORTANCE_ and mecab_pos(w)[0][1] in get_words:
                        keyword[w] = 0
                        
    keyword = [k for k in keyword.keys()]
    # 최종 키워드 추출
    final_keyword = {}
    # 개수는 루트 데이터개수 / 2
    keyword_cnt = int(len(data_frame) ** 0.5) // 2
    cnt = keyword_cnt
    # 키워드중, 상품과 관련된 정보는 추출하지 않기
    product_name_tok = mecab_tokenizer(product_name)

    for w in keyword:
        w = w.strip()

        product_sim_flag = True
        for i in range(len(product_name_tok)):
            if w == product_name_tok[i]:
                product_sim_flag = False
            sim = get_word_similarity(w, product_name_tok[i],wv)
            if sim >= _SAMELITY_:  # 제목이랑 같은 단어는 지우겠다.
                product_sim_flag = False
            elif sim == NOT_IN_W2V:  # w2v에 없는 단어인 경우
                product_sim_flag = False
        keyword_flag = True
                # 추가한 키워드와 비슷한 단어 제거 ->  그렇게 효과적이지 못한것같음
        if product_sim_flag:
            for keyword in final_keyword.keys():
                if get_word_similarity(w, keyword, wv) > _SAMELITY_:
                    keyword_flag = False
                            
        if product_sim_flag and keyword_flag and not_useless(w):
            final_keyword[w] = cnt
            cnt -= 1
        if cnt < 0:
            break
    if cnt == keyword_cnt:  # 키워드가 없는경우, 제목과 완전 같은 키워드를 제외하고 비슷한 단어만 제거
        for w in keyword:
            w = w.strip()

            product_sim_flag = True
            for i in range(len(product_name_tok)):
                if w == product_name_tok[i]:
                    product_sim_flag = False

                keyword_flag = True
                # 추가한 키워드와 비슷한 단어 제거 ->  그렇게 효과적이지 못한것같음
                if product_sim_flag:
                    for keyword in final_keyword.keys():
                        if get_word_similarity(w, keyword, wv) > _SAMELITY_:
                            keyword_flag = False

            if product_sim_flag and keyword_flag and not_useless(w):
                final_keyword[w] = cnt
                cnt -= 1
            if cnt < 0:
                break

    # 최종 추출 단어 반환
    ret = sorted(final_keyword.items(), key=lambda x: x[1], reverse=True)
    ret = [w for w, r in ret]
    return ret


# 사용안함
# 리뷰에서 한문장씩 잘라서 반환
def get_single_sentence(document=''):
    doc = clean_str(document)
    posed = mecab_pos(doc)
    ret = []
    now = 0
    end_word = ['VCN', 'EC', 'EF']

    for i in range(len(posed)):
        word = posed[i][0]
        word_pos = posed[i][1]
        word_len = len(word)

        pos_flag = False  # 문장이 끝나는 신호가 나왔다면 True
        if word_pos in end_word:
            pos_flag = True
            if i + 1 != len(posed):
                if posed[i + 1][0] == '요':  # mecab에서 ~~~했어요 ~~~에요 ~~~요로 끝나는 것을 요라는 글자 하나로 봐서 이경우는 무시
                    pos_flag = False

        if pos_flag:
            now = doc.find(word)
            now += word_len
            if len(doc[:now]) > 7:
                ret.append(doc[:now].strip())
                doc = doc[now:]

    if len(doc.strip()) > 2:
        ret.append(doc.strip())

    return ret


# 문장이 가지고 있는 키워드를 반환
# 문장 내에서 비슷한 키워드가 발견되면 그 키워드를 반환
def get_contain_keyword(word, sentence, wv):
    for w in sentence:
        if get_word_similarity(word, w,wv) >= _SIMILARITY_:
            return word
    return '_etc'


def get_contain_same_keyword(word, sentence, wv):
    for w in sentence:
        if get_word_similarity(word, w, wv) >= _SAMELITY_:
            return word
    return '_etc'


# 추출된 키워드를 받아서 각 키워드별 리뷰의 점수를 반환
# input : 추출된 키워드, 리뷰 데이터프레임, 리뷰데이터프레임에서 리뷰가담긴 열의 이름, 확인할 리뷰의 데이터 개수
# output : 각 리뷰별 해당 키워드의 점수가 들어있는 데이터프레임, 키워드 스코어 총합, 키워드 빈도수, 키워드별 최종 스코어
def make_keyword_dataframe(keyword=[], data=pd.DataFrame(), col='review', size=_DEFAULT_SIZE_, view_single=False, wv={}, max_len= 80):
    keyword_list = [*keyword, '_etc']
    # data에 리뷰데이터프레임
    df = data.copy()
    df = dataframe_cut(df, size)
    df.reset_index(drop=True, inplace=True)
    
    
    # ret_sentence_keyword => 행: 리뷰, 열: 해당 리뷰의 키워드
    ret_sentence_keyword = pd.DataFrame(index=range(len(df)), columns=keyword_list)
    ret_sentence_keyword = ret_sentence_keyword.fillna(0)
    # score_sum 각 키워드별 점수 합
    keyword_score_sum = {w: 0 for w in keyword_list}
    # freq 각 키워드별 빈도수
    keyword_freq = {w: 0 for w in keyword_list}

    is_NOT_contain_keyword = True
    word = ''


    if not view_single:
        for i in tqdm(df.index):
            score = get_sentence_score(df.loc[i,col], max_len= max_len)
            if score == -999:
                continue
            is_NOT_contain_keyword = True

            for w in keyword:  # 문장에 키워드를 포함하지 않는 키워드는 일단 보지않음.
                word = get_contain_same_keyword(w, df.loc[i,'tokenized_data'], wv)
                if word != '_etc':  # 지금 보는 문장에 키워드가 존재한다면,
                    is_NOT_contain_keyword = False
                    ret_sentence_keyword.loc[i, word] = score

            if is_NOT_contain_keyword:  # 문장에 키워드를 포함하고있지 않은 일반 리뷰라면,
                ret_sentence_keyword.loc[i, '_etc'] = score
    else:
        max_len = max(df['len'])
        for i in range(max_len, 0, -1):
            if len(df.loc[df['len']>i]) / len(df) >0.95:
                max_len = i
                break
        for i in tqdm(df.index):
            
            #score = get_sentence_score(df.loc[i,col], max_len= max_len)
            review_list = get_single_sentence(df.loc[i,col])
            freq = {w:1 for w in keyword}
            is_NOT_contain_keyword = True
            for sentence in review_list:
                score = get_sentence_score(sentence, max_len= max_len)
                tokend = mecab_morphs(sentence)
                if score == -999:
                    continue
                for w in keyword:  # 문장에 키워드를 포함하지 않는 키워드는 일단 보지않음.
                    word = get_contain_same_keyword(w, tokend, wv)
                    if word != '_etc':  # 지금 보는 문장에 키워드가 존재한다면
                        keyword_freq[word] += 1
                        freq[word] += 1
                        is_NOT_contain_keyword = False
                        ret_sentence_keyword.loc[i, word] = ret_sentence_keyword.loc[i, word]+score
                    

            if is_NOT_contain_keyword:  # 문장에 키워드를 포함하고있지 않은 일반 리뷰라면,
                keyword_freq['_etc'] += 1
                score = get_sentence_score(df.loc[i,col], max_len= max_len)
                if score == -999:
                    continue
                ret_sentence_keyword.loc[i, '_etc'] = score
    
    keyword_score = {}
    for w in keyword_list:
        keyword_score_sum[w] = ret_sentence_keyword[w].sum()
        keyword_freq[w] = len(ret_sentence_keyword[ret_sentence_keyword[w] != 0].index)
        if keyword_freq[w] == 0:
            del keyword_freq[w]
            del keyword_score_sum[w]
            del ret_sentence_keyword[w]
        else:
            keyword_score[w] = keyword_score_sum[w] / keyword_freq[w]
            if keyword_score[w] > 100:
                keyword_score[w] = 100
    
    return ret_sentence_keyword, keyword_score_sum, keyword_freq, keyword_score


# 키워드와 같은 의견을 가지고 있는지 비교하는 함수
def abs(a, b):
    ret = a - b
    if ret < 0:
        ret = -ret
    return ret


def is_same_opinion(key_score, sentence_score, samelity):
    return ((key_score > 50 and sentence_score > 100 - samelity) or (
                key_score < 50 and sentence_score < samelity))


# 리뷰 원본 데이터에서 키워드가 들어간 문장들 중에서
# 키워드 점수와 비슷한 문장을 골라 예시로 반환
# data = review 데이터프레임 원본, col = 리뷰가 들어있는 열
# key_score= 키워드별 점수가 들어있는 딕셔너리, 0번인덱스부터 살펴볼 양
def get_keyword_example(data: pd.DataFrame, wv, col='review', key_score={}, size=_DEFAULT_SIZE_, max_len = 80):
    total_data = data.copy()
    keyword = [k for k, v in key_score.items()]
    example_sentece = {}
    cnt = 0
    for i in tqdm(total_data.index):
        for w in keyword:
            if total_data.loc[i,w] != 0:
                reveiw_sentence = get_single_sentence(total_data.loc[i, col])
                find_example = False
                for sentence in reveiw_sentence:
                    if not find_example:
                        key = get_contain_same_keyword(w, mecab_tokenizer(sentence),wv)
                        if key != '_etc':
                            sentence_score = get_sentence_score(sentence, max_len= max_len)
                            if sentence_score == -999:
                                continue
                            review_score = total_data.loc[i, key]
                            if is_same_opinion(key_score[key], sentence_score, 50) and is_same_opinion(key_score[key], review_score, 45):
                                find_example = True
                            elif abs(key_score[key], sentence_score) < 10 and is_same_opinion(key_score[key], review_score, 55) :
                                find_example = True
                        
                            
                            if find_example:
                                if w in example_sentece:
                                    if abs(example_sentece[w]['sentence_score'],key_score[key]) < abs(sentence_score,key_score[key]):
                                        find_example=False
                                        
                            if find_example: 
                                if len(total_data.loc[i, col]) < 60:
                                    example_sentece[w] = {
                                        'original_review': total_data.loc[i, col],
                                        'sentence_score': sentence_score,
                                        'reason_sentence': sentence
                                    }
                                else:
                                    origin = mecab_tokenizer(total_data.loc[i, col][:60])
                                    if get_contain_same_keyword(w,origin,wv)==w:
                                        example_sentece[w] = {
                                        'original_review': total_data.loc[i, col][:60]+'...',
                                        'sentence_score': sentence_score,
                                        'reason_sentence': sentence
                                        }
                                    else:
                                        example_sentece[w] = {
                                            'original_review': total_data.loc[i, col][:55-len(sentence)]+'...(중략)...'+sentence,
                                            'sentence_score': sentence_score,
                                            'reason_sentence': sentence
                                        }
                                    
    for w in keyword:
        if w not in example_sentece:
            example_sentece[w] = {
                'original_review': '해당 키워드의 리뷰를 찾을 수 없습니다.',
                'sentence_score': 0,
                'reason_sentence': '해당 키워드의 리뷰를 찾을 수 없습니다.'
            }
    return example_sentece

'''
문장단위로 리뷰를 쪼개고, 카테고리 나눠서 카운트
    t=time_chk('문장 종류 확인해보기')
    st = t.start()
    same_keyword_freq = {k:0 for k in keyword}
    same_keyword_freq['_etc'] = 0
    simil_keyword_freq = {k:0 for k in keyword}
    simil_keyword_freq['_etc'] = 0
    sentence_cnt = 0
    for review in total_data['review']:
        sentence_list = get_single_sentence(review)
        sentence_cnt += len(sentence_list)
        for sentence in sentence_list:
            etc_flag = True
            for kw in keyword:
                sim_word = get_contain_keyword(kw, sentence)
                if sim_word != '_etc':
                    etc_flag = False
                    simil_keyword_freq[sim_word] += 1
            if etc_flag:
                simil_keyword_freq['_etc'] += 1
    t.end()
    print('similar keyword set')
    print(simil_keyword_freq)
    t.start()
    for review in total_data['review']:
        sentence_list = get_single_sentence(review)
        for sentence in sentence_list:
            etc_flag = True
            for kw in keyword:
                same_word = get_contain_same_keyword(kw, sentence)
                if same_word != '_etc':
                    etc_flag = False
                    same_keyword_freq[same_word] += 1
            if etc_flag:
                same_keyword_freq['_etc'] += 1
    t.end()
    print('same keyword set')
    print(same_keyword_freq)
    print('\n\nsentence count')
    print(sentence_cnt)
    t.eend(st)
'''
