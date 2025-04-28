import random
from llm.call_llm import call_llm, call_llama3
from llm.combat_prompt import attack_kind, build_combat_prompt, start_combat_prompt


def combat(player, enemy):
    play_log = ""
    final_log = ""
    turn = 0

    play_log += show_state(player, enemy)
    print(call_llm(start_combat_prompt(play_log))["explain"])
    play_log += print_and_log(f"{player.name}이(가) {enemy.name}과(와) 만났습니다.\n")
    print("\n===== 적의 능력치 =====")
    play_log += print_and_log(enemy.get_stats())
    print("===========================\n")
    play_log += print_and_log(
        f"{player.name}이(가) {enemy.name}과(와) 전투를 시작합니다.\n"
    )

    while True:
        turn += 1
        print("=========================================\n")
        final_log += print_and_log(f"{turn}번째 턴을 시작합니다.\n")
        print("=========================================\n")
        player_log = ""
        player_log += print_and_log(f"{player.name}의 턴\n")
        print("=========================================\n")
        player_log += print_and_log(player_combat(player, enemy))
        player_log += show_state(player, enemy) + "\n"
        print(build_combat(player_log)["explain"] + "\n")
        print("=========================================\n")
        enemy_dead, log = enemy.is_dead()
        if enemy_dead:
            enemy_log += log
            print(build_combat(enemy_log)["explain"] + "\n")
            final_log += print_and_log("전투에서 승리했습니다.")
            print("=========================================\n")
            break

        final_log += player_log

        enemy_log = ""
        enemy_log += print_and_log(f"{enemy.name}턴\n")
        print("=========================================\n")
        enemy_log += print_and_log(enemy_combat(player, enemy))
        print("=========================================\n")
        enemy_log += show_state(player, enemy) + "\n"
        print("=========================================\n")
        print(build_combat(enemy_log)["explain"] + "\n")

        player_dead, log = player.is_dead()
        if player_dead:
            player_log += log
            print(build_combat(player_log)["explain"] + "\n")
            final_log += print_and_log("전투에서 패배했습니다.")
            print("=========================================\n")
            break

        final_log += enemy_log
    final_log += play_log

    print("\n===== 플레이어의 능력치 =====")
    final_log += print_and_log(player.get_stats())
    print("===========================\n")

    return final_log


def print_and_log(log):
    print(log)
    return log


def show_state(player, enemy):
    state_log = ""
    state_log += f"현재 플레이어 상태 {player.get_stats()}"
    state_log += "\n"
    state_log += f"현재 적 상태 {enemy.get_stats()}"
    return state_log


def player_combat(player, enemy):
    log = ""
    log += f"{player.name}이(가) 행동합니다." + "\n"

    user_input = input("플레이어의 행동을 입력하세요: ")
    action = call_llm(attack_kind(user_input))
    print("주사위를 굴립니다...........")
    # 플레이어 공격
    if action["action"]["type"] == "attack":
        log += f"{player.name}이(가) {enemy.name}을(를) 공격합니다.\n"
        attack_info = player.attack(user_input, action["action"]["stat"])
        # 적에게 피해 적용
        log += (
            enemy.apply_damage(
                player.name,
                user_input,
                attack_info["dmg"],
                attack_info["acc"],
                attack_info["roll"]["roll_result"],
            )
            + "\n"
        )

    # 플레이어 강화
    elif action["action"]["type"] == "strength":
        log += f"{player.name} 이(가) 자신을(를) 강화(회복)합니다.\n"
        log += player.strength(user_input, action["action"]["stat"]) + "\n"

    log += "\n"
    return log


def enemy_combat(player, enemy):
    log = ""
    log += f"{enemy.name}이(가) 행동합니다." + "\n"
    pattern = random.choice(enemy.special_patterns)

    # 적 공격
    if pattern["type"]["kind"] == "attack":
        print("주사위를 굴립니다...........")
        log += f"{enemy.name}이(가) {player.name}을(를) 공격합니다.\n"
        attack_info = enemy.attack(pattern)
        # 플레이어에게 피해 적용
        log += (
            player.apply_damage(
                enemy.name,
                pattern["name"] + " 을 시전합니다.",
                attack_info["dmg"],
                attack_info["acc"],
                pattern["type"]["stat"],
                attack_info["roll"]["roll_result"],
            )
            + "\n"
        )

    # 적 강화
    elif pattern["type"]["kind"] == "strength":
        log += f"{enemy.name} 이(가) 자신을(를) 강화(회복)합니다.\n"
        log += enemy.strength(pattern) + "\n"

    log += "\n"
    return log


def build_combat(play_log):
    combat_log = call_llm(build_combat_prompt(play_log))
    return combat_log
