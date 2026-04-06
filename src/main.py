from model import analyze


TEST_CASES = [
    "I feel sad and nobody cares about me 😟 😕 😥. #sad",
    "I don't want to live anymore. Everything is hopeless and I'm so tired.",
    "I'm not depressed, I'm actually doing really well today 😊",
    "Extremely lonely and worthless. I can't sleep, I can't eat.",
    "I want to die. There's no reason to live.",
    "I don't want to die — I just want to feel better. Going to therapy helped.",
    "Feeling grateful and hopeful. Had fun with friends today 🎉",
]


def print_result(text: str) -> None:
    print("─" * 60)
    print(f"INPUT   : {text}")
    result = analyze(text)
    print(f"SCORE   : {result.raw_score}")
    print(f"DEPRESS : [{result.depression.level.upper()}] {result.depression.label}")
    print(f"SUICIDE : [{result.suicide.risk.upper()}] {result.suicide.label}")
    if result.patterns_found:
        print(f"HITS    : {result.patterns_found}")
    print()


if __name__ == "__main__":
    for t in TEST_CASES:
        print_result(t)

