# YouTube-Comment-Analysis
YouTube 댓글분석 및 댓글기반의 채널추천 서비스

## 1. 서비스 소개
유튜브 댓글을 실시간으로 수집하여 분석해주는 서비스입니다. 
- 유튜브 영상 url입력만으로 한 눈에 보기 힘든 유튜브 댓글의 분석된 결과를 확인할 수 있습니다.
- 로그인없이 새로운 댓글 작성만으로 새로운 채널을 추천받아 볼 수 있습니다.

해당 서비스는 아래와 같이 크게 두 부분으로 이루어져있습니다.

#### (1) 유튜브 댓글 분석
✔ 키워드 클러스터링 <br>
전체 댓글들을 3개의 주제(토픽)으로 분류하여 토픽의 분포와 해당 토픽별 단어의 분포를 시각화한 분석기법

✔ 감성분석 <br>
전체 댓글에 대하여 긍정, 부정, 중립을 판별하여 그 비율을 도넛차트를 이용하여 시각화

✔ 워드클라우드 <br>
전체 댓글의 키워드를 직관적으로 파악할 수 있도록 비중이 높은 단어를 글자크기와 색을 통해 강조하는 시각화

#### (2) 댓글 분석 기반의 채널 추천
분석한 영상에 대해 새로운 댓글을 입력하면, 기존 댓글과 새로운 댓글을 분석하여 이웃을 선정하고, <br>
해당 이웃의 구독정보를 수집하여 새로운 채널을 추천해줍니다.

## 2. 서비스 이용방법
#### (1) 유튜브 댓글 분석
[step1] 유튜브 영상의 url 복사 <br>
[step2] 복사한 url을 입력 후, 엔터 <br> 
[step3] 분석 결과 확인 <br>
(Tip) step2➜step3 : 댓글 수집 🠖 텍스트 전처리 🠖 텍스트 분석 🠖 분석결과시각화 수행  <br>

#### (2) 댓글 분석 기반의 채널 추천
[step1] 분석 페이지에서 새로운 댓글 입력 후, 엔터  <br>
[step2] 댓글 분석 기반으로 추천된 채널 확인  <br>
(Tip) step1➜step2 : 새로운 댓글과 기존 댓글간의 유사도 계산 🠖 기존 댓글 작성자들의 구독 정보 수집 🠖 추천 알고리즘 수행 <br>
[step3] 추천된 채널에 대해 평가하기 <br>
(Tip) 채널추천에 대한 평균 평점을 확인할 수 있어요! (추천결과 하단에서 확인가능) <br>

## 3. 화면 구성
<table>
  <thead>
    <tr>
      <th> app.py</th>
      <th> URL </th>
      <th> TEMPLATES </th>
      <th> 설명 </th>
     </tr>
  </thead>
  <tbody>
    <tr>
      <td> home </td>
      <td> localhost </td>
      <td> home.html </td>
      <td> 시작 페이지 (url 입력) </td>
    </tr>
    <tr>
      <td> loading_step숫자 </td>
      <td> localhost/loading_step숫자 </td>
      <td> loading.html </td>
      <td> 분석하는동안 로딩 페이지 </td>
    </tr>
    <tr>
      <td> Analysis_Result </td>
      <td> localhost/Analysis-Result</td>
      <td> DataVis-Design.html </td>
      <td> 분석결과 페이지 (새로운 댓글 입력) </td>
    </tr>
    <tr>
      <td> chRecmd_step숫자 </td>
      <td> localhost/chRecmd_step숫자</td>
      <td> loading_ch.html </td>
      <td> 채널추천이 이루어지는 동안 로딩페이지 </td>
    </tr>
    <tr>
      <td> chRecmd </td>
      <td> localhost/Channel-Recommendation</td>
      <td> chRcmdResult.html </td>
      <td> Top5 채널 추천 결과 페이지 </td>
    </tr>
    <tr>
      <td> page_not_found </td>
      <td> localhost/error</td>
      <td> error.html </td>
      <td> 에러발생시 나타나는 페이지 </td>
    </tr>
    <tr>
      <td> service_info </td>
      <td> localhost/service-info</td>
      <td> service-info.html </td>
      <td> 서비스 소개 페이지 </td>
    </tr>
  </tbody>
 </table>
 
(주의) 'localhost/'에서 순서대로 진행하세요! (url로 그냥 접근하는 경우, 오류가 발생할 수 있습니다.)

## 4. 사용된 기술
- python (Flask Framework, YoutubeAPI: googleapiclient.discovery)
- html
- javascript (d3.js)

## 5. 시연 영상
[![유튜브댓글분석 및 채널추천서비스 시연영상](http://img.youtube.com/vi/tvAdpPtTY8Y/0.jpg)](https://youtu.be/tvAdpPtTY8Y?t=0s) 
