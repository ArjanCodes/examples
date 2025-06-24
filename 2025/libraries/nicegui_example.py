from nicegui import ui

ui.label("Hello from NiceGUI!")
ui.button("Click me", on_click=lambda: ui.notify("Clicked!"))
ui.run()
