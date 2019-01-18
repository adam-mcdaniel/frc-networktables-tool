"""
This project lets you try out Tkinter/Ttk and practice it!

Authors: David Fisher and PUT_YOUR_NAME_HERE.
"""  # TODO: 1. PUT YOUR NAME IN THE ABOVE LINE.

import os
import sys
import dill as pickle
import tkinter
from tkinter import ttk, Scale, Frame, Grid, N, S, E, W

from networktables import NetworkTables
NetworkTables.initialize(server='10.65.18.2')
sd = NetworkTables.getTable("SmartDashboard")


class NetworkSlider(Scale):
    def __init__(self, frame, entry="", slider=0, x=0, y=1, *args, **kwargs):
        super().__init__(frame, from_=0, to=1, digits=4, resolution = 0.001, orient=tkinter.HORIZONTAL, *args, **kwargs)
        self.grid(column=x+1, row=y, sticky=E+W, columnspan=3)

        self.entry = ttk.Entry(frame, justify=tkinter.LEFT)
        self.entry.insert(0, "")
        self.entry.grid(column=x, row=y, sticky=E+W)
        self.entry.insert(0, entry)
        self.set(slider)

    def destroy(self): super().destroy(); self.entry.destroy()

    # def update(self): pass # print(f"{self.get_name()}: {self.get_value()}")
    def update(self): sd.putNumber(self.get_name(), self.get_value())
    def get_name(self): return self.entry.get()
    def get_value(self): return self.get()
    def get_data(self): return self.get_name(), self.get_value()


class App(tkinter.Tk):
    def __init__(self, data=[], auto_push=False, title="NetworkTables Tuning Tool", w=200, h=400):
        self.height = 1
        self.auto_push = auto_push
        super().__init__()
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        self.after(50, self.update)
        self.title(title)

        self.frame = ttk.Frame(self, padding=40)
        self.frame.grid(sticky=N+S+E+W)

        self.add_slider_button = ttk.Button(self, text="New Slider")
        self.add_slider_button.grid(column=0, row=0, sticky=N+S+W+E)
        self.add_slider_button['command'] = lambda: self.add_slider()

        self.remove_slider_button = ttk.Button(self, text="Remove Slider")
        self.remove_slider_button.grid(column=1, row=0, sticky=N+S+E+W)
        self.remove_slider_button['command'] = lambda: self.remove_slider()

        if not self.auto_push:
            self.push_button = ttk.Button(self, text="Push")
            self.push_button.grid(column=2, row=0, sticky=N+S+E+W)
            self.push_button['command'] = lambda: self.push()

        self.save_button = ttk.Button(self, text="Save")
        self.save_button.grid(column=3, row=0, sticky=N+S+E+W)
        self.save_button['command'] = lambda: self.save()

        self.sliders = []
        self.data = data
        for saved in self.data:
            print(saved)
            self.add_slider(*saved)


    def load(path):
        data = []
        with open(path, "rb") as f:
            data = pickle.load(f)
            f.close()
        return data
    def save(self):
        self.data = []
        for slider in self.sliders:
            self.data.append(slider.get_data())
        with open("save", "wb") as f:
            pickle.dump(self.data, f)
            f.close()

    def push(self): self.update_sliders()

    def update(self):
        if self.auto_push:
            self.push()

        for y in range(self.height+1): Grid.rowconfigure(self, y, weight=1)
        self.after(50, self.update)

    def add_slider(self, entry=0, slider=0):
        if entry or slider:
            self.sliders.append(
                NetworkSlider(self, entry=entry, slider=slider, y=self.height)
                )
        else:
            self.sliders.append(
                NetworkSlider(self, y=self.height)
                )

        self.height += 1

    def remove_slider(self):
        if len(self.sliders) > 0:
            self.sliders.pop().destroy()
            self.height -= 1

    def update_sliders(self):
        for slider in self.sliders: slider.update()


def main():
    root = App(auto_push=False, data=(App.load(sys.argv[1]) if len(sys.argv) > 1 else []))
    root.mainloop()


if __name__ == "__main__":
    main()
