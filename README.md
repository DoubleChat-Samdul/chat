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

```
YOU: exit
```
```
User [<USERNAME>] has exited the chatroom.
Type in 'exit' to also finish the chat.
```

두 유저간 채팅 예시:

![스크린샷 2024-08-26 105436 - 복사본](https://github.com/user-attachments/assets/46a5059f-7149-416a-b891-1eccf1ead505) ![스크린샷 2024-08-26 105436](https://github.com/user-attachments/assets/5a86319c-7eac-48cd-975a-8ac677b8fdbb)

본 어플리케이션은 영어와 한국어 채팅을 지원합니다.

### Mechanics

초기 구현시에는 파이썬의 기본 `input()` 및 `print()` 함수, 그리고 `thread` 모듈을 통한 스레딩으로 채팅의 입/출력이 한 윈도우에서 동시에 이뤄지도록 채팅방을 구현했습니다. 그러나 실제로 입력을 받기 전까지 구문을 계속 열어 놓는  `input()` 함수의 특성으로 인해 입출력 병렬 운용이 구현되었어도 입력과 출력이 1:1 비율로 이뤄지지 않는다면 입력구문의 프롬프트가 출력 구문으로 계속 '밀리는'  시각적 혼선 문제가 있었습니다.

이를 해결하기 위해 실제 다양한 채팅 어플리케이션과 같이 입력 윈도우를 출력 윈도우와 분리해 개발하자는 의견이 나와, 조사 후 파이썬 기본 라이브러리의 `curses` 모듈을 통해 CLI에서의 창 분리를 구현하기로 했습니다.

본 어플리케이션은 따라서 `curses` 모듈을 통해 `upperwin`과 `lowerwin`을 분리해 전자를 출력 윈도우, 후자를 입력 윈도우로 사용하도록 제작되었습니다.

### Functionalities - Plan

- [x] v0.2.: 기본적인 채팅 및 input/output 윈도우 분리 기능
- [ ] v0.3.: zepplin과의 연계를 통한 채팅 통계 및 감사 기능
- [ ] v0.4.: Airflow를 통해 구축된 영화 데이터베이스를 바탕으로 요청받은 질문에 대한 답을 돌려주는 챗봇 기능
- [ ] v0.5.: Airflow Task 완료 시 메시지를 사용자에게 알려주는 알림 기능
- [ ] v0.6.: 사용자가 설정한 일정을 지정 시간대에 알려주는 일정 기능 

### Release Changelog
- v0.2.0: python `curses` 라이브러리를 통해, 채팅방에 접속했을 경우 창을 위쪽의 upperwin, 아래쪽의 lowerwin으로 나뉘어 각각 출력/입력을 담당하도록 구현하였습니다.

