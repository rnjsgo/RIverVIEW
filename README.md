# RiverVIEW

<div align="left">
<img width="232" alt="스크린샷 2023-02-26 오후 5 52 05" src="https://user-images.githubusercontent.com/102651155/221401212-98989154-8f7b-47c6-bf6c-ce10ec30e075.png">

</div>


> **전남대학교 컴퓨터정보통신공학과 캡스톤디자인과목** <br/> **개발기간: 2022.10 ~ 2022.12**


## 프로젝트 참여

|      권 해      |          허현준         |                                                                                                             
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: 
| 전남대학교 컴퓨터정보통신공학과 3학년 | 전남대학교 컴퓨터정보통신공학과 3학년 
|자료 조사 및 데이터 수집(공통)<br>서버 구축<br>Web UI 구현<br>데이터 크롤링|자료 조사 및 데이터 수집(공통)<br>Word Embedding 작업<br>리뷰 데이터 분석 모델링|


## 프로젝트 소개

 최근, 합리적 소비를 추구하는 일명 ‘스마트 컨슈머’가 늘어남에 따라, 이들에게 상품 가치 판단에 있어서 상품 리뷰 데이터의 중요성이 증가하고 있다. <br>
 기존의 리뷰 분석 서비스는 데이터 단순 처리를 통한 통계, 혹은 요약 정보만을 제공하기 때문에, 구매 예정자가 상품 구매를 판단하기에 다소 어려움이 있다. <br>
 본 서비스는 "Ai Score"과 같은 구매 판단에 도움이 될 수 있는 정보들을 제공함으로써, 보다 높은 수준의 상품 리뷰 분석 서비스를 제공하고자 한다.<br>

상품에 대한 리뷰 분석 결과는 “Ai Score“, “키워드 별 만족도”, ”Best/Worst Top3”, ”리뷰 워드 클라우드”, 총 4가지로 구분되어 출력된다.<br>
수집한 리뷰 데이터를 분석하는 과정에서 유사 단어 처리를 위한 워드임베딩 기법으로 “word2Vec”을 사용하였고, <br>
리뷰 문장에 대한 감성 분석은 “GRU” 모델을 사용한다. <br>
인공지능 모델의 학습 데이터는 네이버 쇼핑몰 리뷰 20만건을 사용한다.(https://github.com/bab2min/corpus/tree/master/sentiment)


## Stacks 🐈

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![PyCharm](https://img.shields.io/badge/PyCharm-000000?style=for-the-badge&logo=PyCharm&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=SQLite&logoColor=white)
<br>
![Jupyter](https://img.shields.io/badge/JupyterNotebook-F37626?style=for-the-badge&logo=Jupyter&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![GoogleMeet](https://img.shields.io/badge/GoogleMeet-00897B?style=for-the-badge&logo=Google%20Meet&logoColor=white)

---
## 화면 구성 📺
| 상품 URL 입력 페이지  |  상품 총평   |
| :-------------------------------------------: | :------------: |
|  <img width="329" src="https://user-images.githubusercontent.com/102651155/221402341-2faec234-309b-4e61-897d-a098b2486dd9.png"/> |  <img width="329" src="https://user-images.githubusercontent.com/102651155/221402379-1bf11e63-db08-471a-9b08-1699d8620f87.png"/>|  
| 리뷰 분석 1  |  리뷰 분석 2   |  
| <img width="329" src="https://user-images.githubusercontent.com/102651155/221402436-81f0b9dd-b868-4e92-ad71-28b41cb2e844.png"/>   |  <img width="329" src="https://user-images.githubusercontent.com/102651155/221402498-605fa72e-09f4-4ed8-95da-a082a6781f5c.png"/>     |

### 시연 영상(아래 이미지 클릭)
[![시연 영상](https://user-images.githubusercontent.com/102651155/221402341-2faec234-309b-4e61-897d-a098b2486dd9.png)](https://youtu.be/KApzqT6FATQ)
---
## 주요 기능 📦

### ⭐️ 키워드별 만족도 분석 
상품 리뷰 데이터를 분석하여, 전체 리뷰의 핵심 키워드 몇가지를 빈도수 순서에 따라 추출한다. 추출한 키워드에 대한 전체적인 리뷰 감성을 종합하여, 만족도 수치를 그래프와 같은 자료로 시각화한다. 예들 들어, 추출한 키워드 중 하나가 ‘배송’ 이라고 하면 ‘배송’ 키워드에 대한 만족도를 그래프로 나타낸다.

### ⭐️ Best/Worst Top3 
키워드 별 만족도가 가장 높은 키워드, 만족도가 가장 낮은 키워드 각각 3가지를 그에 따른 예시 리뷰와 함께 보여줌으로써, 상품에 대한 추천 요소와 다시 생각해 볼 요소에 대한 정보를 제공한다.

### ⭐️ AI Score 
전체 리뷰와 키워드별 만족도를 기반으로, 상품에 대한 종합 점수를 산출하여 제공한다. 

### ⭐️ 리뷰 워드 클라우드 

단어 별 빈도수를 시각화 하여 리뷰 데이터 전체의 내용을 직관적으로 파악할 수 있도록 한다.

---
## 아키텍쳐

### 시퀀스 다이어그램
<img width="420" alt="image" src="https://user-images.githubusercontent.com/102651155/221402770-631269ee-7e85-4538-ad10-d483217e4a9a.png">

### 클래스 다이어그램
<img width="420" alt="image" src="https://user-images.githubusercontent.com/102651155/221402790-51e39106-0564-421f-bc5a-8345cf04a0ef.png">

---
## 구현 방식 📦

### (1) 상품 페이지 URL이 입력으로 들어옴 -> 해당 리뷰 페이지 크롤링 -> 상품 리뷰, 정보 등 추출 <br>
### (2) 상품정보와 리뷰를 이용하여 키워드 추출<br>
•	KR-WordRank 알고리즘을 통해 모든 리뷰에서 키워드 추출<br>
•	모든 리뷰를 형태소 분석기로 토큰화<br>
•	word2Vec과 TF-IDF모델 생성 후 학습<br>
•	word2Vec에 없는 단어 제외, 불용어 제외, TF-IDF로 중요하지 않은 단어 제외<br>
->자주 사용되면서 의미가 있는 키워드 추출 성공<br>
### (3) 키워드별 만족도 계산<br>
•	GRU모델을 통해 리뷰 데이터에 대한 감성 분석 (감성 분석 1회 실행 시 소요시간 약 0.3초)<br>
•	코사인 유사도가 0.9이상인 단어에 대해서도 해당 키워드에 대한 만족도에 반영<br>
•	키워드 만족도 = 해당 키워드에 대한 모든 리뷰 점수의 합 / 해당 키워드 빈도수<br>
### (4) 키워드별 만족도를 기반으로 실제 리뷰 추출
•	해당 키워드가 포함된 리뷰들을 리뷰 점수에 기반하여 긍정 리뷰, 부정 리뷰 판별<br>
•	해당 키워드 만족도와 같은 감성을 가진 리뷰를 추출(‘배송’ 키워드 감성: 긍정, 추출한 실제 리뷰 감성: 긍정 이어야 추출성공)<br>
### (5) AI score 계산 = (해당 키워드 만족도*키워드 리뷰 수/모든 키워드 리뷰 수…모든 키워드에 대해 계산하여 더해줌} /100<br>
### (6) DB에 결과(키워드, 만족도, AI Score 등)를 저장하여 사용자에게 웹페이지 전달<br>

