import time


def visualize_console(game, generations, sleep_time):
    for generation in range(1, generations):
        game.update()
        print(f"Generation {generation}:\n")
        print(game.grid)
        time.sleep(sleep_time)
