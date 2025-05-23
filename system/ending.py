from llm.ending_prompt import build_ending_prompt
from llm.call_llm import call_llm, call_llama3


def ending(play_log):
    end = call_llm(build_ending_prompt(play_log))

    print("[엔딩 제목]")
    print("=================================")
    print(end["ending"]["title"])
    print("=================================")
    print("\n[엔딩]")
    print(end["ending"]["summary"])

    end_log = ""
    end_log += end["ending"]["title"] + "/n" + end["ending"]["summary"]
