# movchatbot
채팅에서 @bot <영화이름> | <감독, 장르, 제작년도> 형식으로 질문 했을 때, 영화목록 데이터베이스에서 검색하여 질문에 대한 답을 돌려주는 챗봇 기능 

### Usage

```bash
@bot <영화이름> | <감독, 장르, 제작년도>
```

채팅메세지를 다음과 형식으로 작성하면 @bot이 질문으로 인식하여 채팅메세지로 답변합니다.

채팅을 주고받다가, @bot 키워드를 포함하여 채팅을 작성하면 질문으로 인식합니다.  
따라서  <영화이름> | <감독, 장르, 제작년도> 형식으로만 입력받으며, 그 외의 경우 올바른 형식으로 작성하라는 메세지와 함께 재입력 받습니다.
