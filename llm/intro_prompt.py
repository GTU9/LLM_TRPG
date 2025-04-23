def build_intro_prompt(user_input_background_story, user_input_character):
    return f"""
    너는 TRPG 게임의 마스터이며 플레이어의 설명에 따라 게임의 배경과 캐릭터를 생성해야한다.
사용자가 제공한 세계관 초기 입력은 다음과 같다:

'{user_input_background_story}'

사용자가 제공한 플레이어 캐릭터의 정보는 다음과 같아 :

'{user_input_character}'

이것을 기반으로 아래 정보를 생성하라:
1. TRPG 세계 배경 묘사
2. 플레이어 캐릭터 생성 (이름, 설명, 직업, 능력치 포함)
3. 마주칠 적 생성 (설명, 능력치, 패턴 포함)

JSON 형식으로 다음과 같이 반환하라:
{{
  "background": "...",
  "player": {{
    "name": "...",
    "explain": "...",
    "role": "...",
    "hp": ...,
    "wp": ...,
    "str_": ..., "dex_": ..., "int_": ..., "cha_": ...
  }},
  "enemy1": {{
    "name": "...",
    "species": "...",
    "hp": ...,
    "atk": ...,
    "description": "...",
    "special_patterns": [...]
  }},
  "enemy2": {{
    "name": "...",
    "species": "...",
    "hp": ...,
    "atk": ...,
    "description": "...",
    "special_patterns": [...]
  }},
  "enemyBoss": {{
    "name": "...",
    "species": "...",
    "hp": ...,
    "atk": ...,
    "description": "...",
    "special_patterns": [...]
  }}
}}
    """