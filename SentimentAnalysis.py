
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

from LoadDict import load_dictionary
stopwords , pos, neg = load_dictionary()

#df=text_process(df, False)
def sentiment_analysis(df):
    df_sen = df.copy()
    df_sen['score'] = 0
    df_sen['score_label'] = 0

    for i in df_sen.index:
        sentence = df_sen['댓글'][i]
        val = 0
        for j in range(len(pos)):
            if pos['긍정'][j] in sentence:
                val += 1
        for k in range(len(neg)):
            if neg['부정'][k] in sentence:
                val -= 1
    
        df_sen['score'][i] = val
        if val > 0:
            df_sen['score_label'][i] = 1 # 긍정
        elif val < 0:
            df_sen['score_label'][i] = -1 # 부정
        else:
            df_sen['score_label'][i] = 0

    return df_sen

def compute_ratio(df):
    total = df.shape[0]
    try:
        ratio_neu =df['score_label'].value_counts()[0] / total
    except:
        ratio_neu=0
        
    try:
        ratio_pos =df['score_label'].value_counts()[1] / total
    except:
        ratio_pos=0
    
    try:
        ratio_neg =df['score_label'].value_counts()[-1] / total
    except:
        ratio_neg=0
    
    
    
    return ratio_neu, ratio_pos , ratio_neg
    #return pd.DataFrame([ratio_neu, ratio_pos, ratio_neg], columns=['value'])


def filter_senti(df_sen, n):
    return df_sen[df_sen['score_label']==n]

def sentiment_analysis_one(new_cmt):
    val = 0
    for j in range(len(pos)):
        if pos['긍정'][j] in new_cmt:
            val+=1
    for k in range(len(neg)):
        if neg['부정'][k] in new_cmt:
            val-=1
    
    if val>0:
        return 1
    elif val<0:
        return -1
    else:
        return 0