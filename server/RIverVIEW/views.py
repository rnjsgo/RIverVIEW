from django.shortcuts import render, redirect
from .models import ProductModel,  ProductKeyword
from RIverVIEW.MakeData.functions import *
from RIverVIEW.MakeData.make_data import *
from RIverVIEW.MakeData.time_check import *
def foward_home(request):
    if request.method == 'GET':
        return render(request, 'RIverVIEW/main.html')

def view_details(request, product_num):
    product = ProductModel.objects.get(product_num= product_num)
    result_keyword=[]
    pos_keyword = []
    neg_keyword = []
    keywords = {}
    result_keyword_cnt=0
    whole_review=0
    ai_score=0
    # 해당 상품의 키워드 처리
    for keyword in ProductKeyword.objects.filter(product_reference_id= product_num):
        
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

    make_wordcloud(keywords, str(product_num))

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
            T_DEBUG = 1
            t = time_chk('크롤링 시작', T_DEBUG)
            st = t.start()
            #url 분리해서 상품번호 따오기
            product_num = url.split('/')[-1].split('?')[0]
            #시작전 db 초기화
            ProductKeyword.objects.filter(product_reference_id=int(product_num)).delete()
            ProductModel.objects.filter(product_num=int(product_num)).delete()

            #url 비어있을 때
            if url == '':
                return render(request, 'RIverVIEW/main.html')

            else:
                if 'naver' in url:
                    temp,url,product_name,img_src=start_crawling(product_num, url)
                    t.eend(st,t.end())
                    product=ProductModel(product_url=url,
                                         product_name=product_name,
                                         product_num=int(product_num),
                                         img_src=img_src)
                    product.save()
                    keyword, keyword_example, key_score, key_freq = make_final_data(total_data=temp, col_name='review',
                                                                                    limit_size=250, product_name=product_name, T_DEBUG=1)
                    for word in keyword:
                        productKeyword=ProductKeyword(product_reference_id=int(product_num),
                                                      keyword=word,
                                                      review=keyword_example[word]['original_review'],
                                                      keyword_score=round(key_score[word],1),
                                                      keyword_frequency=key_freq[word]
                                                      )
                        productKeyword.save()
                    return redirect('/details/{}/'.format(product_num))

                else:
                    return render(request, 'RIverVIEW/main.html',  {'first': first})



