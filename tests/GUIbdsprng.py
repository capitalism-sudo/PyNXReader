import json
import signal
import sys
import tkinter as tk
from tkinter import ttk
from tables import locations,diff_held_items

# Go to root of PyNXReader
sys.path.append('../')

from nxreader import NXReader
from rng import XOROSHIRO,OverworldRNG,Filter
from rng import Xorshift,BDSPStationaryGenerator
from gui import ChecklistCombobox

rng_pointer = "[main+4F8CCD0]"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.config = json.load(open("../config.json"))
        self.master = master
        self.pack()
        self.advances = 0
        self.create_widgets()
        signal.signal(signal.SIGINT, self.signal_handler)

    def create_widgets(self):
        ttk.Style().configure("Connect.TButton", foreground="green")
        ttk.Style().configure("Disconnect.TButton", foreground="red")
        self.master.title("Overworld RNG")
        self.connect_button = ttk.Button(self, text="Connect", style="Connect.TButton", command=self.connect)
        self.connect_button.grid(column=0,row=1)
        self.quit = ttk.Button(self, text="Disconnect", style="Disconnect.TButton", command=self.disconnect)
        self.quit.grid(column=1,row=1)
        self.generate = ttk.Button(self, text="Generate", command=self.generate,width=20)
        self.generate.grid(column=2,row=1,columnspan=2)
#        self.shiny_charm_var = tk.IntVar()
#        self.mark_charm_var = tk.IntVar()
#        self.weather_active_var = tk.IntVar()
#        self.is_static_var = tk.IntVar()
#        self.is_fishing_var = tk.IntVar()
#        self.diff_held_item_var = tk.IntVar()
#        self.double_mark_gen_var = tk.IntVar()
#        self.is_legendary_var = tk.IntVar()
#        self.is_shiny_locked_var = tk.IntVar()
#        ttk.Checkbutton(self, text="Shiny Charm", variable=self.shiny_charm_var).grid(column=0,row=2,columnspan=2)
#        ttk.Checkbutton(self, text="Mark Charm", variable=self.mark_charm_var).grid(column=2,row=2,columnspan=2)
#        ttk.Checkbutton(self, text="Is Static", variable=self.is_static_var).grid(column=0,row=3,columnspan=2)
#        ttk.Checkbutton(self, text="Is Legendary", variable=self.is_legendary_var).grid(column=2,row=3,columnspan=2)
#        ttk.Checkbutton(self, text="Weather Active", variable=self.weather_active_var).grid(column=0,row=4,columnspan=2)
#        ttk.Checkbutton(self, text="Is Fishing", variable=self.is_fishing_var).grid(column=2,row=4,columnspan=2)
#        ttk.Checkbutton(self, text="Rand Held Item", variable=self.diff_held_item_var).grid(column=0,row=5,columnspan=2)
#        ttk.Checkbutton(self, text="Double Mark Gen", variable=self.double_mark_gen_var).grid(column=2,row=5,columnspan=2)
#        ttk.Checkbutton(self, text="Is Shiny Locked", variable=self.is_shiny_locked_var).grid(column=0,row=6,columnspan=4)
        ttk.Label(self, text="Level:").grid(column=0,row=10)
        self.min_level_var = tk.Spinbox(self, from_= 1, to = 100, width = 5)
        self.max_level_var = tk.Spinbox(self, from_= 1, to = 100, width = 5)
        self.min_level_var.grid(column=1,row=10)
        self.max_level_var.grid(column=2,row=10)
        ttk.Label(self,text="Filter").grid(column=5,row=1,columnspan=3)
        ttk.Label(self,text="Shininess").grid(column=4,row=2,columnspan=1)
        self.shiny_filter = ttk.Combobox(self,state='readonly',values=["Any","Star","Square","Star/Square"])
        self.shiny_filter.grid(column=5,row=2,columnspan=3)
        self.shiny_filter.set("Any")
#        ttk.Label(self,text="Mark").grid(column=4,row=3,columnspan=1)
#        self.mark_var = ChecklistCombobox(self,state='readonly',values=["Rare","Uncommon","Weather","Time","Fishing"]+OverworldRNG.personality_marks)
#        self.mark_var.grid(column=5,row=3,columnspan=3)
#        self.all_mark_button = ttk.Button(self,text="All",width=20//3,command=lambda: self.mark_var.set(["Rare","Uncommon","Weather","Time","Fishing"]+OverworldRNG.personality_marks))
#        self.all_mark_button.grid(column=6,row=4,columnspan=1)
#        self.all_mark_button = ttk.Button(self,text="None",width=20//3,command=lambda: self.mark_var.set([]))
#        self.all_mark_button.grid(column=7,row=4,columnspan=1)
#        self.slot_filter = tk.IntVar()
#        ttk.Checkbutton(self, text="Slot", variable=self.slot_filter).grid(column=4,row=6)
#        self.min_slot_var = tk.Spinbox(self, from_= 0, to = 99, width = 5)
#        self.max_slot_var = tk.Spinbox(self, from_= 0, to = 99, width = 5)
#        self.min_slot_var.grid(column=6,row=6)
#        self.max_slot_var.grid(column=7,row=6)
        ttk.Label(self,text="Adv:").grid(column=3,row=10)
        self.advances_track = ttk.Label(self,text="0")
        self.advances_track.grid(column=4,row=10)
        ttk.Label(self,text="+").grid(column=5,row=10)
        self.max_advance_var = tk.Spinbox(self, value=99999, from_= 0, to = 99999999, width = 20)
        self.max_advance_var.grid(column=6,row=10,columnspan=2)
#        self.autofill = ttk.Button(self,text="Auto Fill Encounter Info",command=self.autofill_info)
#        self.autofill.grid(column=9,row=1)
#        ttk.Label(self,text="Location:").grid(column=8,row=2)
#        self.location = ttk.Combobox(self,values=[n for n in locations],width=40,state='readonly')
#        self.location.bind('<<ComboboxSelected>>',self.populate_weather)
#        self.location.grid(column=9,row=2)
#        ttk.Label(self,text="Weather:").grid(column=8,row=3)
#        self.weather = ttk.Combobox(self,values=[],width=40,state='readonly')
#        self.weather.grid(column=9,row=3)
#        ttk.Label(self,text="Species:").grid(column=8,row=4)
#        self.weather.bind('<<ComboboxSelected>>',self.populate_species)
#        self.species = ttk.Combobox(self,values=[],width=40,state='readonly')
#        self.species.grid(column=9,row=4)
        ttk.Label(self,text="Init:").grid(column=8,row=10)
        self.initial_display = ttk.Entry(self,width=40)
        self.initial_display.grid(column=9,row=10)
    
#    def populate_weather(self,event):
#        self.weather['values'] = [w for w in locations[self.location.get()]]
    
#    def populate_species(self,event):
#        self.species['values'] = [s for s in locations[self.location.get()][self.weather.get()][1]]
    
#    def autofill_info(self):
##        location = self.location.get()
#        weather = self.weather.get()
##        species = self.species.get()
#        self.is_static_var.set(0)
#        self.slot_filter.set(1)
#        if weather != "All Weather":
#            self.weather_active_var.set(1)
#        if weather == "Normal Weather":
#            self.weather_active_var.set(0)
#        if diff_held_items[species]:
##            self.diff_held_item_var.set(1)
#        else:
#            self.diff_held_item_var.set(0)
#        min_level,max_level = locations[location][weather][0]
#        self.min_level_var.delete(0,"end")
#        self.min_level_var.insert(0,min_level)
#        self.max_level_var.delete(0,"end")
#        self.max_level_var.insert(0,max_level)
#        min_slot,max_slot = locations[location][weather][1][species]
#        self.min_slot_var.delete(0,"end")
#        self.min_slot_var.insert(0,min_slot)
#        self.max_slot_var.delete(0,"end")
#        self.max_slot_var.insert(0,max_slot)

    def generate(self):
#        mark_filter = None
        # TODO: fix gui ew and full Filter functionality
#        selected = self.mark_var.get()
#        if selected != "":
#            if type(selected) == type(""):
#                selected = [selected]
#            mark_filter = selected
#        min_slot = max_slot = None
#        if int(self.slot_filter.get()):
#            min_slot = int(self.min_slot_var.get())
#            max_slot = int(self.max_slot_var.get())
        filter = Filter(
            shininess=self.shiny_filter.get() if self.shiny_filter.get() != "Any" else None,
            )
        self.predict = BDSPStationaryGenerator(
#            seed = self.rng.state(),
            *self.rng.seed(),
#            Xorshift(int.from_bytes(self.rng.state[:8], "little"), int.from_bytes(self.rng.state[8:], "little"))
#            tid = self.SWSHReader.TID,
#            sid = self.SWSHReader.SID,
#            shiny_charm = int(self.shiny_charm_var.get()),
#            mark_charm = int(self.mark_charm_var.get()),
#            weather_active = int(self.weather_active_var.get()),
#            is_fishing = int(self.is_fishing_var.get()),
#            is_static = int(self.is_static_var.get()),
#            is_legendary = int(self.is_legendary_var.get()),
#            is_shiny_locked = int(self.is_shiny_locked_var.get()),
#            min_level = int(self.min_level_var.get()),
#            max_level = int(self.max_level_var.get()),
#            diff_held_item = int(self.diff_held_item_var.get()),
#            double_mark_gen = int(self.double_mark_gen_var.get()),
#            filter = filter,
            )
        advances = self.advances
        self.predict.advance += advances
        for _ in range(int(self.max_advance_var.get())+1):
            state = self.predict.generate()
            if state:
                print(state)

    def connect(self):
        print("Connecting to: ", self.config["IP"])
        self.NXReader = NXReader(self.config["IP"])
        self.initial = self.NXReader.read_pointer(rng_pointer, 16)
#        self.rng = XOROSHIRO(int.from_bytes(self.SWSHReader.read(0x4C2AAC18,8),"little"),int.from_bytes(self.SWSHReader.read(0x4C2AAC18+8,8),"little"))
        self.rng = Xorshift(int.from_bytes(self.initial[:8], "little"), int.from_bytes(self.initial[8:], "little"))
#        self.initial = self.rng.state()
        self.initial_display.delete(0,"end")
#        self.initial_display.insert(0,hex(self.initial))
        self.advances = 0
        self.update()

    def disconnect(self):
        print("Disconnecting")
        self.after_cancel(self.after_token)
        self.NXReader.close(False)
        self.NXReader = None
    
    def signal_handler(self, signal, frame):
        self.disconnect()
        sys.exit(0)
    
    def update(self):
#        read = int.from_bytes(self.initial[:16], "little")
        curr = self.NXReader.read_pointer(rng_pointer, 16)
        read = int.from_bytes(curr[:16], "little")
#        print("reading... ", hex(read))
#        print("self rng state = ", hex(self.rng.state()))
        while self.rng.state() != read:
#            print("iteration ", self.advances)
            self.rng.next()
#            print("new rng state = ", hex(self.rng.state()))
            self.advances += 1
            if self.rng.state() == read:
#                print("read iteration ", rng.advances)
                self.advances_track['text'] = str(self.advances)
        self.after_token = self.after(100, self.update)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
