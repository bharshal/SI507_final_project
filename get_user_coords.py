# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 15:03:13 2022

@author: hbora


@Title : SI507 Final Project - get user cho-ords

@Description: This file creates a GUI for getting user location as latitude and 
longitude co-ordinates
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import tkinter.simpledialog
from tkinter import font as tkFont

def get_coords():
    """
    Summary
    -------
    Shows map of AA, gets image co-ordinate of click, converts to lat-long
    
    Description
    -------
    This function creates a TKinter canvas, reads a image which is a screenshot
    of map of AnnArbor cropped exactly to match co-ordinates used to create 
    cache and displays the image. It asks user to click on image to select 
    location, captures the image co-ordinate of the click and converts to 
    actual lat long co-ordinates using math magic
    
    Returns
    -------
    (lat,long) : tuple which denotes latitude and longitude of user chosen 
                location
    """

    global lat, long
    #default values in case something breaks
    lat, long = 42.269025700396604, -83.72926195271462 
    

    root = Tk()
    
    #setting up a tkinter canvas
    w = Canvas(root, width=1000, height=800)
    w.pack()
    
    helv20 = tkFont.Font(family='Helvetica', size=20, weight='bold')

    original = Image.open("aa.jpg")
    width,height = original.size
    img = ImageTk.PhotoImage(original)
    w.create_image(0, 50, image=img, anchor = "nw")

    # Determine the origin by clicking
    def get_click_cord(eventorigin):
        tkinter.messagebox.showinfo(title= "Info", message = "Got location!\n \
                                You can click Done or close this and click \
                                     on map again for new location")
        x0 = eventorigin.x
        y0 = eventorigin.y
        
        # four co-ords for annarbor border: topleft, topright, bottomleft, bottomright
        tl = (42.31672728454659, -83.80731873113874)
        tr = (42.31672728454659, -83.67290787670282)
        bl = (42.23823420163313, -83.80731873113874)
        br = (42.23823420163313, -83.67290787670282)
        
        # horizontal and vertical separation of the borders
        horz_dist = tr[1] - tl[1]
        vert_dist = tr[0] - br[0]
        
        global lat, long
        
        x_ratio = (horz_dist/width)
        long = x_ratio*x0 + tl[1]
        
        y_ratio = (vert_dist/height)
        lat = tl[0] -y_ratio*y0 
     
    w.bind("<Button 1>",get_click_cord)
    
    def save():
        # closes window
        root.destroy()
        
    b = Button(root, text="Done", command=save, anchor='c')
    b["font"] = helv20
    quit_button_window = w.create_window(800, 500, window=b)
    
    w.create_text(300, 25, text="Click on location to search, then press Done", font=helv20)

    root.mainloop()
    
    return lat,long