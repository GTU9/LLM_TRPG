from random import randint

class Player:           # 플레이어 state
    def __init__(self,  
                 name,  # 플레이어 이름
                 explain,  # 플레이어 설명
                 role,  # 플레이어 직업
                 hp,    # 플레이어 체력
                 wp,    # 플레이어 정신력
                 str_   # 플레이어 힘
                 ,dex_  # 플레이어 민첩성
                 ,int_  # 플레이어 지능
                 ,cha_  # 플레이어 화술
                #  ,inventory: dict # 플레이어 인벤토리, 아이템 이름과 설명으로 이루어진 딕셔너리 목록                 
                 ): 
        self.name = name
        self.explain = explain
        self.role = role 
        self.hp = hp
        self.wp = wp
        self.str_ = str_
        self.dex_ = dex_
        self.int_ = int_
        self.cha_ = cha_
        # self.inventory = inventory # 플레이어 인벤토리
    
    def get_stats(self):  # 플레이어 능력치 반환
        stats = {
            '이름': self.name,
            '직업': self.role,
            '체력': self.hp,
            '정신력': self.wp,
            '힘': self.str_,
            '민첩': self.dex_,
            '지능': self.int_,
            '화술': self.cha_
        }
        return stats
    
    # 임의 플레이어 능력치 증감
    def set_stat(self, stat_name, value):  
        if stat_name == "hp":
            self.hp += value
        elif stat_name == "wp":
            self.wp += value
        elif stat_name == "str":
            self.str_ += value
        elif stat_name == "dex":
            self.dex_ += value
        elif stat_name == "int":
            self.int_ += value
        elif stat_name == "cha":
            self.cha_ += value
        else:
            print(f"'{stat_name}' 은(는) 존재하지 않는 능력치입니다.")

    # 플레이어 능력치 보정치 반환
    def get_bonus(self, type):  
        if type == 'str_':
            return self.str_-2
        elif type == 'dex_':
            return self.dex_-2  
        elif type == 'int_':
            return self.int_-2
        elif type == 'cha_':
            return self.cha_-2
        else:
            return 0
    
    # 플레이어 공격
    def act(self, explain,  target, roll, type):  # LLM이 공격을 설명하는 문자열과 적 정보, 주사위 굴림 결과, 보정치, 타입을 받음
        get_bonus = self.get_bonus(type)
        stat = self.get_stats()
        return {"explain" : explain,
                "player_state": stat,
                "target": target,
                "roll":roll,
                "bonus": get_bonus,
                "type": type
                }

    # 플레이어 피해 적용, 데미지, 적중률, 타입
    def apply_damage(self, explain, dmg, acc, type):
        log = f"{self.name}이(가) {type}에 {dmg}의 공격을 받습니다. 명중률 {acc}%\n"
        log += explain + "\n"
        roll = randint(1, 100)
        if roll <= acc:
            if type == 'hp':
                self.hp = max(0, self.hp - dmg)
                log+= f"{self.name}의 체력이 {dmg}만큼 감소했습니다. 현재 체력: {self.hp}"
            elif type == 'wp':
                self.wp = max(0, self.wp - dmg)
                log += f"{self.name}의 정신력이 {dmg}만큼 감소했습니다. 현재 정신력: {self.wp}"
            else:
                return False # 잘못된 타입
        else:
            log += "공격이 빗나갔습니다." # 빗나감
            
        return log
            
    def is_dead(self):  # 플레이어 사망 체크
        if self.hp <= 0:
            state,log = True, f"{self.name}이(가) hp가 0 이되어 사망했습니다."
        elif self.wp <= 0:
            state, log = True, f"{self.name}이(가) wp가 0 이되어 사망했습니다."
        else: 
            state, log =False, f"{self.name}이(가) 살아있습니다."
        return state, log