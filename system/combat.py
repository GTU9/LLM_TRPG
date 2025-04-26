import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.call_llm import call_llm
from llm.combat_prompt import attack_kind, build_combat_prompt
from model.player import Player
from model.enemy import Enemy

def player_combat(player, enemy):
    log =""
    log += f'현재 플레이어 상태 : {repr(player.get_stats())}\n'
    log += f'현재 적 상태 : {repr(enemy.get_stats())}\n'
    log += '\n'
    log += f"{player.name}이(가) 행동합니다."+"\n"

    user_input=input('플레이어의 행동을 입력하세요: ')
    action = call_llm(attack_kind(user_input))
    # 플레이어 공격
    if action['action']['type'] == "attack":
        log += f'{player.name}이(가) {enemy.name}을(를) 공격합니다.\n'
        attack_info = player.attack(user_input, action['action']['stat'])
        # 적에게 피해 적용
        log += enemy.apply_damage(player.name, user_input, attack_info['dmg'], attack_info['acc'], attack_info['roll']['roll_result'])+"\n"
        
    # 플레이어 강화
    elif action['action']['type'] == "strength":
        log += f'{player.name} 이(가) 자신을(를) 강화(회복)합니다.\n'
        log += player.strength(user_input, action['action']['stat']) +'\n'

    log += '\n'
    log += f'현재 플레이어 상태 : {repr(player.get_stats())}\n'
    log += f'현재 적 상태 : {repr(enemy.get_stats())}\n'
    
    return log

def enemy_combat(player, enemy):
    log =""
    log += f'현재 플레이어 상태 : {repr(player.get_stats())}\n'
    log += f'현재 적 상태 : {repr(enemy.get_stats())}\n'
    log += '\n'
    log += f"{enemy.name}이(가) 행동합니다."+"\n"
    pattern = random.choice(enemy.special_patterns)

    # 적 공격
    if pattern['type']['kind'] == "attack":
        log += f'{enemy.name}이(가) {player.name}을(를) 공격합니다.\n'
        attack_info = enemy.attack(pattern)
        # 플레이어에게 피해 적용
        log += player.apply_damage(enemy.name, pattern['name']+' 을 시전합니다.', attack_info['dmg'], attack_info['acc'],pattern['type']['stat'] ,attack_info['roll']['roll_result'])+"\n"

    # 적 강화  
    elif pattern['type']['kind'] == "strength":
        log += f'{enemy.name} 이(가) 자신을(를) 강화(회복)합니다.\n'
        log += enemy.strength(pattern) + '\n'

    log += '\n'
    log += f'현재 플레이어 상태 : {repr(player.get_stats())}\n'
    log += f'현재 적 상태 : {repr(enemy.get_stats())}\n'

    return log

def build_combat(play_log):
    combat_log=call_llm(build_combat_prompt(play_log))
    return combat_log

user_input_background_story = """황폐한 미래 도시, 뉴 에덴. 도시의 지하에는 버려진 기술과 기업의 비밀이 숨겨져 있다. 나는 실종된 동생의 흔적을 쫓아, 금지된 구역으로 들어가기로 결심했다.
"""
user_input_character = """나는 전직 정보전쟁 전문가였다. 과거 기업 사이버 전쟁에서 수많은 AI를 무너뜨렸고, 지금은 폐기된 사이버 의수를 단 채 은신 중이다. 목적은 단 하나, 진실을 찾는 것.
"""
player = Player(
    name="이안",
    explain="전직 정보전쟁 전문가. 폐기된 사이버 의수를 단 채 금지구역을 탐사하고 있다.",
    role="정보전 전문가",
    hp=55,
    wp=40,
    str_=2,
    dex_=4,
    int_=5,
    cha_=3
)

enemy = Enemy(
    name="사이버 괴물",
    species="인간",
    hp=50,
    atk=10,
    description="사이버네틱으로 변형된 괴물. 빠른 속도와 강력한 공격력을 지닌다.",
    special_patterns=[
        {
            "name": "전기 충격",
            "type": {
                "kind": "attack",
                "stat": "hp"
            },
            "cf": 1.5
        },
        {
            "name": "강화 방어",
            "type": {
                "kind": "strength",
                "stat": "hp"
            },
            "cf": 2
        }
    ]
)

play_log=""
while True:

    log= player_combat(player, enemy)
    play_log+=log
    print((build_combat(log))['explain']+'\n')
    
    log= enemy_combat(player, enemy)
    play_log+=log
    print((build_combat(log))['explain']+'\n')

    player_dead, player_log = player.is_dead()
    enemy_dead, enemy_log = enemy.is_dead()

    if player_dead:
        print(player_log)
        break
    
    if enemy_dead:
        print(enemy_log)
        break

# log= '''
# 현재 플레이어 상태 : {'이름': '이안', '직업': '정보전 전문가', '체력': 1, '정신력': 40, '힘': 2, '민첩': 4, '지능': 5, '화술': 3}
# 현재 적 상태 : {'이름': '사이버 괴물', '종류': '인간', '체력': 33, '공격력': 10, '설명': '사이버네틱으로 변형된 괴물. 빠른 속도와 강력한 공격력을 지닌다.', '특수 행동': [{'name': '전기 충격', 'type': {'kind': 'attack', 'stat': 'hp'}, 'cf': 1.5}, {'name': '강화 방어', 'type': {'kind': 'strength', 'stat': 'hp'}, 'cf': 2}]}

# 이안이(가) 행동합니다.
# 이안이(가) 사이버 괴물을(를) 공격합니다.
# 이안(이)가 총쏘기 을 시전합니다.
# 사이버 괴물이(가) 2의 공격을 받습니다. 주사위 값 1! 공격력 2 명중률 0%
# 공격이 빗나갔습니다.

# 현재 플레이어 상태 : {'이름': '이안', '직업': '정보전 전문가', '체력': 1, '정신력': 40, '힘': 2, '민첩': 4, '지능': 5, '화술': 3}
# 현재 적 상태 : {'이름': '사이버 괴물', '종류': '인간', '체력': 33, '공격력': 10, '설명': '사이버네틱으로 변형된 괴물. 빠른 속도와 강력한 공격력을 지닌다.', '특수 행동': [{'name': '전기 충격', 'type': {'kind': 'attack', 'stat': 'hp'}, 'cf': 1.5}, {'name': '강화 방어', 'type': {'kind': 'strength', 'stat': 'hp'}, 'cf': 2}]}
# '''

# print(build_combat(log)['log']['explain'])