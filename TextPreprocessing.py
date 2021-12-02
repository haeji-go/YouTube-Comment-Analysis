import pandas as pd
import konlpy.tag
okt=konlpy.tag.Okt()
import re
'''
LDA : df_prc
감성분석 :df_sen
WC :df_prc['댓글'].to_list()
'''
# 폰트 파일 경로 
#font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf' 

# 불용어 사전 load
stop= pd.read_csv("./data/불용어사전.csv",names=['불용어'])
stopwords = stop['불용어'].to_list()
#이모티콘 제거
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)

#분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')

#한국어만 남기기
hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')

#특수문자, 의성어제거
def remove_nonwords(df):

    comment_list=[]
    for i in range(len(df['댓글'])):
        comment_list.append(df['댓글'].iloc[i])
        
    comment_result = []
    for i in comment_list:
        tokens = re.sub(emoji_pattern,"",i)
        tokens = re.sub(han,"",tokens)
        tokens = hangul.sub("", tokens)
        comment_result.append(tokens)

    df['댓글'] = comment_result

    return df

# 전처리 후, 글자가 사라지는 행 처리
def remove_empty_row(df):
    df_noempty = df[df['댓글'].str.isspace()==False]
    df_noempty = df_noempty[df_noempty['댓글']!='']
    #df_noempty.reset_index(drop=True)
    return df_noempty

#토큰화
def tokenize_okt(df):
    return pd.DataFrame(df['댓글'].apply(lambda x: okt.morphs(x)))

#불용어제거
def remove_stopwords(stopword_list, row):
    result=[]
    for w in row:
        if w not in stopword_list:
            result.append(w)
    return result

# 한 단어제거
def remove_onewords(row):
    result=[]
    for w in row:
        if len(w) != 1:
            result.append(w)
    return result

def text_process(df):
    df = remove_nonwords(df)
    df = remove_empty_row(df)

    # 감성분석에 사용될 df : df_sen
    df_sen = df

    # 워드클라우드, LDA에 사용될 df : df_prc
    df = tokenize_okt(df)
    df['댓글'] = df['댓글'].apply(lambda row : remove_stopwords(stopwords, row))
    df['댓글'] = df['댓글'].apply(remove_onewords)
    df_prc = df
    return df_sen, df_prc

def text_token(df):
    df = tokenize_okt(df)
    df['댓글'] = df['댓글'].apply(lambda row : remove_stopwords(stopwords, row))
    df['댓글'] = df['댓글'].apply(remove_onewords)
    return df

def textprocessing_for_newcmt(newcmt):
  for i in [newcmt]:
    tokens = re.sub(emoji_pattern,"",i)
    tokens = re.sub(han,"",tokens)
    tokens = hangul.sub("", tokens)

  newcmt = tokens
  return newcmt