import tkinter as tk
#import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage


canviseSize = (750, 700)

def callback():
    message = tk.Label(root, text="Hello, World!")
    message.pack()
    
def openMenu():
    canvas.create_rectangle(((canviseSize[0]//2) - (min(canviseSize[0], 500)//2), 0), (min(canviseSize[0], 500), min(canviseSize[1], 900)), fill='white', tags="menu")
    canvas.lift("menu")

root = tk.Tk()

lf = ttk.LabelFrame(root, text='Alignment')

canvas = tk.Canvas(root, width=canviseSize[0], height=canviseSize[1], bg="white")

root.geometry('1200x750')
root.resizable(False, False)
# tk.Label(root, text='Classic Label').pack()
# ttk.Label(root, text='Themed Label').pack()
button = ttk.Button(
   root, 
   text="button3",
   command=callback
)
button.pack(
    #expand=True
)


menueButtonImage = PhotoImage(file="menuButtonS.png")

button2 = ttk.Button(
    canvas,
    text="here is the text",
    command=openMenu,
    image=menueButtonImage,
)


mapImage = PhotoImage(file="tempMap2.png")
imageWidth = mapImage.width()
imageHeight = mapImage.height()



image = tk.Label(canvas, image=mapImage)
#image.pack(expand=True)

canvas.pack()

#canvas.create_window((0, 0), window=image, anchor='center')
canvas.create_image((canviseSize[0]//2, canviseSize[1]//2), image=mapImage)
canvas.create_window((canviseSize[0]-50, canviseSize[1]-50), window=button2, anchor='nw')

menueImage = ttk.Label(master=root, text="Mmmmmmmmmmmmmmmmmmmm")
menueImage.place(width=10, height=10, anchor="se")


#button2.place(x=850, y=600)#TODO firure how to dynamicly place this in the location of the map, or decided on the size of the map and work from there

message = tk.Label(image, text="Hello, World!")
# message.pack()
# root.title('world map')



root.mainloop()