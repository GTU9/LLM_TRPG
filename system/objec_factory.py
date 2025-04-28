from llm.intro_prompt import build_intro_prompt
from llm.enemy_prompt import build_enemy_prompt

from llm.call_llm import call_llm, call_llama3

from model.player import Player
from model.enemy import Enemy


def start_game(user_input, user_input_character):
    prompt = build_intro_prompt(user_input, user_input_character)
    data = call_llm(prompt)

    background = data["background"]
    player = Player(**data["player"])

    return background, player


def create_enemy(background):
    prompt = build_enemy_prompt(background)
    data = call_llm(prompt)

    enemy = Enemy(**data["enemy"])

    return enemy
