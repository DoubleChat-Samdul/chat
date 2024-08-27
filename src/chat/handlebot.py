import json
import pandas as pd
import os

def call_bot(message, username, upperwin):
    # JSON 파일 읽기 및 DataFrame으로 변환
    home_dir = os.path.expanduser("~") #홈 디렉토리 경로를 반환
    file_path = os.path.join(home_dir, f"data/movdata/year=2021/movieList.json")  
    
    with open(file_path, 'r') as f:
        data = json.load(f)

    df = pd.json_normalize(data)  # JSON 구조에 따라 데이터를 정규화하여 DataFrame으로 변환

    if '@bot' in message or '@봇' in message:
        try:
            if '@bot' in message:
                # 메시지에서 '@bot' 부분을 제거하고 나머지 부분 가져오기
                command = message.split('@bot ')[1].strip()
            elif '@봇' in message:
                command = message.split('@봇 ')[1].strip()

            # 키워드1과 키워드2를 '|'를 기준으로 분리
            try:
                keyword1, keyword2 = command.split('|')
                movname = keyword1.strip()  # keyword1을 영화 제목으로 사용
                keyword2 = keyword2.strip()

                # 영화이름과 키워드에 따라 데이터 검색
                if keyword2 == '감독':
                    result = df[df['movieNm'] == movname]['directors'].explode().dropna()
                    if not result.empty:
                        directors = ", ".join(result.apply(lambda x: x['peopleNm']))
                        result_message = f"{movname}를 만든 감독의 이름은 {directors} 입니다."
                    else:
                        result_message = f"{movname}에 대한 감독 정보를 찾을 수 없습니다."

                elif keyword2 == '장르':
                    result = df[df['movieNm'] == movname]['genreAlt']
                    if not result.empty:
                        result_message = f"{movname}의 장르는 {result.iloc[0]} 입니다."
                    else:
                        result_message = f"{movname}에 대한 장르 정보를 찾을 수 없습니다."

                elif keyword2 == '제작년도':
                    result = df[df['movieNm'] == movname]['prdtYear']
                    if not result.empty:
                        result_message = f"{movname}의 제작년도는 {result.iloc[0]} 입니다."
                    else:
                        result_message = f"{movname}에 대한 제작년도 정보를 찾을 수 없습니다."

                else:
                    result_message = "[bot]: 잘못된 형식입니다. '@bot 영화이름|<감독/장르/제작년도>' 형식으로 입력해주세요."

                upperwin.addstr(f"[{username}가 bot을 호출하였습니다]: {message}\n")
                upperwin.addstr(f"[bot]: {result_message}\n")
                upperwin.refresh()
                return True

            except ValueError:
                # '|'로 분리되지 않은 경우 처리
                upperwin.addstr(f"[{username}가 bot을 호출하였습니다]: {message}\n")
                upperwin.addstr("[bot]: 잘못된 형식입니다. '@bot 영화이름|<감독/장르/제작년도>' 형식으로 입력해주세요.\n")
                upperwin.refresh()
                return True  # Bot이 호출되었음을 알림

        except IndexError:
            # @bot 또는 @봇 다음에 텍스트가 없는 경우 처리
            upperwin.addstr(f"[{username}가 bot을 호출하였습니다]: {message}\n")
            upperwin.addstr("[bot]: 명령을 인식할 수 없습니다. '@bot 영화이름|<감독/장르/제작년도>' 형식으로 입력해주세요.\n")
            upperwin.refresh()
            return True

    return False  # Bot이 호출되지 않음

