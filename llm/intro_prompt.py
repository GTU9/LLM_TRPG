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
2. 플레이어 캐릭터 생성 (이름, 설명, 직업, 능력치 포함) 능력치 hp,wp 항목은 수치 30~50로 제한, str_, dex_, int_, cha_항목은 수치를 0~5로 제한
3. ```json ``` 텍스트는 삭제
9. 해당 이벤트를 평문으로 log['exp']:value에 저장

반드시 JSON 형식으로 다음과 같이 반환하라:
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