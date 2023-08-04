from .string_control import *

from .time_check import *


#데이터 정제
'''
total_data = dataframe_limit_string_len(total_data, col_name, 200)
total_data.reset_index(drop=True, inplace=True)
total_data = dataframe_cut(total_data,200)
'''

#필요한 데이터
#리뷰가 담긴 데이터프레임 total_data
#데이터프레임에서 리뷰의 열이름 col_name    default = 'review'
#제한할 데이터의 크기 limit_size,    default = 200
#제품의 이름 문자열 product_name

def  make_final_data(total_data: pd.DataFrame, col_name='review', limit_size = 100, product_name = '',T_DEBUG = 1):
    t = time_chk('키워드추출~AI점수', T_DEBUG)
    st = t.start()
    total_data = dataframe_limit_string_len(total_data, col_name=col_name,str_len = 400)
    total_data = dataframe_clean(total_data,col_name)
    total_data = dataframe_make_clean_str_col(total_data,col_name=col_name)
    #total_data = total_data.sample(frac=1)
    total_data.reset_index(drop=True, inplace=True)
    total_data = dataframe_cut(total_data,limit_size)

    total_data = dataframe_make_tokenized_col(total_data)
    total_data['len'] = total_data['tokenized_data'].apply(len)
    max_len = max(total_data['len'])
    for i in range(max_len, 0, -1):
        if len(total_data.loc[total_data['len']>i]) / len(total_data) >0.95:
            max_len = i
            break


    t.cut('데이터 전처리')
    wv = w2v_fintune(total_data['tokenized_data'])
    #wv = ft_fintune(total_data['tokenized_data'])
    t.cut('w2v 학습')
    keyword = get_keyword(total_data, product_name, wv)
    t.cut('키워드 추출')

    df, score_sum, key_freq, key_score = make_keyword_dataframe(
        keyword= keyword,
        data= total_data,
        col= col_name,
        size=limit_size,
        view_single=True,
        wv= wv,
        max_len=max_len
    )
    keyword = [k for k,v in key_score.items()]
    df = pd.concat([total_data['review'],total_data['tokenized_data'],df],axis=1)
    df.to_csv(product_name+'.csv')
    t.cut('데이터프레임 생성')
    keyword_example = get_keyword_example(
        data= df,
        col= col_name,
        key_score= key_score,
        size=limit_size,
        wv=wv
        )#
    t.cut('keyword example')
    t.eend(st, t.end())
    return keyword, keyword_example, key_score, key_freq
