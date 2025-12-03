
import tkinter as tk

from graphics import GraphicsRenderer, ShapeData, Color


def main() -> None:
    root = tk.Tk()
    root.title("ShapyMcShapeface Renderer")

    canvas_width = 800
    canvas_height = 600

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    renderer = GraphicsRenderer(canvas)

    # ------------------------------------------------------------
    # Define a few shapes
    # ------------------------------------------------------------

    square_points: ShapeData = [(250, 200), (350, 200), (350, 300), (250, 300)]
    square_color: Color = "#444444"

    triangle_points: ShapeData = [(500, 250), (550, 350), (450, 350)]
    triangle_color: Color = "#888888"

    # ------------------------------------------------------------
    # Render shapes using the renderer
    # ------------------------------------------------------------

    renderer.render("square", square_points, square_color)
    renderer.render("triangle", triangle_points, triangle_color)

    root.mainloop()


if __name__ == "__main__":
    main()