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

def  make_final_data(total_data: pd.DataFrame, col_name='review', limit_size = 200, product_name = '',T_DEBUG = 1):
    t = time_chk('키워드 추출', T_DEBUG)
    st = t.start()
    keyword = get_keyword(total_data, product_name)
    t.cut('키워드 데이터프레임 생성')
    df, score_sum, key_freq, key_score = make_keyword_dataframe(
        keyword= keyword,
        data= total_data,
        col= col_name,
        size=limit_size,
        view_single=False
    )
    t.cut('키워드 샘플 추출')
    keyword_example = get_keyword_example(
        data= total_data,
        col= col_name,
        key_score= key_score,
        size=limit_size
        )
    t.eend(st, t.end())
    return keyword, keyword_example, key_score, key_freq