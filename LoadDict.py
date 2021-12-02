import pandas as pd

def load_dictionary():
    df_stop = pd.read_csv('./data/불용어사전.csv', encoding='utf-8-sig',names=['불용어']) 
    df_pos =  pd.read_csv('./data/긍정어사전.csv', encoding='utf-8-sig',names=['긍정']) 
    df_neg =  pd.read_csv('./data/부정어사전.csv', encoding='utf-8-sig',names=['부정']) 
    stopwords = df_stop['불용어'].to_list()
    return stopwords , df_pos, df_neg

