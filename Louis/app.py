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
        your_events = (Event("CS 150 King 101", "King Building", "9:00", "101", "mwf"), Event("CS 000 King 101", "King Building", "9:00", "101", "tt"), Event("Math 210 peters 232", "peters Hall", "10:00", "232", "mwf"), Event("History 108 Peters Hall 102", "peters Hall", "14:00", "102", "mwf"))#touple, cause I want it to be immutable
        self.your_events = your_events#a list of events that you have
        self.ClassSelectedToDeleat = None#the last class that the user selected to deleat
        for i in range(4):
            currClassLable = tkinter.Label(self.class_menu, text=your_events[i].description, font=("Times New Roman", 50, ""))
            currClassLable.grid(row=i, column=0, columnspan=5)
            currClassLable.bind("<Button-1>", lambda interactEvent : self.selectedClass(your_events[i]))
            curr_edit_lable = tkinter.Label(self.class_menu, image=self.edit_icon)
            curr_edit_lable.grid(row=i, column=6)
            curr_edit_lable.bind("<Button-1>", lambda interactEvent : self.edit_event(your_events[i]))
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

        #confermation
        self.deleat_class_confermation = tkinter.Frame(
            self.root,
            bg="white",
            width=380,
            height= 200,
        )
        self.deleat_class_confermation.place()
        self.deleat_class_confermation_text = tkinter.Label(
            self.deleat_class_confermation,
            text="are your sure you want to DELEAT this class?",
            font=("Times New Roman", 50, ""),
        )
        self.deleat_class_confermation_text.grid(row=0, column=0)
        self.deleat_class_confermation_yes_button = tkinter.Button(
            self.deleat_class_confermation,
            text="yes",
            font=("Times New Roman", 50, ""),
            command= lambda: self.deleat_class()
        )
        self.deleat_class_confermation_yes_button.grid(row=1, column=0)
        self.deleat_class_confermation_no_button = tkinter.Button(
            self.deleat_class_confermation,
            text="no",
            font=("Times New Roman", 50, ""),
            command = lambda: self.close_confermation_window()
        )
        self.deleat_class_confermation_no_button.grid(row=2, column=0)

        #edit event page
        self.editEventPage = tkinter.Frame(
            self.root,
            #self.root,
            bg="black",
            # width=380,
            # height= 200,
        )






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
        self.class_menu.place_forget()

    def locations(self):
        self.close_submenu()
        self.class_menu.place(relx=.5, rely=.15, anchor=tkinter.N, relwidth=.6, relheight=.7)
        #self.class_menu.pack()

    def go_To_Class(self, class_to_navigate):
        print("Start Navigation for Next Event", class_to_navigate)
        #TODO buld navagation feture

    def next_class(self):
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
        """
        for when the button thta openes the deleat a class windown is pressed, 
        opens the confermation window
        """
        self.ClassSelectedToDeleat = event
        self.deleat_class_confermation.place(relx=0.5, rely=0.4, anchor="center")

    def deleat_class(self):#will deleat class in future
        self.close_confermation_window()
        #adding soon

    def close_confermation_window(self):#closes the conermation window
        self.deleat_class_confermation.place_forget()

    def edit_event(self, event):
        """
        brings up screen that allows you to edit the event clicked on
        """
        print("funct edit event called")
        self.close_class_menu()
        self.event_name_lable = tkinter.Label(
            self.editEventPage,
            text="Name of Event:",
            font=("Times New Roman", 40, ""),
            borderwidth=6,
        )
        self.event_name_enter = tkinter.Entry(
            self.editEventPage,
            width=30
        )
        self.event_name_lable.grid(column=0, row=0)
        self.event_name_enter.grid(row=0, column=1)


        self.event_bulding_lable = tkinter.Label(
            self.editEventPage,
            text="Bulding:",
            font=("Times New Roman", 40, ""),
            borderwidth=6,
        )
        self.event_bulding_enter = tkinter.Entry(
            self.editEventPage,
            width=30
        )
        self.event_bulding_lable.grid(column=0, row=1)
        self.event_bulding_enter.grid(row=1, column=1)

        
        self.event_room_number_lable = tkinter.Label(
            self.editEventPage,
            text="Room number:",
            font=("Times New Roman", 40, ""),
            borderwidth=6,
        )
        self.event_room_number_enter = tkinter.Entry(
            self.editEventPage,
            width=30
        )
        self.event_room_number_lable.grid(column=0, row=2)
        self.event_room_number_enter.grid(row=2, column=1)

        
        self.event_time_lable = tkinter.Label(
            self.editEventPage,
            text="Time:",
            font=("Times New Roman", 40, ""),
            borderwidth=6,
        )
        self.event_time_enter = tkinter.Entry(
            self.editEventPage,
            width=30
        )
        self.event_time_lable.grid(column=0, row=3)
        self.event_time_enter.grid(row=3, column=1)

        
        self.event_weekday_lable = tkinter.Label(
            self.editEventPage,
            text="Day of week:",
            font=("Times New Roman", 40, ""),
            borderwidth=6,
        )
        self.event_weekday_enter = tkinter.Entry(
            self.editEventPage,
            width=30
        )
        self.event_weekday_lable.grid(column=0, row=4)
        self.event_weekday_enter.grid(row=4, column=1)
        self.editEventPage.place(relx=.5, rely=.15, anchor="n", relheight=.7, relwidth=.5)

        
        
        
        

        

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



class Event:#used for keeping track of information about a single event(class) in one place
    def __init__(self, description, location, time, roomNumber, weekDay):
        self.description = description
        self.location = location
        self.time = time
        self.roomNumber = roomNumber
        self.weekday = weekDay



app = CampusMap()
app.root.mainloop()

