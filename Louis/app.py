import tkinter
from PIL import Image, ImageTk
import tkintermapview

class CampusMap:
    def __init__(self):
        self.width = 405
        self.height = 720
        self.root = tkinter.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.submenu_visible = False

        self.load_assets()
        self.setup_map()
        self.create_ui()

    def load_assets(self):
        self.menu_btn_img = ImageTk.PhotoImage(Image.open("menu_button.png"))
        self.submenu_bg_img = ImageTk.PhotoImage(Image.open("submenu_bg.png"))
        self.close_btn_img = ImageTk.PhotoImage(Image.open("close_button.png"))
        self.locations_btn_img = ImageTk.PhotoImage(Image.open("my_locations.png"))
        self.next_btn_img = ImageTk.PhotoImage(Image.open("next_event.png"))
        self.search_bar_img= ImageTk.PhotoImage(Image.open("search_bar.png"))

    def setup_map(self):
        self.map_widget = tkintermapview.TkinterMapView(
            self.root,
            width=self.width,
            height=self.height,
            corner_radius=0
        )
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(41.295741, -82.22184)
        self.map_widget.set_zoom(18)


    def create_ui(self):
        #menu button
        self.menu = tkinter.Label(
            self.root, 
            image=self.menu_btn_img,
            bd=0
        )
        self.menu.place(x=10, y=610)
        self.menu.bind("<Button-1>", lambda e: self.open_submenu())

        #submenu
        submenu_bg_width=self.submenu_bg_img.width()
        submenu_bg_height=self.submenu_bg_img.height()

        self.submenu = tkinter.Frame(
            self.root, 
            bg="white", 
            bd=0,
            width=submenu_bg_width,
            height=submenu_bg_height
            )
        self.submenu_bg_label=tkinter.Label(
            self.submenu,
            image=self.submenu_bg_img,
            bd=0
        )
        self.submenu_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #close submenu
        self.close_btn = tkinter.Label(
            self.submenu,
            image=self.close_btn_img,
            bd=0,
            bg="white"
        )
        self.close_btn.place(relx=0.85, rely=0.15, anchor=tkinter.CENTER)
        self.close_btn.bind("<Button-1>", lambda e: (self.close_submenu(), self.menu.place(x=10, y=610)))

        #my locations
        self.my_locations_btn = tkinter.Label(
            self.submenu,
            image=self.locations_btn_img,
            bg="white"
        )
        self.my_locations_btn.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)
        self.my_locations_btn.bind("<Button-1>", lambda e: self.locations())

        #take me to my next event
        self.next_event_btn = tkinter.Label(
            self.submenu,
            image=self.next_btn_img,
            bg="white"
        )
        self.next_event_btn.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.next_event_btn.bind("<Button-1>", lambda e: self.next_class())

        #search bar
        self.search_bar = tkinter.Label(
            self.root,
            image=self.search_bar_img,
        )
        self.search_bar.place(relx = 0.5, rely= 0.1, anchor=tkinter.CENTER)

    def open_submenu(self):
        self.menu.place_forget() #hide the menu button
        self.submenu.place(x=205, y=550, anchor=tkinter.CENTER)
        self.root.update_idletasks() #for button responsiveness
    
    def close_submenu(self):
        self.submenu.place_forget() 
        self.root.update_idletasks()

    def locations(self):
        print("Open Locations Menu")
        self.close_submenu()

    def next_class(self):
        print("Start Navigation for Next Event")
        self.close_submenu()

app = CampusMap()
app.root.mainloop()
