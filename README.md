# DoucleChat
## ◆ Introduction
팀프로젝트2를 위해 `DoubleChat-Samdul` 조가 개발한 Kafka 서버를 경유하는 채팅 어플리케이션입니다.

## ◆ Usage
※ 본 항목에서 `<MY_REPOSITORY_PATH>`는 해당 레포지토리를 클론한 경로를 뜻합니다.

### 1. Chat Basics
```bash
$ python <MY_REPOSITORY_PATH>/src/chat/chat2.py
```
```
Input chatroom name:<CHATROOM>
Input username:     <USERNAME>
```

위 방식으로 채팅방에 접속할 수 있습니다. 동일한 `<CHATROOM>`을 입력한 서로 다른 `<USERNAME>`의 유저들은 실시간 채팅이 가능하게 됩니다.

채팅방은 별도의 윈도우에서 열리게 되며, 해당 윈도우의 하단 3줄은 입력을 받는 `lowerwin`, 나머지는 서버가 메시지를 출력하는 `upperwin`로 구별됩니다.
사용자는 `YOU:` 프롬프트를 통해 `lowerwin`과 `uppwerin`을 구별할 수 있으며, 해당 프롬프트를 통해 입력한 메시지는 서버로 전송돼 `upperwin`에 닉네임과 함께 출력됩니다.


채팅에서 접속을 종료하고 싶으면 `exit`을 입력하면 되며, 이 경우 서버는 해당 사용자가 접속을 종료했음을 채팅방에 알리게 됩니다.

```
YOU: exit
```
```
User [<USERNAME>] has exited the chatroom.
Type in 'exit' to also finish the chat.
```

두 유저간 채팅 예시:

![스크린샷 2024-08-26 105436 - 복사본](https://github.com/user-attachments/assets/46a5059f-7149-416a-b891-1eccf1ead505) ![스크린샷 2024-08-26 105436](https://github.com/user-attachments/assets/5a86319c-7eac-48cd-975a-8ac677b8fdbb)

### 2. movchatbot
채팅에서 `@bot` 또는 `@봇` 키워드로 질문 프롬프트를 입력했을 때, 영화목록 데이터베이스에서 검색하여 질문에 대한 답을 돌려주는 챗봇 기능입니다.

![image](https://github.com/user-attachments/assets/d897bb0c-4306-42bf-ad7f-29957ef143c2) 

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


### 3. Chat Auditor
채팅 이용자 메시지 로그 데이터 수집을 통한 감사 기능입니다.
본 기능은 [DoubleChat-Samdul/Airflow](https://github.com/DoubleChat-Samdul/airflow/tree/0.2.0/audit) 레포지토리의 기능과 연동되는 구조이므로, 사용을 위해 해당 모듈도 필요합니다.
해당 레포지토리의 README 또한 참조해 주시기 바랍니다.

본 기능은 `AUDIT_PATH`라는 셸 환경변수에 로그 데이터를 수집할 경로를 저장하고 있습니다.

따라서, 다음과 같이 사용중인 셸의 설정 파일 (`~/.bashrc`, `~/.zshrc`, ...)에 환경변수를 추가하면 됩니다.
```bash
$ tail -3 ~/.zshrc

# AUDIT_PATH
export AUDIT_PATH =<MY_PATH>
```

`<MY_PATH>`는 사용자가 직접 지정하면 되는 경로입니다. 실제로 로그 파일이 저장될 위치입니다.

해당 기능은 자동적으로 Kafka 서버의 채팅 로그를 가져와 지정된 경로에 저장하며, 여기에 포함된 데이터는 다음과 같습니다.
- `sender`: 메시지의 전송자
- `message`: 전송된 메시지
- `end`: 해당 메시지가 채팅을 종료하는 커맨드였는지의 여부
- `timestamp`: 해당 메시지가 전송된 시/분 시각 정보

해당 데이터를 활용하여 얻을 수 있는 통계 정보는 다음과 같은 것들이 있습니다. 
- `user count`: 해당 전송자가 몇 개의 채팅을 전송하였는지에 대한 정보
- `word count`: 해당 단어가 몇 번 사용되었는지에 대한 정보
- `time count`: 해당 시,분에 몇 개의 채팅이 전송되었는지에 대한 정보

### ◇ Audit module
- `audit.py` DAG: 감사를 위한 데이터 수집 작업은 1시간 마다 스케줄링되어 이루어지며, 이 과정은 `Spark`를 활용하여 분산 처리함
- `offset.txt`: 전송된 메시지의 누수를 방지하고, 데이터 추출의 효율성을 확보하기 위하여 Kafka UI를 통해 확인가능한 `offset` 정보를 저장하여 관리
- `message_audit`: Kafka에서 가져온 데이터를 spark의 데이터 프레임 형식으로 변환한 후, 해당 경로에 parquet 형식으로 누적해서 저장


## ◆ Update Changelog
- `v0.2.0`
: python `curses` 라이브러리를 통해, 채팅방에 접속했을 경우 창을 위쪽의 upperwin, 아래쪽의 lowerwin으로 나눠 각각 입/출력을 담당하게 하는 채팅 기능을 완성하였습니다.
- `v0.2.1` → `v0.2.2`
: 
- `v0.3.0`
: 
: 또한, `utf-8` 인코딩/디코딩 과정에서 빈번하게 발생하는 한글/영문 입력의 `UnicodeError`를 캐치하는 에러 핸들링 구문을 추가했습니다.
 

## ◆ Mechanics

초기 구현시에는 파이썬의 기본 `input()` 및 `print()` 함수, 그리고 `thread` 모듈을 통한 스레딩으로 채팅의 입/출력이 한 윈도우에서 동시에 이뤄지도록 채팅방을 구현했습니다. 그러나 실제로 입력을 받기 전까지 구문을 계속 열어 놓는  `input()` 함수의 특성으로 인해 입출력 병렬 운용이 구현되었어도 입력과 출력이 1:1 비율로 이뤄지지 않는다면 입력구문의 프롬프트가 출력 구문으로 계속 '밀리는'  시각적 혼선 문제가 있었습니다.

이를 해결하기 위해 실제 다양한 채팅 어플리케이션과 같이 입력 윈도우를 출력 윈도우와 분리해 개발하자는 의견이 나와, 조사 후 파이썬 기본 라이브러리의 `curses` 모듈을 통해 CLI에서의 창 분리를 구현하기로 했습니다.

본 어플리케이션은 따라서 `curses` 모듈을 통해 `upperwin`과 `lowerwin`을 분리해 전자가 출력을, 후자가 입력을 담당하도록 제작되었습니다.
