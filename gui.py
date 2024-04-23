# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:09:56 2021

@author: Mahdi Elghazali
"""
from functools import partial
import tkinter as tk
from tkinter import Toplevel
from PIL import Image,ImageTk
import time as tm
import datetime as dt
from datetime import datetime
#from datetime import timedelta
import pandas as pd
import numpy as np
import os

photos = [] # array to store the list of the resized photos 

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def update_photos():
    main_folder ="C:\\Users\\ICCH_\\My Drive\\Ads transfer"
    if not os.path.exists(main_folder):
        main_folder = os.path.dirname(__file__) + "\\sample ads"

    photo_path = os.listdir(main_folder) # array to store the path of the photos 
    photo_list = [] # array to store the list of the photos 
    photos.clear()

    # assigning the whole path to the photo list
    for file in photo_path:
        if (file.endswith(".png")):
            new_file = os.path.join(main_folder, file)
            photo_list.append(new_file)
        else:
            photo_path.remove(file)

    # reading and loading the photos
    for file in photo_list:
        load = Image.open(file)
        load1 = load.resize((height_value,height_value)) # reszing the ad photo to 1520*1080
        photos.append(ImageTk.PhotoImage(load1))
    
    print()
    print(photo_path)
    print("Photos updated from \"", main_folder, "\" at", tm.strftime('%#m/%#d/%Y %#I:%M:%S %p') + "\n")
    
def quit():# close Admin window if cancel is clicked
    window.destroy()  
    
def display_time(updated):
    current_time = tm.strftime('%B %#d %#I:%M:%S %p') # calculate current time
    today = datetime.now().timetuple().tm_yday # calculate current day of the year
    hour_time = tm.strftime('%H:%M') # calculate current hour

    tomorrow = today + 1 # calculate tomorrow
    today_schedule = data.loc[data["Day_of_year"] == today] # read df and assign the row of today to today_schedule
    tomorrow_schedule = data.loc[data["Day_of_year"] == tomorrow] # read df and assign the row of tomorrow to tomorrow_schedule
    Fajr_Athan = today_schedule.iloc[0]["Fajr_Athan"].strftime('%#I:%M') # assign data with column title Fajr_Athan to Fajr_Athan
    Fajr_Iqama = today_schedule.iloc[0]["Fajr_Iqama"].strftime('%#I:%M')
    Sunrise = today_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%#I:%M')
    Sunrise_Iqama = (datetime.combine(dt.date.today(), today_schedule.iloc[0]["Shurooq_Sunrise"]) + dt.timedelta(minutes=15)).strftime('%#I:%M')
    Thuhr_Athan = today_schedule.iloc[0]["Thuhr_Athan"].strftime('%#I:%M')
    Thuhr_Iqama = today_schedule.iloc[0]["Thuhr_Iqama"].strftime('%#I:%M')
    Asr_Athan = today_schedule.iloc[0]["Asr_Athan"].strftime('%#I:%M')
    Asr_Iqama = today_schedule.iloc[0]["Asr_Iqama"].strftime('%#I:%M')
    Maghrib_Athan = today_schedule.iloc[0]["Maghrib_Athan"].strftime('%#I:%M')
    Maghrib_Iqama = today_schedule.iloc[0]["Maghrib_Iqama"].strftime('%#I:%M')
    Ishaa_Athan = today_schedule.iloc[0]["Ishaa_Athan"].strftime('%#I:%M')
    Ishaa_Iqama = today_schedule.iloc[0]["Ishaa_Iqama"].strftime('%#I:%M')

    fajr_time = today_schedule.iloc[0]["Fajr_Athan"].strftime('%H:%M')
    sunrise_time = today_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%H:%M')
    thuhr_time = today_schedule.iloc[0]["Thuhr_Athan"].strftime('%H:%M')
    asr_time = today_schedule.iloc[0]["Asr_Athan"].strftime('%H:%M')
    maghrib_time = today_schedule.iloc[0]["Maghrib_Athan"].strftime('%H:%M')
    isha_time = today_schedule.iloc[0]["Ishaa_Athan"].strftime('%H:%M')

    Fajr_Athan2 = tomorrow_schedule.iloc[0]["Fajr_Athan"].strftime('%#I:%M')
    Fajr_Iqama2 = tomorrow_schedule.iloc[0]["Fajr_Iqama"].strftime('%#I:%M')
    Sunrise2 = tomorrow_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%#I:%M')
    Sunrise_Iqama2 = (datetime.combine(dt.date.today(), tomorrow_schedule.iloc[0]["Shurooq_Sunrise"]) + dt.timedelta(minutes=15)).strftime('%#I:%M')
    Thuhr_Athan2 = tomorrow_schedule.iloc[0]["Thuhr_Athan"].strftime('%#I:%M')
    Thuhr_Iqama2 = tomorrow_schedule.iloc[0]["Thuhr_Iqama"].strftime('%#I:%M')
    Asr_Athan2 = tomorrow_schedule.iloc[0]["Asr_Athan"].strftime('%#I:%M')
    Asr_Iqama2 = tomorrow_schedule.iloc[0]["Asr_Iqama"].strftime('%#I:%M')
    Maghrib_Athan2 = tomorrow_schedule.iloc[0]["Maghrib_Athan"].strftime('%#I:%M')
    Maghrib_Iqama2 = tomorrow_schedule.iloc[0]["Maghrib_Iqama"].strftime('%#I:%M')
    Ishaa_Athan2 = tomorrow_schedule.iloc[0]["Ishaa_Athan"].strftime('%#I:%M')
    Ishaa_Iqama2 = tomorrow_schedule.iloc[0]["Ishaa_Iqama"].strftime('%#I:%M')

    today_date_label['text'] = today_schedule.iloc[0]["Day"] # to assign today in excel file to today_date_label text
    tomorrow_date_label['text'] = tomorrow_schedule.iloc[0]["Day"] #to assign today+1 in excel file to tomorrow_date_label text
    today_fajr_athan_label ['text'] = Fajr_Athan #to assign Fajir_Athan to today_fajr_athan_label text
    today_fajr_iqama_label ['text'] = Fajr_Iqama
    today_shurooq_athan_label ['text'] = Sunrise
    # today_shurooq_iqama_label ['text'] = Sunrise_Iqama
    today_thuhr_athan_label ['text'] = Thuhr_Athan
    today_thuhr_iqama_label ['text'] = Thuhr_Iqama
    today_asr_athan_label ['text'] = Asr_Athan
    today_asr_iqama_label ['text'] = Asr_Iqama
    today_maghrib_athan_label ['text'] = Maghrib_Athan
    today_maghrib_iqama_label ['text'] = Maghrib_Iqama
    today_isha_athan_label ['text'] = Ishaa_Athan
    today_isha_iqama_label ['text'] = Ishaa_Iqama

    tomorrow_fajr_athan_label ['text'] = Fajr_Athan2
    tomorrow_fajr_iqama_label ['text'] = Fajr_Iqama2
    tomorrow_shurooq_athan_label ['text'] = Sunrise2
    # tomorrow_shurooq_iqama_label ['text'] = Sunrise_Iqama2
    tomorrow_thuhr_athan_label ['text'] = Thuhr_Athan2
    tomorrow_thuhr_iqama_label ['text'] = Thuhr_Iqama2
    tomorrow_asr_athan_label ['text'] = Asr_Athan2
    tomorrow_asr_iqama_label ['text'] = Asr_Iqama2
    tomorrow_maghrib_athan_label ['text'] = Maghrib_Athan2
    tomorrow_maghrib_iqama_label ['text'] = Maghrib_Iqama2
    tomorrow_isha_athan_label ['text'] = Ishaa_Athan2
    tomorrow_isha_iqama_label ['text'] = Ishaa_Iqama2

    next_prayer_color = _from_rgb((255, 0, 0))# to assign color to next prayer
    pre_prayer_color = _from_rgb((0,0,0))# to assign color to next prayer
    current_prayer_color = _from_rgb((0,50,0)) # to assign color to next prayer


    # to highlight the next prayer time

    if (":00" in hour_time):
        if (updated is False):
            update_photos()
            updated = True
    else:
        updated = False

    if(hour_time <= fajr_time):
        today_isha_label['fg'] = pre_prayer_color
        today_isha_athan_label['fg'] = pre_prayer_color
        today_isha_iqama_label['fg'] = pre_prayer_color

        tomorrow_fajr_label['fg'] = pre_prayer_color
        tomorrow_fajr_athan_label['fg'] = pre_prayer_color
        tomorrow_fajr_iqama_label['fg'] = pre_prayer_color

        today_fajr_label['fg'] = next_prayer_color
        today_fajr_athan_label['fg'] = next_prayer_color
        today_fajr_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= fajr_time and hour_time < sunrise_time):
        today_fajr_label['fg'] = current_prayer_color
        today_fajr_athan_label['fg'] = current_prayer_color
        today_fajr_iqama_label['fg'] = current_prayer_color

        today_shurooq_label['fg'] = next_prayer_color
        today_shurooq_athan_label['fg'] = next_prayer_color
        # today_shurooq_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= sunrise_time and hour_time < thuhr_time):
        today_fajr_label['fg'] = pre_prayer_color
        today_fajr_athan_label['fg'] = pre_prayer_color
        today_fajr_iqama_label['fg'] = pre_prayer_color

        today_shurooq_label['fg'] = current_prayer_color
        today_shurooq_athan_label['fg'] = current_prayer_color
        # today_shurooq_iqama_label['fg'] = current_prayer_color

        today_thuhr_label['fg'] = next_prayer_color
        today_thuhr_athan_label['fg'] = next_prayer_color
        today_thuhr_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= thuhr_time and hour_time < asr_time):
        today_shurooq_label['fg'] = pre_prayer_color
        today_shurooq_athan_label['fg'] = pre_prayer_color
        today_shurooq_iqama_label['fg'] = pre_prayer_color
        
        today_thuhr_label['fg'] = current_prayer_color
        today_thuhr_athan_label['fg'] = current_prayer_color
        today_thuhr_iqama_label['fg'] = current_prayer_color

        today_asr_label['fg'] = next_prayer_color
        today_asr_athan_label['fg'] = next_prayer_color
        today_asr_iqama_label['fg'] = next_prayer_color
        
    elif(hour_time >= asr_time and hour_time < maghrib_time):
        today_thuhr_label['fg'] = pre_prayer_color
        today_thuhr_athan_label['fg'] = pre_prayer_color
        today_thuhr_iqama_label['fg'] = pre_prayer_color
        
        today_asr_label['fg'] = current_prayer_color
        today_asr_athan_label['fg'] = current_prayer_color
        today_asr_iqama_label['fg'] = current_prayer_color

        today_maghrib_label['fg'] = next_prayer_color
        today_maghrib_athan_label['fg'] = next_prayer_color
        today_maghrib_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= maghrib_time and hour_time < isha_time):
        today_asr_label['fg'] = pre_prayer_color
        today_asr_athan_label['fg'] = pre_prayer_color
        today_asr_iqama_label['fg'] = pre_prayer_color
        
        today_maghrib_label['fg'] = current_prayer_color
        today_maghrib_athan_label['fg'] = current_prayer_color
        today_maghrib_iqama_label['fg'] = current_prayer_color

        today_isha_label['fg'] = next_prayer_color
        today_isha_athan_label['fg'] = next_prayer_color
        today_isha_iqama_label['fg'] = next_prayer_color
        
    elif(hour_time >= isha_time):
        today_maghrib_label['fg'] = pre_prayer_color
        today_maghrib_athan_label['fg'] = pre_prayer_color
        today_maghrib_iqama_label['fg'] = pre_prayer_color

        today_isha_label['fg'] = current_prayer_color
        today_isha_athan_label['fg'] = current_prayer_color
        today_isha_iqama_label['fg'] = current_prayer_color

        tomorrow_fajr_label['fg'] = next_prayer_color
        tomorrow_fajr_athan_label['fg'] = next_prayer_color
        tomorrow_fajr_iqama_label['fg'] = next_prayer_color

    clock_label ['text'] = current_time # to assign current time to clock label

    # to flash the different announcements every 30 sec
    global counter
    global i    
    
    if (i >= len(photos) - 1):
        i = 0

    if(counter <Time and i< len(photos)):
        flyer_photo_now = photos[i]
        counter += 1
    else:
        flyer_photo_now = photos[i]
        counter = 0
        i+=1
    
    flyer['image'] = flyer_photo_now
    clock_label.after(1000,display_time, updated) # rerun display_time() after 1sec

    return updated


# reading prayer schedule excel file
data = pd.read_excel(os.path.dirname(__file__) + '/prayer_schedule.xlsx',sheet_name=0,header=0) # read prayer time excelsheet

#tk window declaration with name of Prayer Time Portland Oregon
window = tk.Tk(className='Prayer Time Portland Oregon')
# set window size

width_value = window.winfo_screenwidth()
height_value = window.winfo_screenheight()
window.geometry("%dx%d+0+0" %(width_value, height_value))

#set window text_color
window.configure(bg='white')

background = Image.open(os.path.dirname(__file__) + "/Background.png")
background = background.resize((width_value, height_value))
bg = ImageTk.PhotoImage(background)

# declaring the counter for controlling the flyer animation
counter = 0
i =0
j =0
# declaring the time limit for controlling the flyer animation
Time = 10 # 10 seconds per photo

update_photos()

bg_label = tk.Label(text="",bg='white', image = bg)
flyer = tk.Button( command = update_photos , image = photos[0], borderwidth=0) # defining flyer as image and using photo2 for it "flyer photo", also stops the program when hit
window.bind("<Escape>", lambda e: quit())

# defining font variables to be used for display
font_info = 'Helvetica', round(30 * (height_value/1080)), 'bold'
font_info1 = 'Helvetica', round(30 * (height_value/1080)), 'bold'
font_info2 = 'Helvetica', round(30 * (height_value/1080)), 'bold'

text_color = "black" # define text color
# defining the different variables to be shown with background color "bg", text color "fg", and font info "font_info"

times = tk.Frame(window, width=width_value/3.4, height=height_value/1.35, bg='white')

clock_label = tk.Label(times, bg='white', fg=text_color, font = font_info2)

today_date_label = tk.Label(times, bg='white', fg=text_color,font= font_info1)
today_space_label = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)
athan_label = tk.Label(times, bg='white', text="Athan", fg=text_color,font= font_info2)
iqama_label = tk.Label(times, bg='white', text="Iqama", fg=text_color,font= font_info2)
today_fajr_label = tk.Label(times, bg='white', text="Fajr", fg=text_color,font= font_info2)
today_shurooq_label = tk.Label(times, bg='white', text="Shurooq", fg=text_color,font= font_info2)
today_thuhr_label = tk.Label(times, bg='white', text="Thuhr", fg=text_color,font= font_info2)
today_asr_label = tk.Label(times, bg='white', text="Asr", fg=text_color,font= font_info2)
today_maghrib_label = tk.Label(times, bg='white', text="Maghrib", fg=text_color,font= font_info2)
today_isha_label = tk.Label(times, bg='white', text="Ishaa", fg=text_color,font= font_info2)

tomorrow_date_label = tk.Label(times, bg='white', fg=text_color,font= font_info1)
tomorrow_space_label = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)

tomorrow_fajr_label = tk.Label(times, bg='white', text="Fajr", fg=text_color,font= font_info2)
tomorrow_shurooq_label = tk.Label(times, bg='white', text="Shurooq", fg=text_color,font= font_info2)
tomorrow_thuhr_label = tk.Label(times, bg='white', text="Thuhr",fg=text_color,font= font_info2)
tomorrow_asr_label = tk.Label(times, bg='white', text="Asr", fg=text_color,font= font_info2)
tomorrow_maghrib_label = tk.Label(times, bg='white', text="Maghrib", fg=text_color,font= font_info2)
tomorrow_isha_label = tk.Label(times, bg='white', text="Ishaa", fg=text_color,font= font_info2)

# today data
today_fajr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_fajr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_shurooq_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
# today_shurooq_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_shurooq_iqama_label = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)
today_thuhr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_thuhr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_asr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_asr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_maghrib_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_maghrib_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_isha_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_isha_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)

# tomorrow data
tomorrow_fajr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_fajr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_shurooq_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
# tomorrow_shurooq_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_shurooq_iqama_label = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)
tomorrow_thuhr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_thuhr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_asr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_asr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_maghrib_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_maghrib_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_isha_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_isha_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)

bg_label.place(x=0, y=0)
flyer.place(x=width_value-height_value)
times.place(x=120 * (width_value/1920), y=125 * (height_value/1080))

clock_label.grid(row =0, column=0, columnspan =3)
today_date_label.grid(row=1, column=1, columnspan = 2)
today_space_label.grid(row=2, column=0)
athan_label.grid(row=2, column=1)
iqama_label.grid(row=2, column=2)
today_fajr_label.grid(row=3, column=0)
today_shurooq_label.grid(row=4, column=0)
today_thuhr_label.grid(row=5, column=0)
today_asr_label.grid(row=6, column=0)
today_maghrib_label.grid(row=7, column=0)
today_isha_label.grid(row=8, column=0)

tomorrow_date_label.grid(row=11, column=1, columnspan = 2)
tomorrow_fajr_label.grid(row=12, column=0)
tomorrow_shurooq_label.grid(row=13, column=0)
tomorrow_thuhr_label.grid(row=14, column=0)
tomorrow_asr_label.grid(row=15, column=0)
tomorrow_maghrib_label.grid(row=16, column=0)
tomorrow_isha_label.grid(row=17, column=0)

today_fajr_athan_label.grid(row=3, column=1)
today_fajr_iqama_label.grid(row=3, column=2)
today_shurooq_athan_label.grid(row=4, column=1)
today_shurooq_iqama_label.grid(row=4, column=2)
today_thuhr_athan_label.grid(row=5, column=1)
today_thuhr_iqama_label.grid(row=5, column=2)
today_asr_athan_label.grid(row=6, column=1)
today_asr_iqama_label.grid(row=6, column=2)
today_maghrib_athan_label.grid(row=7, column=1)
today_maghrib_iqama_label.grid(row=7, column=2)
today_isha_athan_label.grid(row=8, column=1)
today_isha_iqama_label.grid(row=8, column=2)

tomorrow_fajr_athan_label.grid(row=12, column=1)
tomorrow_fajr_iqama_label.grid(row=12, column=2)
tomorrow_shurooq_athan_label.grid(row=13, column=1)
tomorrow_shurooq_iqama_label.grid(row=13, column=2)
tomorrow_thuhr_athan_label.grid(row=14, column=1)
tomorrow_thuhr_iqama_label.grid(row=14, column=2)
tomorrow_asr_athan_label.grid(row=15, column=1)
tomorrow_asr_iqama_label.grid(row=15, column=2)
tomorrow_maghrib_athan_label.grid(row=16, column=1)
tomorrow_maghrib_iqama_label.grid(row=16, column=2)
tomorrow_isha_athan_label.grid(row=17, column=1)
tomorrow_isha_iqama_label.grid(row=17, column=2)


display_time(False) # to call display_time() function
window.resizable(False, True) # to make the window resizable
window.bind()

window.wm_attributes('-fullscreen', 1)
window.bind()
window.mainloop()