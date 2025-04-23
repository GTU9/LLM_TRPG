import random

def roll_dice(sides=12):        # 12면체 주사위
    return random.randint(1, sides)

def get_outcome_label(roll_result: int):    # 주사위 값 에 따른 결과 레이블 반환
    if roll_result <= 3:
        label = "대실패"
    elif roll_result <= 6:
        label = "실패"
    elif roll_result <= 9:
        label = "성공"
    else:
        label = "대성공"

    return {
        "roll_result": roll_result,
        "label": label,
    }
