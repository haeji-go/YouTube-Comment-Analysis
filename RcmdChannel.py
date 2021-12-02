import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from SentimentAnalysis import sentiment_analysis, sentiment_analysis_one
from CrawlingData import crawling_subscriptions, get_subscriptions

def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm     
    
    return similarity


def feature_vector(df, new_cmt, neighbors):
    # 댓글 values를 1차원 list로 변환
    sen_list = df['댓글'].values.tolist()
    sen_list = np.ravel(sen_list)
    sen_list = sen_list.tolist()

    # 임시 문장을 댓글 list에 추가
    sen_list.append(new_cmt)

    # 유사도 분석을 위한 matrix 정의
    tfidf_vect_simple = TfidfVectorizer(min_df=1)
    feature_vect_simple= tfidf_vect_simple.fit_transform(sen_list)
    
    # TFidfVectorizer로 transform()한 결과는 Sparse Matrix이므로 Dense Matrix로 변환. 
    feature_vect_dense = feature_vect_simple.todense()

    #첫번째 문장과 두번째 문장의 feature vector  추출
    vect1 = np.array(feature_vect_dense[0]).reshape(-1,)
    vect2 = np.array(feature_vect_dense[1]).reshape(-1,)

    #첫번째 문장과 두번째 문장의 feature vector로 두개 문장의 Cosine 유사도 추출
    similarity_simple = cos_similarity(vect1, vect2)
    # 유사도 matrix 계산
    similarity_simple_pair = cosine_similarity(feature_vect_simple , feature_vect_simple)
    # 유사도 분석 결과를 list에 저장

    analysis_result = []
    for i in similarity_simple_pair[similarity_simple_pair.shape[0]-1]:
        analysis_result.append(i)
    analysis_result.pop(similarity_simple_pair.shape[0]-1)

    df['유사도'] = analysis_result
    newcmt_score_label = sentiment_analysis_one(new_cmt)
    
    df['가중_유사도']=0.0
    #입력 댓글 긍정인 경우
    if newcmt_score_label==1:
        for i in df.index:
            if df['score_label'][i]==1:
                df['가중_유사도'][i]=df['유사도'][i] * 2.0
            elif df['score_label'][i]==-1:
                df['가중_유사도'][i]=df['유사도'][i] * 0.5
            else:
                df['가중_유사도'][i]=df['유사도'][i]
                

    #입력 댓글 중립인 경우
    elif newcmt_score_label==0:
        for i in df.index:
            if df['score_label'][i]==0:
                df['가중_유사도'][i]= df['유사도'][i] * 2.0
            else:
                df['가중_유사도'][i]=df['유사도'][i]
                
    #입력 댓글 부정인 경우
    else:
        for i in df.index:
            if df['score_label'][i]==-1:
                df['가중_유사도'][i]=df['유사도'][i] * 2.0
            elif df['score_label'][i]==1:
                df['가중_유사도'][i]=df['유사도'][i] * 0.5
            else:
                df['가중_유사도'][i]=df['유사도'][i]
    
    df_order = df.sort_values(by='가중_유사도', ascending=False)

    df_subscription, df_sim=crawling_subscriptions(df_order, neighbors)
    df_subscription ['score'] = 1
    user_subscription = df_subscription.pivot_table('score', index='authorId', columns='sub_channelId').fillna(0)
    user_subscription_sim = user_subscription.T
    
    for i in df_sim.index:
        #유사도
        sim = df_sim.loc[i, '가중_유사도']
        user_subscription_sim.loc[:, df_sim.loc[i,'작성자id']] = sim * user_subscription.T.loc[:, df_sim.loc[i,'작성자id']]
    user_subscription_sim = user_subscription_sim.T
    df_recomd = user_subscription_sim.sum().sort_values(ascending=False).reset_index()
    
    df_recomd.columns=['channelID', 'score']

    return df_recomd['channelID'].to_list()