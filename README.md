# movchatbot
채팅에서 @bot 키워드로 질문 했을 때, 영화목록 데이터베이스에서 검색하여 질문에 대한 답을 돌려주는 챗봇 기능.  
  
![image](https://github.com/user-attachments/assets/d897bb0c-4306-42bf-ad7f-29957ef143c2) 
## Usage
채팅에서 `@bot` 혹은 `@봇` 키워드를 포함하여 메세지를 작성하면 봇이 질문으로 인식하여 채팅메세지로 답변합니다.   
  
![image](https://github.com/user-attachments/assets/8f006545-ce73-4913-a133-7c2a1e8261c1)  
 
질문으로 인식되게 되면 아래 형식으로만 입력받으며, 그 외의 경우 올바른 형식으로 작성하라는 메세지와 함께 재입력 받습니다.
```bash
@bot <영화이름> | <감독 OR 장르 OR 제작년도> 
```
```bash 
@봇 <영화이름> | <감독 OR 장르 OR 제작년도>
```  
![image](https://github.com/user-attachments/assets/592c066d-5db8-4670-a668-29be32c29e70)  
