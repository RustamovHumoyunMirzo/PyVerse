from pyverse.core import App, Window

app = App()

win = Window(800, 600)

@app.on("launch")
def on_launch():
    print("App launched!")

def on_quit():
    print("App is quitting...")

app.on("quit", on_quit)

app.run()