import matplotlib.pyplot as plt


def visualize_plot(game, generations, sleep_time):
    fig, ax = plt.subplots()
    game_display = ax.imshow(game.grid.grid, cmap="gray_r")

    ax.set_xticks([])
    ax.set_yticks([])

    for generation in range(generations):
        game.update()
        game_display.set_data(game.grid.grid)
        plt.draw()
        plt.pause(sleep_time)

    plt.show()
