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
        self.listbox_has_focus = False
        self.root.bind_all("<Button-1>", lambda e: hasattr(e.widget, "focus_set") and e.widget.focus_set())

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
        self.marker_img= ImageTk.PhotoImage(Image.open("self_marker.png"))
        self.king_navbar= ImageTk.PhotoImage(Image.open("nav_bar.png"))
        self.peters_navbar=ImageTk.PhotoImage(Image.open("navbar_peter.png"))
        self.talcott_navbar=ImageTk.PhotoImage(Image.open("navbar_talcott.png"))
        self.search_bar_img = ImageTk.PhotoImage(Image.open("search_bar.png"))
        self.class_menu_img = ImageTk.PhotoImage(Image.open("class_menu.png"))
        self.edit_icon = ImageTk.PhotoImage(Image.open("edit_icon.png").resize((40, 40), Image.Resampling.LANCZOS))
        self.delete_icon = ImageTk.PhotoImage(Image.open("delete_icon.png").resize((33, 40), Image.Resampling.LANCZOS))
        self.navbar_x = ImageTk.PhotoImage(Image.open("navbar_x.png"))

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
        self.valid_locations = ["Barrows Hall", "Peters Hall","Kade Haus", "Keep Cottage", "Khan Hall", "Knowlton", "King Building", "Talcott Hall"]
        self.marker=self.map_widget.set_marker(41.295728, -82.221735, icon=self.marker_img)

    def under_construction(self):
        # Create popup frame
        self.under_construction_popup = tkinter.Frame(
            self.root,
            bg="white",
            width=300,
            height=200,
            highlightthickness=2,
            highlightbackground="black"
        )
        self.under_construction_popup.place(relx=0.5, rely=0.5, anchor="center")

        label = tkinter.Label(
            self.under_construction_popup,
            text="Under Construction",
            font=("Arial", 18, "bold"),
            bg="white"
        )
        label.pack(pady=30)

        close_button = tkinter.Label(
            self.under_construction_popup,
            image=self.close_btn_img,
            bd=0,
            bg="white"
        )
        close_button.pack()
        close_button.bind("<Button-1>", lambda e: self.under_construction_popup.place_forget())


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

        self.class_menu_bg=tkinter.Label(
            self.class_menu,
            image=self.class_menu_img,
            bd=0
        )
        self.class_menu_bg.place(relx=0.5, rely=0.15, anchor=tkinter.N)

        
        
        #class menue classes
        your_events = [
            Event("CS 150", "King Building", "9:00", "101", "MWF"),
            Event("ENGL 140", "King Building", "13:00", "106", "TT"),
            Event("Math 210", "Peters Hall", "10:00", "232", "MWF"),
            Event("History 108", "Peters Hall", "14:00", "102", "MWF")
        ]#used list instead of touple (original ver) to make easier to add
        self.your_events = your_events#a list of events that you have
        self.ClassSelectedToDeleat = None#the last class that the user selected to deleat
        #commented out to handle this dynamically in locations() (so easier to add new ones)
        """
        for i in range(4):
            currClassLable = tkinter.Label(self.class_menu, text=your_events[i].description, font=("Times New Roman", 50, ""))
            self.__setattr__("class" + str(i) + "lable", currClassLable)
            currClassLable.grid(row=i, column=0, columnspan=5)
            currClassLable.bind("<Button-1>", lambda interactEvent, event=your_events[i]: self.selectedClass(event))
            curr_edit_lable = tkinter.Label(self.class_menu, image=self.edit_icon)
            curr_edit_lable.grid(row=i, column=6)
            curr_edit_lable.bind("<Button-1>", lambda interactEvent, event=your_events[i]: self.edit_event(event))
            curr_deleat_lable = tkinter.Label(self.class_menu, image=self.delete_icon)
            curr_deleat_lable.grid(row=i, column=7)
            curr_deleat_lable.bind("<Button-1>", lambda interactEvent, event=your_events[i]: self.pressed_deleat_class(event))
        """


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
            width=200,
            height= 200,
        )
        self.deleat_class_confermation.place()
        self.deleat_class_confermation_text = tkinter.Label(
            self.deleat_class_confermation,
            text="Are you sure you want to delete this class?",
            font=("Arial", 20, ""),
        )
        self.deleat_class_confermation_text.grid(row=0, column=0)
        self.deleat_class_confermation_yes_button = tkinter.Button(
            self.deleat_class_confermation,
            text="yes",
            font=("Arial", 28, ""),
            command= lambda: self.deleat_class()
        )
        self.deleat_class_confermation_yes_button.grid(row=1, column=0)
        self.deleat_class_confermation_no_button = tkinter.Button(
            self.deleat_class_confermation,
            text="no",
            font=("Arial", 28, ""),
            command = lambda: self.close_confermation_window()
        )
        self.deleat_class_confermation_no_button.grid(row=2, column=0)

        #edit event page
        self.editEventPage = tkinter.Frame(
            self.root,
            #self.root,
            bg="white",
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
    
    def close_class_menu(self, show_menu_button=True):
        self.class_menu.place_forget()
        if show_menu_button:
            self.menu.place(x=10, y=610)

    def locations(self):
        """
        displays the list of diffrent classes(assumes not alredy displayed)
        """
        
        #has to rebuild menu so new added classes are visible
        for x in self.class_menu.winfo_children():
            x.destroy()
        #re-add background
        self.class_menu_bg = tkinter.Label(
            self.class_menu,
            image=self.class_menu_img,
            bd=0
        )
        self.class_menu_bg.place(x=0, y=0, relwidth=1, relheight=1)
        #create scroll canvas for classes
        canvas = tkinter.Canvas(self.class_menu, borderwidth=0)
        scroll_frame = tkinter.Frame(canvas, bg="white")
        scroll_frame.columnconfigure(0, weight=1)

        scrollbar = tkinter.Scrollbar(self.class_menu, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scroll_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        
        self.close_submenu()
        
        #self.class_menu.place(relx=.5, rely=.15, anchor=tkinter.N, relwidth=.6, relheight=.7)
        self.class_menu.place(relx=.5, rely=.15, anchor=tkinter.N, width=380, height=488)
        tkinter.Label(scroll_frame, text="", bg="white").grid(row=0, column=0, columnspan=8, pady=(30, 5)) #blank row for padding at top
        for i, event in enumerate(self.your_events):
            row_index = i * 2 + 1  # two rows per event

            # Class name
            class_name_label = tkinter.Label(
                scroll_frame,
                text=event.description,
                font=("Arial", 20, "bold"),
                bg="white",
                anchor="w"
            )
            class_name_label.grid(row=row_index, column=0, columnspan=5, sticky="w", padx=10, pady=(15, 0))
            class_name_label.bind("<Button-1>", lambda e, ev=event: self.selectedClass(ev))

            # Class details 
            details_text = f"{event.location} {event.roomNumber} • {event.weekday.upper()} @ {event.time}"
            class_details_label = tkinter.Label(
                scroll_frame,
                text=details_text,
                font=("Arial", 14),
                bg="white",
                fg="gray20",
                anchor="w"
            )
            class_details_label.grid(row=row_index + 1, column=0, columnspan=5, sticky="w", padx=20, pady=(0, 10))
            class_details_label.bind("<Button-1>", lambda e, ev=event: self.selectedClass(ev))

            # Edit button 
            edit_btn = tkinter.Label(scroll_frame, image=self.edit_icon, bg="white")
            edit_btn.grid(row=row_index, column=6, rowspan=2, sticky="n", padx=5, pady=(15, 0))
            edit_btn.bind("<Button-1>", lambda e, ev=event: self.edit_event(ev))

            # Delete button
            delete_btn = tkinter.Label(scroll_frame, image=self.delete_icon, bg="white")
            delete_btn.grid(row=row_index, column=7, rowspan=2, sticky="n", padx=5, pady=(15, 0))
            delete_btn.bind("<Button-1>", lambda e, ev=event: self.pressed_deleat_class(ev))

            
        #add location button
        self.add_location_button = tkinter.Button(
            self.class_menu,
            text="+",
            font=("Arial", 50),
            bg="white",
            bd=0,
            command=self.add_event
        )
        self.add_location_button.place(relx=0.5, rely=0.95, anchor="center")
        

            
        #self.class_menu.pack()
        header_label = tkinter.Label(
            self.class_menu,
            text="My Locations",
            font=("Arial", 24, "bold"),
            width=388,
            bg="white",
            fg="black"
)       
        header_label.place(relx=0.5, rely=0.05, anchor="n")

        #close menu button
        self.close_btn = tkinter.Label(
            self.class_menu,
            image=self.close_btn_img,
            bd=0,
            bg="white"
        )
        self.close_btn.place(relx=0.95, rely=0.05, anchor=tkinter.CENTER)
        self.close_btn.bind("<Button-1>", lambda e: self.close_class_menu())

    def go_To_Class(self, class_to_navigate):
        print("Start Navigation for Next Event", class_to_navigate)
        #TODO buld navagation feture
        self.navigate(class_to_navigate.location, class_to_navigate.description, class_to_navigate.roomNumber) #goes to placeholder navigation

    def next_class(self):
        self.close_submenu()
        self.navigate("King Building", "CS150", "101")

    def selectedClass(self, chosesClass):#for when the user selects a spsific class they wish to travel to
        self.close_class_menu(show_menu_button=False) #stops from reappearing hamburger menu too earlier
        self.go_To_Class(chosesClass)

        self.close_submenu()
        #self.navigate() already called in go_To_class

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
            self.navigate(selected_text, selected_text, "")
            

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
        self.close_class_menu(show_menu_button=False) #prevents menu from reappearing prematurely
        self.event_name_lable = tkinter.Label(
            self.editEventPage,
            text="Name of Event:",
            font=("Arial", 18, ""),
            anchor="w",
            borderwidth=6,
            bg="white"
        )
        self.event_name_enter = tkinter.Entry(
            self.editEventPage,
            width=18
        )
        self.event_name_lable.grid(column=0, row=0,sticky="w")
        self.event_name_enter.grid(row=0, column=1)


        self.event_bulding_lable = tkinter.Label(
            self.editEventPage,
            text="Building:",
            font=("Arial",18, ""),
            anchor="w",
            borderwidth=6,
            bg="white"
        )
        self.event_bulding_enter = tkinter.Entry(
            self.editEventPage,
            width=18
        )
        self.event_bulding_lable.grid(column=0, row=1, sticky="w")
        self.event_bulding_enter.grid(row=1, column=1)

        
        self.event_room_number_lable = tkinter.Label(
            self.editEventPage,
            text="Room number:",
            font=("Arial",18, ""),
            anchor="w",
            borderwidth=6,
            bg="white"
        )
        self.event_room_number_enter = tkinter.Entry(
            self.editEventPage,
            width=18
        )
        self.event_room_number_lable.grid(column=0, row=2, sticky="w")
        self.event_room_number_enter.grid(row=2, column=1)

        
        self.event_time_lable = tkinter.Label(
            self.editEventPage,
            text="Time:",
            font=("Arial", 18, ""),
            anchor="w",
            borderwidth=6,
            bg="white"
        )
        self.event_time_enter = tkinter.Entry(
            self.editEventPage,
            width=18
        )
        self.event_time_lable.grid(column=0, row=3, sticky="w")
        self.event_time_enter.grid(row=3, column=1)
        
        self.event_weekday_lable = tkinter.Label(
            self.editEventPage,
            text="Day of week:",
            font=("Arial", 18, ""),
            anchor="w",
            borderwidth=6,
            bg="white"
        )
        self.event_weekday_enter = tkinter.Entry(
            self.editEventPage,
            width=18
        )
        self.event_weekday_lable.grid(column=0, row=4, sticky="w")
        self.event_weekday_enter.grid(row=4, column=1)

        self.confirm_changes_button = tkinter.Button(
        self.editEventPage,
        text="confirm changes",
        font=("Arial", 20, ""),
        borderwidth=6,
        background="green",
        command= lambda: self.update_event_info(event)
        )
        self.undo_changes_button = tkinter.Button(
            self.editEventPage,
            text="undo changes",
            font=("Arial", 20, ""),
            borderwidth=6,
            background="red",
            command= lambda: self.set_boxes(event),
        )
        self.confirm_changes_button.grid(column=0, row=5)
        self.undo_changes_button.grid(row=5, column=1)

        self.editEventPage.place(relx=.5, rely=.15, anchor="n", width=380, height=488)

        self.set_boxes(event)
        
    def add_event(self):
        new_event = Event("", "", "", "", "")
        self.your_events.append(new_event)
        self.edit_event(new_event)

    def set_boxes(self, event):
        self.event_name_enter.delete(0, tkinter.END)
        self.event_name_enter.insert(0, event.description)

        self.event_bulding_enter.delete(0, tkinter.END)
        self.event_bulding_enter.insert(0, event.location)

        self.event_room_number_enter.delete(0, tkinter.END)
        self.event_room_number_enter.insert(0, event.roomNumber)

        self.event_time_enter.delete(0, tkinter.END)
        self.event_time_enter.insert(0, event.time)

        self.event_weekday_enter.delete(0, tkinter.END)
        self.event_weekday_enter.insert(0, event.weekday)

    def update_event_info(self, event):
        """
        called when the user updeste the info about a class
        intended to update the info that is stored about that class
        to whatever the user input
        """
        event.description = self.event_name_enter.get()
        event.location = self.event_bulding_enter.get()
        event.time = self.event_time_enter.get()
        event.roomNumber = self.event_room_number_enter.get()
        event.weekday = self.event_weekday_enter.get()
        self.editEventPage.place_forget()
        self.locations()


        

        
        
        

        

    def navigate(self, location, label, number):
        self.search_bar_frame.place_forget()
        navigate = True
        if "King" in location:
            self.navbar_img=self.king_navbar
            if number != "":
                self.dest=self.map_widget.set_marker(41.29225950788716, -82.22067847961983, text=label + " - King " + number)
            else:
                self.dest=self.map_widget.set_marker(41.29225950788716, -82.22067847961983, text=label)
            self.map_widget.set_position(41.2939542, -82.2211778)
            self.map_widget.set_zoom(17)
            self.path_1 = self.map_widget.set_path([self.marker.position, (41.2954777, -82.2214728), (41.2953729, -82.2215587), (41.2937607, -82.2215265), (41.2934383, -82.2210651), (41.2924307, -82.2211081), self.dest.position,])
        elif "Peters" in location:
            self.navbar_img=self.peters_navbar
            if number != "":
                self.dest = self.map_widget.set_marker(41.2930514, -82.2207326, text=label + " - Peters " + number)
            else:
                self.dest = self.map_widget.set_marker(41.2930514, -82.2207326, text=label)
            self.map_widget.set_position(41.2945104, -82.2210759)
            self.map_widget.set_zoom(17)
            self.path_1 = self.map_widget.set_path([self.marker.position, (41.2954777, -82.2214728), (41.2953729, -82.2215587), (41.2937607, -82.2215265), (41.2934383, -82.2210651), (41.2929627, -82.2210759), self.dest.position,])
        elif "Talcott" in location:
            self.navbar_img=self.talcott_navbar
            self.dest = self.map_widget.set_marker(41.2914643, -82.2205346, text=label)
            self.map_widget.set_position(41.2939453, -82.2212714)
            self.map_widget.set_zoom(17)
            self.path_1 = self.map_widget.set_path([self.marker.position, (41.2954777, -82.2214728), (41.2953729, -82.2215587), (41.2937607, -82.2215265), (41.2934383, -82.2210651), (41.2916336, -82.2211569), (41.2916094, -82.2209101), self.dest.position,])
        else:
            navigate=False
            self.under_construction()
            self.close_navigation()
        if navigate:
            self.navbar_frame=tkinter.Frame(self.root, width=400, height=200, bg="white")
            #add invisible close button (x is already in image)
            self.navbar=tkinter.Label(
                self.navbar_frame,
                image=self.navbar_img,
                bd=0
            )
            self.navbar.pack()
            self.nav_close_btn = tkinter.Label(
                self.navbar_frame,
                image=self.navbar_x,
            )
            self.nav_close_btn.place(relx=0.8, rely=0.5, anchor="center")
            self.nav_close_btn.bind("<Button-1>", lambda e: self.close_navigation())
            self.navbar_frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)




    #cleans up/closes sample navigation
    def close_navigation(self):
        self.navbar_frame.destroy()
        if hasattr(self, "path_1"):
            self.path_1.delete()
        if hasattr(self, "dest"):
            self.dest.delete()
        self.menu.place(x=10, y=610)
        self.search_bar_frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)


class Event:#used for keeping track of information about a single event(class) in one place
    def __init__(self, description, location, time, roomNumber, weekDay):
        self.description = description
        self.location = location #
        self.time = time
        self.roomNumber = roomNumber
        self.weekday = weekDay



app = CampusMap()
app.root.mainloop()

