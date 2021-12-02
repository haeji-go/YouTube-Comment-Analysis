from nltk import Text
from wordcloud import WordCloud
from collections import Counter
import pandas as pd




def word_counts(df_list):

  word_list = sum(df_list, [])
  df_word = pd.DataFrame(Counter(word_list).most_common(), columns = ['word', 'count'])
  return df_word.head(150)

