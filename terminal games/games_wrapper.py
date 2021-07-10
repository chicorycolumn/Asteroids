from games.guess_game import guess_game
from games.quick_maths import quick_maths


def play():
    score = {"value": 0}

    while True:
        to_play_response = input("Play a game?\n(Q)uick maths | (G)uess game | (X) Exit")
        if to_play_response.lower() == "g":
            guess_game(score)
            continue
        if to_play_response.lower() == "gg":
            guess_game(score=score, cheat=True)
            continue
        if to_play_response.lower() == "q":
            quick_maths(score)
            continue
        if to_play_response.lower() == "qq":
            quick_maths(score=score, cheat=True)
            continue
        elif to_play_response.lower() == "x":
            print("Goodbye!")
            break
        else:
            print("Not an option")
            continue


if __name__ == "__main__.py":
    play()
