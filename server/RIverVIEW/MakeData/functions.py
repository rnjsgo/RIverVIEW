import json
import re
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from functools import partial
from multiprocessing import Pool
import os
from pathlib import Path
from PIL import Image
from wordcloud import WordCloud
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
def Crawling(product_num, merchant_num, store, pageNo):
    #REVIEW_CREATE_DATE_DESC, REVIEW_RANKING
    sort_type = 'REVIEW_RANKING'
    if pageNo %2== 0:
        sort_type = 'REVIEW_RANKING'
    elif pageNo %2== 1:
        sort_type = 'REVIEW_CREATE_DATE_DESC'
    try:
        if store == 'shopping':
            url = ('https://smartstore.naver.com/i/v1/reviews/paged-reviews?page={}&pageSize=10&merchantNo={}&originProductNo={}&sortType='+sort_type).format(
                 pageNo, merchant_num, product_num)  # REVIEW_RANKING
        elif store == 'smartstore':
            url = ('https://{}.naver.com/i/v1/reviews/paged-reviews?page={}&pageSize=10&merchantNo={}&originProductNo={}&sortType='+sort_type).format(
                store, pageNo, merchant_num, product_num)  # REVIEW_RANKING
        elif store == 'brand':
            url = ('https://{}.naver.com/n/v1/reviews/paged-reviews?page={}&pageSize=10&merchantNo={}&originProductNo={}&sortType='+sort_type).format(
                store, pageNo, merchant_num, product_num)  # REVIEW_RANKING
        else:
            url = ''
        response = urlopen(url)
        json_data = json.load(response)['contents']
        temp=[]

        for rev in json_data:
            if rev['reviewContent']:
                review = rev['reviewContent'].replace("\n", " ")
                temp.append(review)

        return temp

    except:
        return


def start_crawling(product_num, url=None):

        #url 쪼개서 원하는 정보 얻기
        url_basic = url
        store = url_basic.split('//')[1].split('.')[0]  # 네이버 쇼핑, 스마트스토어, 브랜드스토어 구별
        data = requests.get(url_basic, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        product_detail = soup.find_all('script')[1].text.split(',')

        #판매자 번호 얻기
        for detail in product_detail:
            if '"payReferenceKey"' in detail:
                merchant_num = detail.split(':')[1].replace('"', '')
                break
        else:
            merchant_num = ''

        #상품 번호 얻기
        for detail in product_detail:
            if '"originProductNo"' in detail:
                product_num = re.sub('[^0-9]', '', detail.split(':')[1].replace('"', ''))
                if product_num == '':
                    continue
                break
            elif '"sellerImmediateDiscountPolicyNo"' in detail:
                product_num = re.sub('[^0-9]', '', detail.split(':')[2].replace('"', ''))
                if product_num == '':
                    continue
                break



        product_name = soup.find('h3', attrs={'class': '_22kNQuEXmb _copyable'}).text.strip()
        img_src = soup.find('div', attrs={'class': '_23RpOU6xpc'}).find('img')['src']

        pool = Pool(4)
        func = partial(Crawling, product_num,merchant_num,store)
        temp= pool.map(func, range(1, 40))
        pool.close()
        pool.join()
        temp = list(filter(None, temp))
        # for page in tqdm(range(1,21)):
        #     temp=Crawling(product_num,merchant_num,store,page,temp)

        # pool.map을 사용하기위해 매개변수가 하나인 함수로 만들기 위해 새로 함수 생성
        # 네이버쇼핑 페이지에서는 한페이지에 리뷰 20개, JSON은 한페이지에 리뷰 10개 저장
        #그래서 리뷰 10페이지까지 보고싶다하면 20페이지까지로 설정해야 다 가져올수 잇음
        temp=sum(temp,[])
        review_data = pd.DataFrame(temp,columns=['review'])
        return review_data, url,product_name,img_src



def make_wordcloud(words, filename):
    base_dir = Path(__file__).resolve().parent
    static_dir = os.path.join(base_dir, '../../static')
    filename = static_dir + '/image/wordcloud/'+filename
    fontpath = static_dir + '/fonts/jua.ttf'
    mask = np.array(Image.open(static_dir+'/image/circle.png'))
    wordcloud = WordCloud(font_path=fontpath, mask= mask).generate_from_frequencies(words)
    wordcloud.to_file(filename+'.png')
