from game import Game

def main() -> None:
    """Main function to start the game
    """
    user_name = Game.get_user_name()
    game = Game(user_name)
    game.play()

if __name__ == '__main__':
    main()
    