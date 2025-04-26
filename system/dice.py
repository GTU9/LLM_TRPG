import random

def roll_dice(sides=12):        # 12면체 주사위
    return random.randint(1, sides)

def get_outcome_label(roll_result: int):    # 주사위 값 에 따른 결과 레이블 반환
    if roll_result <= 1:
        label = "대실패"
        acc = 0
        dmgCf = 0.6
        strength = 0
    elif roll_result <= 3:
        label = f"{roll_result}"
        acc =50
        dmgCf = 0.8
        strength = 1
    elif roll_result <= 6:
        label = f"{roll_result}"
        acc =70
        dmgCf = 1.0
        strength = 1
    elif roll_result <= 9:
        label = f"{roll_result}"
        acc =80
        dmgCf = 1.2
        strength = 1
    elif roll_result <= 11:
        label = f"{roll_result}"
        acc = 90
        dmgCf = 1.4 
        strength = 2
    else:
        label = "대성공"
        acc= 100
        dmgCf = 1.6
        strength = 3

    return {
        "roll_result": roll_result,
        "label": label,
        "dmgCf" : dmgCf,
        "acc" : acc,
        "strength" : strength
    }
