from random import randint

class Enemy:
    def __init__(self,  
                 name,   # 적 이름
                 species,  # 종류 or 분류 (예: 괴수, 인간, 악령 등)
                 hp,     # 체력
                 atk,    # 공격력
                 description,  # 설명 텍스트
                special_patterns # 특수 행동 함수 or 설명
                ):
        self.name = name
        self.species = species
        self.hp = hp
        self.atk = atk
        self.description = description
        self.special_patterns =  special_patterns  # 선택적 기능

    # 적 상태 출력
    def get_stats(self):
        stats = {
            "이름": self.name,
            "종류": self.species,
            "체력": self.hp,
            "공격력": self.atk,
            "설명": self.description,
            "특수 행동": self.special_patterns
        }
        return stats
    
     # 임의 적 능력치 증감 
    def set_stat(self, stat_name, value):
        if stat_name == 'hp':
            self.hp += value
        elif stat_name == 'atk':
            self.atk += value
        else:
            print(f"'{stat_name}' 은(는) 존재하지 않는 능력치입니다.")

    # 적 행동패턴 반환
    def act(self, roll, target):
        state =self.get_stats()
        return {"Enermy_state" : state,
                "roll" : roll,
                "target" : target
                }
    
    # 데미지 적용
    def apply_damage(self, dmg, acc):
        roll = randint(1, 100)
        if roll <= acc:
            self.hp = max(0, self.hp - dmg)
            log = f" 공격이 명중했습니다. {self.name}의 체력이 {dmg}만큼 감소했습니다."
        else:
            log = "공격이 빗나갔습니다."
        return log

    def is_dead(self):  # 적 사망 여부 확인
        if self.hp <= 0:
            state,log = True, f"{self.name}이(가) 사망했습니다."
        else: 
            state, log =False, f"{self.name}이(가) 살아있습니다."
        return state, log
