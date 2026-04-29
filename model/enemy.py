from random import randint
from system.dice import roll_dice, get_outcome_label

# 출력용 한글 매핑
STAT_KO = {
    'hp': '체력', 'atk': '공격력'
}

class Enemy:
    def __init__(
        self,
        name,               # 적 이름
        species,            # 종류 or 분류 (예: 괴수, 인간, 악령 등)
        hp,                 # 체력
        atk,                # 공격력
        description,        # 설명 텍스트
        special_patterns,   # 특수 행동 함수 or 설명
    ):
        self.name = name
        self.species = species
        self.hp = hp
        self.atk = atk
        self.description = description
        self.special_patterns = special_patterns  # 선택적 기능

    # 적 상태 출력
    def get_stats(self):
        special_action_names = [pattern['name'] for pattern in self.special_patterns]
        return f"""
            이름: {self.name}
            종류: {self.species}
            체력: {self.hp}
            공격력: {self.atk}
            설명: {self.description}
            특수 행동: {special_action_names}
        """

    # 임의 적 능력치 증감
    def update_stat(self, stat_name, value):
        # [BUG FIX] LLM이 문자열로 반환하는 경우 int 변환 + 상한선 적용
        try:
            value = int(value)
        except (ValueError, TypeError):
            print(f"[경고] '{STAT_KO.get(stat_name, stat_name)}' 변화값 '{value}'이(가) 숫자가 아닙니다. 무시합니다.")
            return

        if stat_name == "hp":
            self.hp = max(0, min(100, self.hp + value))
        elif stat_name == "atk":
            self.atk = max(0, min(50, self.atk + value))
        else:
            print(f"'{stat_name}' 은(는) 존재하지 않는 능력치입니다.")

    # 적 능력치 강화
    def strength(self, pattern):
        stat_ko = STAT_KO.get(pattern['type']['stat'], pattern['type']['stat'])
        log = f"{self.name}이(가) {pattern['name']}을(를) 시전합니다.\n"
        log += f"{self.name}의 {stat_ko}이(가) {pattern['cf']} 만큼 강화(회복)되었습니다.\n"
        self.update_stat(pattern['type']["stat"], pattern["cf"])
        return log

    # 적 공격
    def attack(self, pattern):
        # [BUG FIX] 적 주사위 +3 고정 보정 제거 → 공평한 주사위
        roll = get_outcome_label(roll_dice())  # 주사위 굴림 결과
        acc = roll["acc"]
        dmg = int(self.atk * pattern["cf"] * roll["dmgCf"])
        return {
            "enemy": self.get_stats(),
            "pattern": pattern,
            "roll": roll,
            "acc": acc,
            "dmg": dmg,
        }

    # 데미지 적용
    def apply_damage(self, player, text, dmg, acc, roll_result):
        roll = randint(1, 100)
        log = ""
        log += f"{player}(이)가 {text}을 시전합니다.\n"
        log += f"{self.name}이(가) {dmg}의 공격을 받습니다. 주사위 값 {roll_result}! 공격력 {dmg} 명중률 {acc}%\n"
        if roll <= acc:
            self.hp = max(0, self.hp - dmg)
            log += f"공격이 명중했습니다. {self.name}의 체력이 {dmg}만큼 감소했습니다.\n현재 적 체력: {self.hp}"
        else:
            log += "공격이 빗나갔습니다."
        return log

    def is_dead(self):  # 적 사망 여부 확인
        if self.hp <= 0:
            state, log = True, f"{self.name}이(가) 쓰러졌습니다.\n"
        else:
            state, log = False, "\n"
        return state, log
