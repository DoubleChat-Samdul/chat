# chat
팀프로젝트2를 위해 개발한 Kafka 서버를 경유하는 채팅 기능입니다.

### Usage
```bash
$ python <REPOSITORY_PATH>/src/chat/chat2.py
```
```
Input chatroom name:<CHATROOM>
Input username:     <USERNAME>
```

위 방식으로 채팅방에 접속할 수 있습니다. 동일한 `<CHATROOM>`을 입력한 서로 다른 `<USERNAME>` 유저들은 실시간 채팅이 가능하게 됩니다.

채팅방은 별도의 윈도우에서 열리게 되며, 해당 윈도우의 하단 3줄은 입력을 받는 `lowerwin`, 나머지는 서버가 메시지를 출력하는 `upperwin`로 구별됩니다.
사용자는 `YOU:` 프롬프트를 통해 `lowerwin`과 `uppwerin`을 구별할 수 있으며, 해당 프롬프트를 통해 입력한 메시지는 서버로 전송돼 `upperwin`에 닉네임과 함께 출력됩니다.


채팅에서 접속을 종료하고 싶으면 `exit`을 입력하면 되며, 이 경우 서버는 해당 사용자가 접속을 종료했음을 채팅방에 알리게 됩니다.

예시:

![스크린샷 2024-08-26 105436](https://github.com/user-attachments/assets/5a86319c-7eac-48cd-975a-8ac677b8fdbb) ![스크린샷 2024-08-26 105436 - 복사본](https://github.com/user-attachments/assets/a47edae4-b1c5-4941-90fc-4490469a2ff1)


```
YOU: exit
```
```
User [<USERNAME>] has exited the chatroom.
Type in 'exit' to also finish the chat.
```

예시:

본 채팅은 영어와 한국어 채팅을 지원합니다.

### Functionalities - Plan

- [x] v0.2.: 기본적인 채팅 및 input/output 윈도우 분리 기능
- [ ] v0.3.: zepplin과의 연계를 통한 채팅 통계 및 감사 기능
- [ ] v0.4.: Airflow를 통해 구축된 영화 데이터베이스를 바탕으로 요청받은 질문에 대한 답을 돌려주는 챗봇 기능
- [ ] v0.5.: Airflow Task 완료 시 메시지를 사용자에게 알려주는 알림 기능
- [ ] v0.6.: 사용자가 설정한 일정을 지정 시간대에 알려주는 일정 기능 

### Release Changelog
- v0.2.0: python `curses` 라이브러리를 통해, 채팅방에 접속했을 경우 창을 위쪽의 upperwin, 아래쪽의 lowerwin으로 나뉘어 각각 출력/입력을 담당하도록 구현하였습니다.

