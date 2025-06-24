from textual.app import App
from textual.widgets import Static


class MyApp(App):
    def compose(self):
        yield Static("Hello from Textual!")


MyApp().run()
