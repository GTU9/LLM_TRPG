from llm.call_llm import call_llm, call_llama3
from llm.event_prompt import build_event_prompt_before, build_event_prompt_after
from system.dice import roll_dice, get_outcome_label


def event(player, play_log):

    event_log = ""

    event_log += player.get_stats()

    event_log += event_before(play_log)

    event_log += event_after(player, event_log)

    return event_log


def print_and_log(log):
    print(log)
    return log


def event_before(play_log):
    event_log = ""

    event_before = call_llm(build_event_prompt_before(play_log))
    event_log += print_and_log(event_before["event"]["explain"])

    return event_log


def event_after(player, event_before_log):

    event_log = ""
    player_act = input("\n플레이어의 행동을 입력하세요: ")
    roll_result = get_outcome_label(roll_dice())["roll_result"]
    event_log += print_and_log(
        f"{player.name}은 {player_act} 행동을 하기로 결정하였습니다.\n"
    )
    event_log += print_and_log(f"주사위를 굴립니다.....\n")
    event_log += print_and_log(f"주사위 결과는 {roll_result}입니다.\n")

    event_result = call_llm(
        build_event_prompt_after(event_before_log, player_act, roll_result)
    )
    event_log += print_and_log(event_result["event"]["explain"] + "\n")

    for stat, change_value in event_result["event"]["type"].items():
        player.update_stat(stat, change_value)
        event_log += print_and_log(
            f"{player.name}의 능력치가 {stat}이 + {change_value} 만큼 변화했습니다."
        )

    print("\n===== 플레이어의 능력치 =====")
    event_log += print_and_log(player.get_stats())
    print("===========================\n")

    return event_log
