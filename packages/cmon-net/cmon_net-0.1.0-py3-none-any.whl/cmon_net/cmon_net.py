from textual.app import App, ComposeResult
from textual.widgets import Label, Header

class MyApp(App):
    TITLE="TOP"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("Boas vindas")


def app():
    MyApp().run()