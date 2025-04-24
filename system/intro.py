import json
from llm.intro_prompt import build_intro_prompt
from model.player import Player
from model.enemy import Enemy
from llm.call_llm import call_llm


def start_game(user_input: str, user_input_character: str):
    prompt = build_intro_prompt(user_input, user_input_character)
    raw = call_llm(prompt)
    print(raw)
    data = json.loads(raw)

    player = Player(**data["player"])
    enemy1 = Enemy(**data["enemy1"])
    enemy2 = Enemy(**data["enemy2"])
    enemyBoss = Enemy(**data["enemyBoss"])

    return data["background"], player, enemy1, enemy2, enemyBoss
