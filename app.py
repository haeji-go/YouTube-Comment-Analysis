from flask import Flask, render_template, request, redirect, flash
from TextPreprocessing import text_process, text_token, textprocessing_for_newcmt
from WordCloud import word_counts
from LDA import LDA
import pandas as pd
import numpy as np
import time
import json
from CrawlingData import crawling_comments, url_id_parsing
from SentimentAnalysis import sentiment_analysis, compute_ratio,filter_senti
from LoadDict import load_dictionary
from YoutubeInfo_Crawling import ch_img, ytb_information
from RcmdChannel import feature_vector
import re
from datetime import datetime
app = Flask(__name__)
app.run(debug=True)

app.config.update(
    DEBUG=True,
    SECRET_KEY="secret123456"
)

# global 변수 선언
df=pd.DataFrame()
df_sen = pd.DataFrame()
df_prc = pd.DataFrame()
ytb_img=""
ytb_title=""
value=""
dict_wc = []
ratio_neu=0
ratio_pos=0
ratio_neg =0
dict_wc_pst=[]
dict_wc_ngt=[]
dict_wc_nut=[]
lda_json_name = ""
json_data ={}
newcmt=""
ch_id_list=[]
img_name_list=[]
ch_name_list=[]
ch_url_list=[]
stopwords , pos, neg = load_dictionary()
rating_value=0
rating_df = pd.DataFrame()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/loading', methods=["POST"])
def loading():
    global value
    value = request.form['keyword']
    hangeul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    if(value != ""): #키워드로 텍스트가 입력된 경우
        if (hangeul.sub("", value)==""):
            return render_template('loading.html', prg_text="댓글 수집중..", url_value=1 )
        else:
            flash(' 영상의 url을 확인해주세요. (영어+숫자 url) ')
            return redirect('/')
    
    else:# 입력이 안된 경우
        flash(' 영상의 url을 입력해주세요. ')
        return redirect('/')
    
    
    

@app.route('/loading_step1', methods=["POST"])
def loading_step1():
    global df, ytb_title, ytb_img, value
    df = crawling_comments(value)
    if df.shape[0] < 300:
        flash(' 댓글이 300개이상인 영상으로 입력해주세요. ')
        return redirect('/')
    
    ytb_title, ytb_img = ytb_information(value)
    return render_template('loading.html', prg_text="댓글 전처리중..", url_value=2 )

@app.route('/loading_step2', methods=["POST"])
def loading_step2():
    global df, df_sen, df_prc
    df_sen, df_prc = text_process(df)
    return render_template('loading.html', prg_text="워드클라우드 분석중.." , url_value=3)

@app.route('/loading_step3', methods=["POST"])
def loading_step3():
    global df_prc, dict_wc
    dict_wc = makeWordcloud(df_prc)
    return render_template('loading.html', prg_text="감성 분석중.." , url_value=4)

@app.route('/loading_step4', methods=["POST"])
def loading_step4():
    global df_sen,ratio_neu, ratio_pos, ratio_neg, dict_wc_pst, dict_wc_ngt, dict_wc_nut
    df_sen = sentiment_analysis(df_sen)
    df_sen.to_csv('data/df_sen.csv', encoding='utf-8-sig')
    ratio_neu, ratio_pos, ratio_neg=compute_ratio(df_sen)
    wc_word_by_senti()
    return render_template('loading.html', prg_text="클러스터링 분석중.." , url_value=5)

@app.route('/loading_step5', methods=["POST"])
def loading_step5():
    global lda_json_name, json_data
    lda_json_name= LDA(df_prc, sub_title="")
    if lda_json_name !='':
        time.sleep(5)
        with open(lda_json_name, 'r') as f:
            json_data = json.load(f)    
        return render_template('loading.html', prg_text="페이지 로딩중.." , url_value=6)

    else:
        return print("Error")

@app.route('/Analysis-Result', methods=["POST"])
def Analysis_Result():
    global ytb_title, ytb_img, value, json_data, dict_wc, ratio_neu, ratio_pos, ratio_neg, dict_wc_pst, dict_wc_ngt, dict_wc_nut,  ytb_title, value
    return render_template('Datavis-Design.html',ytb_img="image/"+ytb_img, ldavis_json = json_data,  dict_wc = dict_wc, ratio_neu=ratio_neu, ratio_pos=ratio_pos, ratio_neg=ratio_neg, dict_wc_pst = dict_wc_pst, dict_wc_ngt=dict_wc_ngt, dict_wc_nut=dict_wc_nut, ytb_title = ytb_title, ytb_url=value)
            
@app.route('/service-info.html')
def service_info():
    return render_template('service-info.html')


@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(405)
@app.route('/error')
def page_not_found(error):
    return render_template('error.html')


def makeWordcloud(df):
    df_wc = word_counts(df['댓글'].to_list())
    dict_wc=dataframe_to_dict(df_wc, df_wc.columns)
    return dict_wc

def dataframe_to_dict(df, columns):
    result_list = []
    n = len(columns)
    for i in range(df.shape[0]):
        tmp_dict= {}
        for j in range(n):
            if str.isdigit(str(df.iloc[i, j])):
                tmp_dict[columns[j]]=int(df.iloc[i, j])
            else:
                tmp_dict[columns[j]]=df.iloc[i, j]
        result_list.append(tmp_dict)
    return result_list

def wc_word_by_senti():
    global dict_wc, dict_wc_pst, dict_wc_ngt, dict_wc_nut, pos, neg
    for i in range(len(dict_wc)):
        w = dict_wc[i]['word']
        if w in pos['긍정'].to_list():
            dict_wc_pst.append(dict_wc[i])
        elif w in neg['부정'].to_list():
            dict_wc_ngt.append(dict_wc[i])
        else :
            dict_wc_nut.append(dict_wc[i])


## 채널 추천 관련 코드 ##
@app.route('/chRecmd_step1', methods=["POST"])
def chRecmd_step1():
    global newcmt
    newcmt = request.form['keyword']
    
    return render_template('loading_ch.html', prg_text="새로 입력한 댓글 전처리 중.." , url_value=2)


@app.route('/chRecmd_step2', methods=["POST"])
def chRecmd_step2():
    global newcmt
    newcmt = textprocessing_for_newcmt(newcmt)
    return render_template('loading_ch.html', prg_text="채널 추천을 위한 분석 중..." , url_value=3)


@app.route('/chRecmd_step3', methods=["POST"])
def chRecmd_step3():
    global newcmt, ch_id_list
    df_sen = pd.read_csv('data/df_sen.csv', encoding='utf-8-sig')
    neighbors = 6
    ch_id_list = feature_vector(df_sen, newcmt, neighbors)
    return render_template('loading_ch.html', prg_text="추천 채널의 정보 가져오는 중..." , url_value=4)


@app.route('/Channel-Recommendation', methods=["POST"])
def chRecmd_step4():
    global newcmt, ch_id_list, img_name_list, ch_name_list, ch_url_list, rating_value, rating_df
    img_name_list, ch_name_list, ch_url_list =ch_img(ch_id_list)
    rating_df=pd.read_csv('data/ratings.csv', encoding='utf-8-sig')
    
    rating_value=round(rating_df['Ratings'].sum() / rating_df.shape[0] , 1)
    
    if len(ch_name_list) <5 :
        index = len(ch_name_list) 
        for i in range(index, 5, 1):
            img_name_list.append("image/no_recmd_ch.png")
            ch_name_list.append("추천채널 없음")
            ch_url_list.append("")
    return render_template('chRcmdResult.html', img_name_list=img_name_list, ch_name_list= ch_name_list, ch_url_list=ch_url_list, rating_value=rating_value)

# 채널추천 평가 완료한 경우
@app.route('/Channel-Recommendation-rating-submit', methods=["POST"])
def rating_submit():
    global rating_value, newcmt, value, rating_df, ch_id_list, img_name_list, ch_name_list, ch_url_list, rating_value, rating_df
    new_rating = int(request.form['rating_data'])
    new_data={'Datetime':datetime.today(),'YoutubeID':value, "Comments":newcmt, "Ratings":new_rating} #새로 평가된 점수 및 정보 저장
    rating_df=rating_df.append(new_data, ignore_index=True)
    rating_df.to_csv('data/ratings.csv', index=False, encoding='utf-8-sig')
    rating_value=round(rating_df['Ratings'].sum() / rating_df.shape[0] , 1) # 평균평점 업데이트
    return render_template('chRcmdResult_submit.html', img_name_list=img_name_list, ch_name_list= ch_name_list, ch_url_list=ch_url_list, rating_value=rating_value)
    
