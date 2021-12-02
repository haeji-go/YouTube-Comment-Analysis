from bs4 import BeautifulSoup
import requests
import urllib.request
import time
from CrawlingData import url_id_parsing
'''
채널 추천 결과 : ch_id_list
--> 각 채널 이미지 수집 : ch_img() 
'''

## 유튜브 영상의 제목, 썸네일 수집 및 저장
def ytb_information(ytb_url):
    response = requests.get(ytb_url)
    img_name = url_id_parsing(ytb_url)+".jpg"
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('div', {'class':'watch-main-col'}).find('meta', {'itemprop':'name'})['content']
    img_url= soup.find('span', {'itemprop':'thumbnail'}).find('link')['href']
    download_img(img_url, img_name)
    return title, img_name

## 유튜브 채널의 이미지 수집 & 저장
def ch_img(id_list):
    img_name_list = []
    ch_name_list = []
    ch_url_list=[]
    for n, id in enumerate(id_list):
        ch_url = 'https://www.youtube.com/channel/'+id
        response = requests.get(ch_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        ch_img_url = soup.find('meta', {'property':'og:image'})['content']
        ch_name = soup.find('span', {'itemprop':'author'}).find('link', {'itemprop':'name'})['content']
        img_name = id+".jpg"
        img_name_list.append("image/"+img_name)
        ch_name_list.append(ch_name)
        ch_url_list.append(ch_url)
        download_img(ch_img_url, img_name)
        time.sleep(1.2)
    return img_name_list, ch_name_list, ch_url_list

## 이미지 url로 부터 다운로드
def download_img(url, title):
    urllib.request.urlretrieve(url, './static/image/'+title)