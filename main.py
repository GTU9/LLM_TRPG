import random
from system.objec_factory import start_game, create_enemy
from system.event import event
from system.combat import combat
from system.ending import ending
from system.save_log import save_log


def main():
    print("['내가 만드는 TRPG 게임'에 오신것을 환영합니다.]\n")
    print("[세계관 설정과 내가 쓸 주인공 캐릭터를 설정합니다!]\n")
    user_input_background = input("세계관(배경 설정)을 입력하세요: ")
    user_input_character = input("캐릭터 정보를 입력하세요: ")

    background, player = start_game(user_input_background, user_input_character)

    print("\n[세계관 설정 완료]")
    print("===========================\n")
    print(background)
    print("===========================\n")
    print("[캐릭터 설정]")
    print(player.get_stats())
    print("===========================\n")

    play_log = ""

    play_log += f"세계관 : {background}\n 플레이어 정보: {player.get_stats()}"

    time = 0

    while True:
        time += 1
        print("\n===== 이벤트 발생 =====")
        play_log += event(player, play_log)

        dead, dead_log = player.is_dead()
        if dead:
            print(dead_log)
            print("게임 오버!\n")
            break
        save_log(play_log)

        if random.random() < 1.0:
            print("\n===== 적이 등장했습니다! =====")
            enemy = create_enemy(play_log)
            play_log += combat(player, enemy)

            dead, dead_log = player.is_dead()
            if dead:
                print(dead_log)
                print("게임 오버!\n")
                break
        save_log(play_log)

        if time >= 1:
            break

    ending(play_log)
    save_log(play_log)


main()
