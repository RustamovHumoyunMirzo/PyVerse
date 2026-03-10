from pyverse.core import App
from pyverse.core import Window

app = App()

win = Window(800, 600)

def show_main_window():
    print("App launched! Showing window...")
    win.show()

app.on("launch", show_main_window)
app.on("destroy", lambda: print("App is closing..."))

app.run()