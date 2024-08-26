# chat
팀프로젝트2를 위해 개발한 Kafka 서버를 경유하는 채팅 기능입니다.

### Functionalities
- [x] v0.2.: 기본적인 채팅 및 input/output 윈도우 분리 기능
![스크린샷 2024-08-26 105436](https://github.com/user-attachments/assets/4eee8002-5fd3-4168-91ec-26ae45c9d94a)

- [ ] v0.3.: zepplin과의 연계를 통한 채팅 통계 및 감사 기능
- [ ] v0.4.: Airflow를 통해 구축된 영화 데이터베이스를 바탕으로 요청받은 질문에 대한 답을 돌려주는 챗봇 기능
- [ ] v0.5.: Airflow Task 완료 시 메시지를 사용자에게 알려주는 알림 기능
- [ ] v0.6.: 사용자가 설정한 일정을 지정 시간대에 알려주는 일정 기능 

### changelog
- v0.2.0: python `curses` 라이브러리를 통해, 채팅방에 접속했을 경우 창을 위쪽의 upperwin, 아래쪽의 lowerwin으로 나뉘어 각각 출력/입력을 담당하도록 구현하였습니다.
