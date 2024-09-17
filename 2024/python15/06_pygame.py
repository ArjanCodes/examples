import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    running = True
    x = 0

    # Game loop (fixed framerate)
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simple moving rectangle
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (100 + x, 100, 50, 50))
        pygame.display.flip()
        x = (x + 1) % 500

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
