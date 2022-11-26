from functions import *
from django.shortcuts import render, redirect
from .models import ProductModel, ReviewModel, ProductKeyword
import re
from functions import *
# from viz_trend import *
from collections import Counter, defaultdict

def foward_home(request):
    if request.method == 'GET':
        return render(request, 'RIverVIEW/main.html')

def view_details(request, product_id):
    product = ProductModel.objects.get(product_num= product_id)
    pos_keyword = []
    neg_keyword = []
    keywords = {}
    for keyword in ProductKeyword.objects.filter(product_id= product_id):
        if keyword.keyword_score > 0 and len(pos_keyword) <= 3:
            pos_keyword.append(keyword)
        elif keyword.keyword_score < 0 and len(neg_keyword) <= 3:
            neg_keyword.append(keyword)
        if keyword.keyword in keywords:
            keywords[keyword.keyword] = keywords[keyword] + 1
        else:
            keywords[keyword.keyword] = 1
    make_wordcloud(keywords, str(product_id))

    context = {
        "product": product,
        "neg_keyword": neg_keyword[:5],
        "neg_keyword_cnt": len(neg_keyword[:5]),
        "pos_keyword": pos_keyword[:5],
        "pos_keyword_cnt": len(pos_keyword[:5])
    }
    return render(request, 'RiverView/product_details.html',context)
def search(request):
    first = 1
    if request.method == 'POST':
        url= request.POST.get("url", '')
        if '/' in url:
            #url 분리해서 상품번호 따오기
            if 'share' in url:   #share가 뭘까..
                product_num = url.split('/')[-2].split('?')[0]
            else:
                product_num = url.split('/')[-1].split('?')[0]

            #url 비어있을 때
            if url == '':
                return render(request, 'RIverVIEW/main.html')

            # 이 부분은 전에 분석했던 상품들 db에 저장되어 있으면 그걸로 분석 하겠다는 뜻 같음. 꼭 필요한지 잘 모르겠음
            elif ProductModel.objects.filter(product_num=product_num).exists():
                search_product = ProductModel.objects.get(product_num=product_num)
                search_product.search_value += 1
                search_product.save()
                id = search_product.id
                return redirect('/modal/{}/'.format(id))
            #11번가 , 네이버의 url을 받았을 때 크롤링
            else:
                if '11st' in url:
                    site = 1
                    tem_data, pre_product_name, img_src, price, categories, result, keyword, keyword_ratio = lets_do_crawling(
                        site, product_num)
                elif 'naver' in url:
                    site = 2
                    tem_data, pre_product_name, img_src, price, categories, result, keyword, keyword_ratio = lets_do_crawling(
                        site, product_num, url)
                else: # 지원하지 않는 URL 형식
                    return render(request, 'RIverVIEW/main.html',  {'first': first})


                product_name = []
                for sen in pre_product_name.split():
                    if '[' in sen or ']' in sen or '/' in sen:
                        pass
                    else:
                        product_name.append(sen)

                product_name = ' '.join(product_name).strip()

                xai_before_text = tem_data['xai_before_text']
                xai_value = tem_data['xai_value']
                xai_positive_negative = tem_data['xai_positive_negative']
                dates = tem_data['date']
                product = ProductModel.objects.create(product_url=url_src, product_name=product_name,
                                                      img_src=img_src, price=price,
                                                      categories=categories, product_num=product_num, search_value=1)
                product_score_list = []
                for index, row in tem_data.iterrows():
                    review_model = ReviewModel()
                    word_list = keyword_in_review(row['review'], keyword)
                    result_words = ''
                    if word_list:
                        result_words = '#' + " #".join(word_list).strip()
                    review_model.keywords = result_words
                    review_model.product_id = product
                    review_model.review = " ".join(xai_before_text[index])
                    tmp_score = xai_positive_negative[index]
                    review_model.score = tmp_score
                    product_score_list.append(tmp_score)
                    review_model.morph = " ".join(xai_before_text[index])
                    review_model.xai_vale = " ".join([*map(lambda x: str(x), xai_value[index])])
                    review_model.date = dates[index]
                    review_model.save()
                product.pos_neg_rate = int(sum([1 for i in product_score_list if i > 5]) * 100 / (index + 1))
                product.total_value = round(sum(product_score_list) / (index + 1), 1)
                product.save()

                for word, sentence in result.items():
                    product_keyword = ProductKeyword()
                    product_keyword.product_id = product
                    product_keyword.keyword = word
                    product_keyword.summarization = sentence
                    product_keyword.keyword_positive = round(float(keyword_ratio[word]), 1)
                    product_keyword.save()

            return render(request, 'home/main.html',
                          {'TOP_Products': T_Products, 'RECENT_Products': R_Products, 'first': first})

        else:
            search_cate = url_src
            if search_cate == '':
                return render(request, 'home/main.html',
                              {'error01': 'URL 혹은 카테고리를 입력해주세요!', 'TOP_Products': T_Products,
                               'RECENT_Products': R_Products})
            else:
                same_cate_products = []
                flag = 0
                for product in ProductModel.objects.all():
                    if search_cate in product.categories:
                        same_cate_products.append([product, product.search_value, product.created_at])
                        flag = 1
                if flag != 1:
                    return render(request, 'home/main.html',
                                  {'TOP_Products': T_Products, 'RECENT_Products': R_Products, 'first': first})
                # 카테고리 검색 시 오류, 수정필요
                T_Products = [
                    [p for p, _, _ in sorted(same_cate_products, key=lambda x: x[1], reverse=True)][i * 5:i * 5 + 5] for
                    i in range(4)]
                R_Products = [
                    [p for p, _, _ in sorted(same_cate_products, key=lambda x: x[2], reverse=True)][i * 5:i * 5 + 5] for
                    i in range(4)]
                return render(request, 'home/main.html',
                              {'TOP_Products': T_Products, 'RECENT_Products': R_Products, 'first': first})