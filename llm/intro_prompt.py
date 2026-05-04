def build_intro_prompt(user_input_background_story, user_input_character):
    return f"""
너는 TRPG 게임의 마스터이며 플레이어의 설명에 따라 게임의 배경과 캐릭터를 생성해야한다.
사용자가 제공한 세계관 초기 입력은 다음과 같다:

{user_input_background_story}

사용자가 제공한 플레이어 캐릭터의 정보는 다음과 같다:

{user_input_character}

이것을 기반으로 아래 정보를 생성하라:
0. 문자열 value 값은 한글로 표기한다. 숫자 value는 반드시 정수(integer)로 표기한다.
1. TRPG 세계 배경 묘사와 캐릭터가 왜 이곳에 오게 됐는지 목적 묘사
2. 플레이어 캐릭터 생성 (이름, 설명, 직업, 능력치 포함). hp, wp는 30~50, str_, dex_, int_, char_는 0~5로 제한
3. 작은따옴표(')는 절대 사용하지 않는다. 모든 key와 문자열 value는 반드시 큰따옴표(")로 감싼다.
4. ```json``` 텍스트는 포함하지 않는다.
5. JSON 외 다른 텍스트는 절대 포함하지 않는다.

반드시 유효한 JSON 형식으로 다음과 같이 반환하라:
{{
    "background": "...",
    "player": {{
        "name": "...",
        "explain": "...",
        "role": "...",
        "hp": 40,
        "wp": 35,
        "str_": 3,
        "dex_": 2,
        "int_": 3,
        "char_": 2
    }},
    "log": {{
        "type": "intro",
        "exp": "..."
    }}
}}
"""
