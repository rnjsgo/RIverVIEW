from functions import *
from django.shortcuts import render, redirect
from .models import ProductModel,  ProductKeyword
import re
from functions import *
# from viz_trend import *
from collections import Counter, defaultdict

def foward_home(request):
    if request.method == 'GET':
        return render(request, 'RIverVIEW/main.html')

def view_details(request, product_id):
    product = ProductModel.objects.get(product_num= product_id)
    result_keyword=[]
    pos_keyword = []
    neg_keyword = []
    keywords = {}
    result_keyword_cnt=0
    whole_review=0
    ai_score=0

    # 해당 상품의 키워드 처리
    for keyword in ProductKeyword.objects.filter(product_id= product_id):
        score=keyword.keyword_score
        frequency=keyword.keyword_frequency
        name=keyword.keyword
        whole_review+=frequency

        #AI score 계산 ('_etc'포함하여 계산)
        ai_score+=score*frequency

        #키워드 이름이 '_etc'(키워드가 포함되지 않은 리뷰들)에 대해서는 처리하지 않음
        if name =='_etc':
            continue

        #만족도가 50이 넘으면 긍정키워드, 글엏지 않으면 부정키워드로 구분
        if score > 50 :
            pos_keyword.append(keyword)

        elif score < 50 :
            neg_keyword.append(keyword)

        keywords[name] = frequency #워드클라우드를 만들기 위한 딕셔너리
        result_keyword.append(keyword)  #보여줄 키워드를 제한하기 위해 새로 만든 리스트
        result_keyword_cnt+=1

    ai_score/=whole_review
    ai_score=round(ai_score,1)
    product.product_score=ai_score
    product.save()

    make_wordcloud(keywords, str(product_id))

    pos_keyword.sort(key=lambda x: x.keyword_score,reverse=True)
    neg_keyword.sort(key=lambda x: x.keyword_score)

    context = {
        "product": product,
        "neg_keyword": neg_keyword[:3],
        "neg_keyword_cnt": len(neg_keyword[:3]),
        "pos_keyword": pos_keyword[:3],
        "pos_keyword_cnt": len(pos_keyword[:3]),
        "result_keyword":result_keyword[:(result_keyword_cnt//2)],
        "result_keyword_cnt":result_keyword_cnt//2
    }
    return render(request, 'RiverView/product_details.html',context)

def search(request):
    first = 1
    if request.method == 'POST':
        url= request.POST.get("url", '')
        if '/' in url:
            #url 분리해서 상품번호 따오기
            product_num = url.split('/')[-1].split('?')[0]

            #url 비어있을 때
            if url == '':
                return render(request, 'RIverVIEW/main.html')

            # 이 부분은 전에 분석했던 상품들 db에 저장되어 있으면 그걸로 분석 하겠다는 뜻 같음. 꼭 필요한지 잘 모르겠음
            # elif ProductModel.objects.filter(product_num=product_num).exists():
            #     search_product = ProductModel.objects.get(product_num=product_num)
            #     search_product.search_value += 1
            #     search_product.save()
            #     id = search_product.id
            #     return redirect('/modal/{}/'.format(id))

            # 크롤링

            # tem_data, pre_product_name, img_src, price, categories, result, keyword, keyword_ratio = lets_do_crawling(
            #     site, product_num, url)
            else:
                if 'naver' in url:
                    start_crawling(product_num, url)
                else: # 지원하지 않는 URL 형식
                    return render(request, 'RIverVIEW/main.html',  {'first': first})

                # 상품 이름 전처리
                # product_name = []
                # for sen in pre_product_name.split():
                #     if '[' in sen or ']' in sen or '/' in sen:
                #         pass
                #     else:
                #         product_name.append(sen)
                # product_name = ' '.join(product_name).strip()
                #
                # xai_before_text = tem_data['xai_before_text']
                # xai_value = tem_data['xai_value']
                # xai_positive_negative = tem_data['xai_positive_negative']
                # dates = tem_data['date']
                # product = ProductModel.objects.create(product_url=url, product_name=product_name,
                #                                       img_src=img_src, price=price,
                #                                       categories=categories, product_num=product_num, search_value=1)
                # product_score_list = []
                # for index, row in tem_data.iterrows():
                #     review_model = ReviewModel()
                #     word_list = keyword_in_review(row['review'], keyword)
                #     result_words = ''
                #     if word_list:
                #         result_words = '#' + " #".join(word_list).strip()
                #     review_model.keywords = result_words
                #     review_model.product_id = product
                #     review_model.review = " ".join(xai_before_text[index])
                #     tmp_score = xai_positive_negative[index]
                #     review_model.score = tmp_score
                #     product_score_list.append(tmp_score)
                #     review_model.morph = " ".join(xai_before_text[index])
                #     review_model.xai_vale = " ".join([*map(lambda x: str(x), xai_value[index])])
                #     review_model.date = dates[index]
                #     review_model.save()
                # product.pos_neg_rate = int(sum([1 for i in product_score_list if i > 5]) * 100 / (index + 1))
                # product.total_value = round(sum(product_score_list) / (index + 1), 1)
                # product.save()
                #
                # for word, sentence in result.items():
                #     product_keyword = ProductKeyword()
                #     product_keyword.product_id = product
                #     product_keyword.keyword = word
                #     product_keyword.summarization = sentence
                #     product_keyword.keyword_positive = round(float(keyword_ratio[word]), 1)
                #     product_keyword.save()

            return render(request, 'home/main.html')


