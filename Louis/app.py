import tkinter
from PIL import Image, ImageTk
import tkintermapview

#import eventClass



class CampusMap:
    def __init__(self):
        self.width = 405
        self.height = 720
        self.root = tkinter.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.submenu_visible = False
        self.root.bind_all("<Button-1>", lambda e: e.widget.focus_set())

        self.load_assets()
        self.setup_map()
        self.create_ui()
        self.search_setup()

    def load_assets(self):
        self.menu_btn_img = ImageTk.PhotoImage(Image.open("menu_button.png"))
        self.submenu_bg_img = ImageTk.PhotoImage(Image.open("submenu_bg.png"))
        self.close_btn_img = ImageTk.PhotoImage(Image.open("close_button.png"))
        self.locations_btn_img = ImageTk.PhotoImage(Image.open("my_locations.png"))
        self.next_btn_img = ImageTk.PhotoImage(Image.open("next_event.png"))
        self.search_bar_img= ImageTk.PhotoImage(Image.open("search_bar.png"))
        self.navigation_img= ImageTk.PhotoImage(Image.open("navigation.png"))
        self.marker_img= ImageTk.PhotoImage(Image.open("self_marker.png"))
        self.navbar_img= ImageTk.PhotoImage(Image.open("nav_bar.png"))
        self.search_bar_img = ImageTk.PhotoImage(Image.open("search_bar.png"))
        self.class_menu_img = ImageTk.PhotoImage(Image.open("class_menu.png"))
        self.edit_icon = ImageTk.PhotoImage(Image.open("edit_icon.png"))
        self.delete_icon = ImageTk.PhotoImage(Image.open("delete_icon.png"))

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
        self.valid_locations = ["Barrows Hall", "Peters Hall","Kade Haus", "Keep Cottage", "Khan Hall", "Knowlton", "King Building"]
        self.marker=self.map_widget.set_marker(41.295728, -82.221735, icon=self.marker_img)



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

        #class menu
        self.class_menu = tkinter.Frame( 
            self.root,
            #image=self.class_menu_img,
            bg="white",
            width = self.class_menu_img.width(),
            height = self.class_menu_img.height(),
        )
        #class menue classes
        your_events = (Event("CS 150 King 101", "King Building"), Event("CS 150 King 101", "King Building"), Event("Math 210 King 232", "peters Hall"), Event("History 108 Peters Hall 102", "King Building"))#touple, cause I want it to be immutable
        #classDestinations = ("king", "king", "peters", "king")#note when you want to create the navagation system, this is where you put the data you need passed into your function to navagate
        for i in range(4):
            currClassLable = tkinter.Label(self.class_menu, text=your_events[i].description, font=("Times New Roman", 50, ""))
            currClassLable.grid(row=i, column=0, columnspan=5)
            currClassLable.bind("<Button-1>", lambda interactEvent : self.selectedClass(your_events[i]))
            curr_edit_lable = tkinter.Label(self.class_menu, image=self.edit_icon)
            curr_edit_lable.grid(row=i, column=6)
            curr_deleat_lable = tkinter.Label(self.class_menu, image=self.delete_icon)
            curr_deleat_lable.grid(row=i, column=7)
            curr_deleat_lable.bind("<Button-1>", lambda interactEvent : self.pressed_deleat_class(your_events[i]))


        #take me to my next event
        self.next_event_btn = tkinter.Label(
            self.submenu,
            image=self.next_btn_img,
            bg="white"
        )
        self.next_event_btn.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.next_event_btn.bind("<Button-1>", lambda e: self.next_class())

    def search_setup(self):
        self.search_bar_frame = tkinter.Frame(
            self.root,
            bg="white",
            bd=0,
            width=60,
        )
        self.search_bar_frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.search_bar = tkinter.Label(
            self.search_bar_frame,
            image=self.search_bar_img,
            bd=0,
        )
        self.search_bar.pack()
        self.searchbox = tkinter.Entry(self.root, font=("",20))
        self.searchbox.bind("<Button-1>", lambda e: (self.search()))
        self.searchbox.place(relx=0.57, rely=0.1,width = 180, anchor=tkinter.CENTER)

    def open_submenu(self):
        self.menu.place_forget() #hide the menu button
        self.submenu.place(x=205, y=550, anchor=tkinter.CENTER)
        self.map_widget.focus_set()
        self.root.update_idletasks() #for button responsiveness
    
    def close_submenu(self):
        self.submenu.place_forget() 
        self.map_widget.focus_set()
        self.root.update_idletasks()
    
    def close_class_menu(self):
        print("opened forget function")
        self.class_menu.place_forget()

    def locations(self):
        print("Open Locations Menu")
        self.close_submenu()
        self.class_menu.place(relx=.5, rely=.15, anchor=tkinter.N)
        #self.class_menu.pack()

    def go_To_Class(self, class_to_navigate):
        print("Start Navigation for Next Event", class_to_navigate)
        #TODO buld navagation feture

    def next_class(self):
        # print("Start Navigation for Next Event")
        # self.close_submenu()
        self.close_submenu()
        self.go_To_Class(None)#TODO buld and store what the "next class" is somewhere

    def selectedClass(self, chosesClass):#for when the user selects a spsific class they wish to travel to
        self.close_class_menu()
        self.go_To_Class(chosesClass)

        self.close_submenu()
        self.navigate()

    def search(self):
        self.search_has_focus = True
        self.root.update_idletasks()
        if not hasattr(self, 'listbox'):
            self.listbox = tkinter.Listbox(self.root, width=60, font=("", 20))
            self.listbox.place(relx=0.5, rely=0.14, width=259, height=125, anchor=tkinter.N)

            self.listbox.bind("<FocusOut>", lambda e: self.listbox_focus_out())
            self.listbox.bind("<Button-1>", lambda e: self.listbox_focus())
            self.listbox.bind("<<ListboxSelect>>", self.fillout)

            self.searchbox.bind("<FocusOut>", lambda e: self.search_focus_out())
            self.searchbox.bind("<KeyRelease>", self.check)
        #Autofill Suggestions

    def update(self, data):
        self.listbox.delete(0, tkinter.END)
        for item in data:
            self.listbox.insert(tkinter.END, item)
    
    def fillout(self, e):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_text = self.listbox.get(index)
            self.searchbox.delete(0, tkinter.END)
            self.searchbox.insert(0, selected_text)
            self.listbox.place_forget()
            self.map_widget.focus_set()
            if selected_text == "King Building":
                self.navigate()
            #else: display work in progress screen

    def check(self, e):
        typed= self.searchbox.get()

        if not hasattr(self, 'listbox') or not self.listbox.winfo_ismapped():
            self.listbox.place(relx=0.5, rely=0.14, width=259, height=125, anchor=tkinter.N)

        data=[]
        for item in self.valid_locations:
            if typed.lower() in item.lower():
                data.append(item)
        self.update(data)


    def listbox_focus(self):
        self.listbox_has_focus = True

    def search_focus_out(self):
        if not self.listbox_has_focus:
            self.listbox.place_forget()
        self.search_has_focus = False

    def listbox_focus_out(self):
        if not self.search_has_focus:
            self.listbox.place_forget()
        self.listbox_has_focus = False

    def pressed_deleat_class(self, event):
        print("presed Nuke")
        

        

    def navigate(self):
        self.search_bar_frame.place_forget()
        self.king=self.map_widget.set_marker(41.29225950788716, -82.22067847961983, text="King Building")
        self.map_widget.set_position(41.2939542, -82.2211778)
        self.map_widget.set_zoom(17)
        path_1 = self.map_widget.set_path([self.marker.position, (41.2954777, -82.2214728), (41.2953729, -82.2215587), (41.2937607, -82.2215265), (41.2934383, -82.2210651), (41.2924307, -82.2211081), self.king.position,])
        self.navbar_frame=tkinter.Frame(self.root, width=400, height=200, bg="white")
        self.navbar=tkinter.Label(
            self.navbar_frame,
            image=self.navbar_img,
            bd=0
        )
        self.navbar.pack()
        self.navbar_frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)



class Event:
    def __init__(self, description, location):
        self.description = description
        self.location = location



app = CampusMap()
app.root.mainloop()

