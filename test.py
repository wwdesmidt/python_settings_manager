from settings_manager import SettingsManager, SettingsManagerFrame
import tkinter as tk
from tkinter import ttk

s = SettingsManager("settings.json")

s.add_setting("debug", "should the application produce extra debugging output?", "False", ("True","False"))
s.add_setting("width", "width? i dont know how to do ranges", "640", ("range","100","1000"))
s.add_setting("height", "description for height", "480", ("range","100","1000"))
s.add_setting("test", "a test setting.\nthis description has a new line in it", "abc", ("abc","123","456","789"))
s.add_setting("test2", "just adding another setting\nto see if adding a new one works after\neverythuing is in place", "abc", ("abc","123","456","789"))

#s.print_test()

root = tk.Tk()

frame = SettingsManagerFrame(root, s)

frame.pack()

root.mainloop()