import json
from llm.intro_prompt import build_intro_prompt
from model.player import Player
from model.enemy import Enemy

def start_game(user_input: str):
    prompt = build_intro_prompt(user_input)
    raw = call_llm(prompt)
    data = json.loads(raw)

    player = Player(**data["player"])
    enemy = Enemy(**data["enemy"])

    return data["background"], player, enemy