from random import randint
from system.dice import roll_dice, get_outcome_label

# 출력용 한글 매핑
STAT_KO = {
    'hp': '체력', 'wp': '정신력',
    'str_': '힘', 'dex_': '민첩',
    'int_': '지능', 'char_': '화술'
}

class Player:           # 플레이어 state
    def __init__(self,
                 name,      # 플레이어 이름
                 explain,   # 플레이어 설명
                 role,      # 플레이어 직업
                 hp,        # 플레이어 체력
                 wp,        # 플레이어 정신력
                 str_,      # 플레이어 힘
                 dex_,      # 플레이어 민첩성
                 int_,      # 플레이어 지능
                 char_,     # 플레이어 화술
                 # inventory: dict  # 플레이어 인벤토리, 아이템 이름과 설명으로 이루어진 딕셔너리 목록
                 ):
        self.name = name
        self.explain = explain
        self.role = role
        self.hp = hp
        self.wp = wp
        self.str_ = str_
        self.dex_ = dex_
        self.int_ = int_
        self.char_ = char_
        # self.inventory = inventory  # 플레이어 인벤토리

    def get_stats(self):  # 플레이어 능력치 반환
        return f"""
            이름: {self.name}
            설명: {self.explain}
            직업: {self.role}
            체력: {self.hp}
            정신력: {self.wp}
            힘: {self.str_}
            민첩: {self.dex_}
            지능: {self.int_}
            화술: {self.char_}
        """

    # 임의 플레이어 능력치 증감
    def update_stat(self, stat_name, value):
        # [BUG FIX] LLM이 문자열로 반환하는 경우 int 변환
        try:
            value = int(value)
        except (ValueError, TypeError):
            print(f"[경고] '{STAT_KO.get(stat_name, stat_name)}' 변화값 '{value}'이(가) 숫자가 아닙니다. 무시합니다.")
            return

        if stat_name == "hp":
            self.hp = max(0, min(100, self.hp + value))
        elif stat_name == "wp":
            self.wp = max(0, min(100, self.wp + value))
        elif stat_name == "str_":
            self.str_ = max(0, min(10, self.str_ + value))
        elif stat_name == "dex_":
            self.dex_ = max(0, min(10, self.dex_ + value))
        elif stat_name == "int_":
            self.int_ = max(0, min(10, self.int_ + value))
        elif stat_name == "char_":
            self.char_ = max(0, min(10, self.char_ + value))
        else:
            print(f"'{stat_name}' 은(는) 존재하지 않는 능력치입니다.")

    def get_one_state(self, type):  # 플레이어 해당 능력치 반환
        stat_map = {
            'hp': self.hp,
            'wp': self.wp,
            'str_': self.str_,
            'dex_': self.dex_,
            'int_': self.int_,
            'char_': self.char_
        }
        return stat_map.get(type, 0)

    # 플레이어 능력치 보정치 반환
    def get_bonus(self, type):
        if type == 'str_':
            return self.str_ - 2
        elif type == 'dex_':
            return self.dex_ - 2
        elif type == 'int_':
            return self.int_ - 2
        elif type == 'char_':
            return self.char_ - 2
        else:
            return 0

    # 플레이어 이벤트 결과
    def event_result(self, text, type, num):  # 이벤트 결과 설명과, 증감된 능력치, 수치
        stat_ko = STAT_KO.get(type, type)
        log = f"{self.name}이(가) {stat_ko}을(를) {num} 만큼 증감합니다.\n"
        self.update_stat(type, num)
        return log

    # 플레이어 전투 중 강화
    def strength(self, text, type):  # 캐릭터를 강화한다.
        roll = get_outcome_label(roll_dice())
        stat_ko = STAT_KO.get(type, type)
        log = ""
        log += text + "\n"
        log += f"{self.name}이(가) {stat_ko}을(를) 강화(회복)합니다.\n"
        if roll['strength'] == 0:
            log += f"주사위 값 {roll['roll_result']}! 강화(회복)에 실패했습니다.\n"
        else:
            if type == 'hp' or type == 'wp':
                log += f"주사위 값 {roll['roll_result']}! {stat_ko} +{roll['strength']*10} 강화(회복)에 성공했습니다.\n"
                self.update_stat(type, roll['strength'] * 10)
            else:
                log += f"주사위 값 {roll['roll_result']}! {stat_ko} +{roll['strength']} 강화(회복)에 성공했습니다.\n"
                self.update_stat(type, roll['strength'])
        return log

    # 플레이어 공격
    def attack(self, text, type):  # LLM이 공격을 설명하는 문자열과 적 정보, 주사위 굴림 결과를 받음
        roll = get_outcome_label(roll_dice() + self.get_bonus(type))
        acc = roll['acc']
        dmg = int(self.get_one_state(type) * 2 * roll['dmgCf'])
        return {
            "player": self.get_stats(),
            "text": text,
            "acc": acc,
            "dmg": dmg,
            "roll": roll
        }

    # 플레이어 피해 적용
    def apply_damage(self, enemy, text, dmg, acc, type, roll_result):
        stat_ko = STAT_KO.get(type, type)
        log = ""
        log += enemy + '이(가) ' + text + "\n"
        log += f"{self.name}이(가) {stat_ko} 공격을 받습니다. 주사위 값 {roll_result}! 공격력 {dmg} 명중률 {acc}%\n"
        roll = randint(1, 100)
        if roll <= acc:
            if type == 'hp':
                self.hp = max(0, self.hp - dmg)
                log += f"공격이 명중했습니다. {self.name}의 체력이 {dmg}만큼 감소했습니다. 현재 체력: {self.hp}\n"
            elif type == 'wp':
                self.wp = max(0, self.wp - dmg)
                log += f"공격이 명중했습니다. {self.name}의 정신력이 {dmg}만큼 감소했습니다. 현재 정신력: {self.wp}\n"
            else:
                log += f"[경고] 알 수 없는 공격 타입: {type}\n"
        else:
            log += "공격이 빗나갔습니다.\n"
        return log

    def is_dead(self):  # 플레이어 사망 체크
        if self.hp <= 0:
            state, log = True, f"{self.name}이(가) 체력이 0이 되어 쓰러졌습니다."
        elif self.wp <= 0:
            state, log = True, f"{self.name}이(가) 정신력이 0이 되어 쓰러졌습니다."
        else:
            state, log = False, "\n"
        return state, log
