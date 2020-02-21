'''
a class that uses a dictionary and a json file to manage settings

usage:
1. in the main app have something to "intialize" your settings, using the add_setting() method
   this will add the setting to the file if it isn't already there, if it is already there it will
   just do nothing, so it is safe for it to run every time, and it is a way to create the settings
   file with default values if it doesn't exist
2. use the set_setting() and get_setting() methods to interact with the class. this way changed 
   settings will be returned as well as written back to the file, and the proper exceptions can be
   raised if a setting doesnt exist and you try to read it


todo: change everything we dont want to user to read to private

'''

import os
import json

class SettingsManager:
    def __init__(self, file_name):
        #initialize the file
        self.file_name = file_name
        self.init_file()

        #set of settings
        self.settings = dict()

        #load data from file
        self.load_file()

    #add a new setting to the file and save the file
    #if the setting is already there dont overwrite it
    #that way initialization can be done in the main app
    #without values always returning to their default
    def add_setting(self, name, description, value, possible_values):
        if name not in self.settings:
            self.settings[name] = {"name":name, "description":description, "value":value, "possible_values":possible_values}
            self.write_file()

    #write the current data to the file
    def write_file(self):
        f = open(self.file_name, "w")
        json.dump(self.settings, f)
        f.close()

    #just print everything for testing
    def print_test(self):
        print(self.settings)

    #if the file doesnt exist, create it
    def init_file(self):
        if not os.path.isfile(self.file_name):
            f = open(self.file_name, "w+")
            empty_json = json.loads("{}")
            json.dump(empty_json,f)
            f.close

    #load json data from file and create settings objects
    def load_file(self):
        f = open(self.file_name, "r")
        self.settings = json.load(f)
        f.close
        #self.settings = json_data

    def get_value(self, setting):
        return self.settings[setting]["value"]

    def get_description(self, setting):
        return self.settings[setting]["description"]

    def get_possible_values(self, setting):
        return self.settings[setting]["possible_values"]

    def get_settings(self):
        settings_list = set()
        for setting in self.settings:
            settings_list.add(self.settings[setting]["name"])
        return settings_list

    #if the setting exists, update its value
    #and then write everything back to the file
    def set_setting(self, setting, value):
        #this is where we could check if the setting was in the possible values
        if setting in self.settings:
            self.settings[setting]["value"]=value
        else:
            raise KeyError(setting)
        
        self.write_file()


#basic tkinter frame for managing settings
import tkinter as tk
from tkinter import ttk


class SettingsManagerFrame(ttk.Frame):
    def __init__(self, container, settings_manager):
        super().__init__(container)

        self.container = container

        self.settings_manager = settings_manager

        self.settings_list = settings_manager.get_settings()

        #a dictionary to keep track of the settings
        self.setting_values=dict()

        #a counter for positioning etc.
        i=0

        for setting in self.settings_list:
            #print(setting)

            #a label with the name of the setting
            ttk.Label(self, text=setting).grid(row=i, column=0, pady=5, padx=5, sticky="W")

            #initialize a stringvar dict entry
            self.setting_values[setting]=tk.StringVar()

            #input for the setting
            #later id like to be able to make this more advanced 
            # (checkbox for bool, slider for range, dropdown with possible choices etc)
            ttk.Entry(self, textvariable=self.setting_values[setting]).grid(row=i, column=1, pady=5, padx=5, sticky="W")

            #prefil input with current setting
            self.setting_values[setting].set(self.settings_manager.get_value(setting))

            #a label for the description
            ttk.Label(self, text=f"Description: {self.settings_manager.get_description(setting)}").grid(row=i, column=2, pady=5, padx=5, sticky="W")

            #a label for the possible values list
            #possible_settings = self.settings_manager.get_possible_values(setting)

            ttk.Label(self, text=f"Possible Settings:{self.settings_manager.get_possible_values(setting)}").grid(row=i, column=3, pady=5, padx=5, sticky="W")

            #increment the counter
            i=i+1

        #container so the buttons can have different columns than the rest of the fields
        button_container = ttk.Frame(self)
        button_container.grid(row=i, column=0, columnspan=4, sticky="NSWE")

        #cancel button
        cancel_button = tk.Button(button_container, text="Cancel", command=self.cancel, width=15)
        cancel_button.grid(row=0, column=0, pady=5, padx=(5,2.5), sticky="NSE")
        
        #ok button
        ok_button = tk.Button(button_container, text="OK", command=self.ok, width=15)
        ok_button.grid(row=0, column=1, pady=5, padx=(2.5,5), sticky="NSW")

        #force the 2  button columns to equally span the 4 uneven main columns
        button_container.grid_columnconfigure(0, weight=1, uniform="buttons")
        button_container.grid_columnconfigure(1, weight=1, uniform="buttons")

    #just close the window
    def cancel(self):
        self.container.destroy()

    #update each setting, and then close the window
    def ok(self):
        for setting in self.setting_values:
            self.settings_manager.set_setting(setting, self.setting_values[setting].get())
        self.container.destroy()