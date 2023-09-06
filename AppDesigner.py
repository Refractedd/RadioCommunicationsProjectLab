# import the formation library which loads the design for you
from formation import AppBuilder

def on_click(event):
    print("Button clicked")

app = AppBuilder(path="hello.xml")

app.connect_callbacks(globals()) # clicking the button will trigger the on_click function

print(app.myLabel["text"]) # outputs text in the label 'Hello world!'
print(app.myButton["text"]) # outputs text in the button 'Click me'

app.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()