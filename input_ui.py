# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 18:03:48 2022

@author: hbora

@Title : SI507 Final Project - User input

@Description: This file creates a GUI for getting user preferences between 
dist, price, rating
"""

#Import the required Libraries
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont


    
def get_user_input():
    """
    Summary
    -------
    Asks user to drop between drop down options of dist, price and rating
    
    Description
    -------
    This function creates a TKinter window, and shows the user drop down menus
    to choose between choices of dist, price and rating ranges. There is a save
    button below the menus. Once user clicks save, the window closes and chosen
    options are returned as tuple between (0,0,0)-(3,3,3). (3 buckets for each
                                                            query)
    
    Returns
    -------
    (dist,price,rating) : tuple which denotes option chosen between respective 
                        buckets
    """
    
    win = Tk()
    #Set the geometry of the Tkinter frame
    win.geometry("700x700")
    helv30 = tkFont.Font(family='Helvetica', size=30, weight='bold')
    helv20 = tkFont.Font(family='Helvetica', size=10, weight='bold')
    
    
    option_dist = ["0 to 2km","2 to 4km","4km and above"]
    option_price = ["$","$$","$$$"]
    option_rating = ["1 to 3","3 to 4","4 and above"]
    
    #Create Multiple Buttons with different commands

    lab_dist = Label(win, text="Select distance", font=helv30) #label
    lab_dist.grid(row=1,column=1)
    variable_dist = StringVar(win)
    menu1 = OptionMenu(win, variable_dist,option_dist[0], *option_dist[1:])
    variable_dist.set(option_dist[0])
    opt = win.nametowidget(menu1.menuname)  # Get menu widget.
    opt["font"] = helv20  # Set the dropdown menu's font
    menu1["font"] = helv30
    menu1.grid(row=1,column=2)
    
    lab_price = Label(win, text="Select price range", font=helv30)
    lab_price.grid(row=2,column=1)
    variable_price = StringVar(win)
    menu2 = OptionMenu(win, variable_price,option_price[0], *option_price[1:])
    variable_price.set(option_price[0])
    opt = win.nametowidget(menu2.menuname)  # Get menu widget.
    opt["font"] = helv20  # Set the dropdown menu's font
    menu2.grid(row=2,column=2)
    menu2["font"] = helv30
    
    lab_rate = Label(win, text="Select rating", font=helv30)
    lab_rate.grid(row=3,column=1)
    variable_rating = StringVar(win)
    menu3 = OptionMenu(win, variable_rating,option_rating[0], *option_rating[1:])
    variable_rating.set(option_rating[0])
    opt = win.nametowidget(menu3.menuname)  # Get menu widget.
    opt["font"] = helv20  # Set the dropdown menu's font
    menu3.grid(row=3,column=2)
    menu3["font"] = helv30
    
    global dist,price,rating

    def save():
        
        global dist,price,rating
        dist = option_dist.index(variable_dist.get())
        price = option_price.index(variable_price.get())
        rating = option_rating.index(variable_rating.get())
        win.destroy()

    b = Button(win, text="Save", command=save)
    b["font"] = helv30
    b.grid(row = 5, column = 2)
    
    win.mainloop()
    return dist, price, rating