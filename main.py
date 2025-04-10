import tkinter as tk
import tkinter as tk
from tkinter import ttk

def callback():
    message = tk.Label(root, text="Hello, World!")
    message.pack()
    

root = tk.Tk()

tk.Label(root, text='Classic Label').pack()
ttk.Label(root, text='Themed Label').pack()
button = ttk.Button(
   root, 
   text="button3",
   command=callback
)
button.pack(
    ipadx=5,
    ipady=5,
)

message = tk.Label(root, text="Hello, World!")
# message.pack()
# root.title('world map')



root.mainloop()