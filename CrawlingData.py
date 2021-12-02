from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import time
'''
crwaling_comments("영상id")
get_subscriptions("작성자id",이웃수)
'''
def url_id_parsing(url):
    id=''
    if url.find('watch?v=')>0:
        id=url[32:]
    else:
        id=url[17:]
    return id

def crawling_comments(url): # input : 동영상id
    video_id = url_id_parsing(url)
    api_key='AIzaSyCgy1VjpdFF3DqQwyDV-gwHriZxskM6gQ8'
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorChannelId']['value'], comment['authorDisplayName'], comment['publishedAt']])

            if item['snippet']['totalReplyCount'] > 0:
                if 'replies' in item:
                    for reply_item in item['replies']['comments']:
                        reply = reply_item['snippet']
                        comments.append([reply['textDisplay'], reply['authorChannelId']['value'], reply['authorDisplayName'], reply['publishedAt']])

        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break

    df = pd.DataFrame(comments)
    df.columns = ['댓글','작성자id', '작성자', '작성날짜']

    return df #return : 영상의 댓글 dataframe

def get_subscriptions(authorId): # input : 댓글작성자id
    api_key='AIzaSyCHG_iASY8bvt7_BuX3fy8KXBzcvbRpfxw'
    subscription_list = list()

    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.subscriptions().list(channelId=authorId,  part='snippet,contentDetails',  maxResults=50).execute()

    while response:
        for item in response['items']:
            title = item['snippet']['title']
            channelid = item['snippet']['resourceId']['channelId']
            #print(title, channelid)
 
        subscription_list.append([authorId, channelid, title])
 

        if 'nextPageToken' in response:
            response = api_obj.subscriptions().list(part='snippet,contentDetails', channelId=userId, pageToken=response['nextPageToken'], maxResults=50).execute()
        else:
            break
    
    df = pd.DataFrame(subscription_list)
    df.columns = ['authorId', 'sub_channelId', 'sub_channelTitle']
    return df # 댓글작성자가 구독한 채널 id, 이름 Dataframe

def crawling_subscriptions(df, num_neighbor): #input : 댓글크롤링df(작성자id필수), 이웃 수
    df_subscription = pd.DataFrame(columns=['authorId', 'sub_channelId', 'sub_channelTitle'])
    df_sim = pd.DataFrame() #작성자id, 유사도로 구성된 dataframe
    neighbor_count = 0
    for index, row in df.iterrows():
        if neighbor_count == num_neighbor:
            break

        try:
            df_subscription = pd.concat([df_subscription,get_subscriptions(row['작성자id'])], axis=0)
            neighbor_count += 1
            df_sim= pd.concat([df_sim, df.loc[[index], ['작성자id', '가중_유사도']]], axis=0)

        except:
            continue 
    return df_subscription, df_sim #return : 작성자id, 구독채널id, 구독채널이름 으로 구성된 DataFrame