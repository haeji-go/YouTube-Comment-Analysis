import gensim
from gensim import corpora
import pyLDAvis.gensim_models
from flask import render_template

# 사용 : LDA(df)

# 정수인코딩과 단어집합 만들기
def encoding_make_dic(df):
  dictionary = corpora.Dictionary(df['댓글'])
  #dictionary.filter_extremes(no_below=10) ## 빈도수가 10이상인 것만 보고싶을 때
  corpus = [dictionary.doc2bow(row) for row in df['댓글']]
  return dictionary, corpus

def LDA(df,sub_title='0' ,epochs=10, num_topics=3):
  dictionary, corpus = encoding_make_dic(df)
  lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=epochs) #passes(epoch)
  vis =  pyLDAvis.gensim_models.prepare(lda, corpus, dictionary) 
  pyLDAvis.save_json(vis, './visLDA'+sub_title+'.json')
  return './visLDA'+sub_title+'.json'