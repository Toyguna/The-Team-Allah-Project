import src.game as game

if __name__ == "__main__":
    print(">> Launching...")

    gameInstance = game.Game()
    gameInstance.game_loop()