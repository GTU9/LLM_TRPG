def build_intro_prompt(user_input_background_story, user_input_character):
    return f"""
    너는 TRPG 게임의 마스터이며 플레이어의 설명에 따라 게임의 배경과 캐릭터를 생성해야한다.
사용자가 제공한 세계관 초기 입력은 다음과 같다:

'{user_input_background_story}'

사용자가 제공한 플레이어 캐릭터의 정보는 다음과 같아 :

'{user_input_character}'

이것을 기반으로 아래 정보를 생성하라:
0. 모든 value 값은 한글로 표기한다.
1. TRPG 세계 배경 묘사와 캐릭터가 왜 이곳에 오게 됬는지 목적 묘사
2. 플레이어 캐릭터 생성 (이름, 설명, 직업, 능력치 포함) 능력치는 str_, dex_, int_, cha_항목은 수치를 0~5로 제한
3. ```json ``` 텍스트는 삭제
9. 해당 이벤트를 평문으로 log['exp']:value에 저장

JSON 형식으로 다음과 같이 반환하라:
{{
  "background": "...",
  "player": {{
    "name": "...",
    "explain": "...",
    "role": "...",
    "hp": ...,
    "wp": ...,
    "str_": ..., "dex_": ..., "int_": ..., "cha_": ...,
  }}
  "log: {{
    "type":"intro",
    "exp":"..."
  }}
}}
    """


from call_llm import call_llm

user_input_background_story = """황폐한 미래 도시, 뉴 에덴. 도시의 지하에는 버려진 기술과 기업의 비밀이 숨겨져 있다. 나는 실종된 동생의 흔적을 쫓아, 금지된 구역으로 들어가기로 결심했다.
"""
user_input_character = """나는 전직 정보전쟁 전문가였다. 과거 기업 사이버 전쟁에서 수많은 AI를 무너뜨렸고, 지금은 폐기된 사이버 의수를 단 채 은신 중이다. 목적은 단 하나, 진실을 찾는 것.
"""
result = call_llm(build_intro_prompt(user_input_background_story, user_input_character))

print(result)
