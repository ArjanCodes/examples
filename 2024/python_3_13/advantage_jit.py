WIDTH, HEIGHT = 800, 600
MAX_ITERATIONS = 256
XMIN, XMAX = -2.0, 1.0
YMIN, YMAX = -1.5, 1.5


def create_image() -> list[list[int]]:
    image = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Compute heavy computation
    for y in range(HEIGHT):
        for x in range(WIDTH):
            cx = XMIN + x * (XMAX - XMIN) / WIDTH
            cy = YMIN + y * (YMAX - YMIN) / HEIGHT
            c = complex(cx, cy)
            z = 0j
            color = 0
            for _i in range(MAX_ITERATIONS):
                if abs(z) > 2.0:
                    break
                z = z * z + c
                color += 1
            image[y][x] = color
    return image


def write_image_to_file(image: list[list[int]]) -> None:
    with open("mandelbrot.txt", "w") as file:
        for row in image:
            for col in row:
                if col == MAX_ITERATIONS:
                    file.write(" ")
                else:
                    file.write(str(col) + " ")
            file.write("\n")


def main() -> None:
    image = create_image()
    write_image_to_file(image)


if __name__ == "__main__":
    main()
