# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:09:56 2021

@author: Mahdi Elghazali and Omar Nassar
"""

import tkinter as tk
from PIL import Image,ImageTk
import time as tm
from datetime import datetime
import pandas as pd
import numpy as np
import os
import argparse
from trivia import get_winners


photos = [] # array to store the list of the resized photos 

# declaring the counter for controlling the flyer animation
counter = 0
i =0
j =0
# declaring the time limit for controlling the flyer animation
Time = 10 # 10 seconds per photo

class Labels:
    def __init__(self, times, bg_color, text_color, font_info, font_info1, font_info2):
            self.clock_label = tk.Label(times,bg=bg_color, fg=text_color, font = font_info2)

            self.today_date_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info1)
            self.today_space_label = tk.Label(times,bg=bg_color, text="", fg=text_color,font= font_info)
            self.athan_label = tk.Label(times,bg=bg_color, text="Athan", fg=text_color,font= font_info2)
            self.iqama_label = tk.Label(times,bg=bg_color, text="Iqama", fg=text_color,font= font_info2)
            self.today_fajr_label = tk.Label(times,bg=bg_color, text="Fajr", fg=text_color,font= font_info2)
            self.today_shurooq_label = tk.Label(times,bg=bg_color, text="Shurooq", fg=text_color,font= font_info2)
            self.today_thuhr_label = tk.Label(times,bg=bg_color, text="Thuhr", fg=text_color,font= font_info2)
            self.today_asr_label = tk.Label(times,bg=bg_color, text="Asr", fg=text_color,font= font_info2)
            self.today_maghrib_label = tk.Label(times,bg=bg_color, text="Maghrib", fg=text_color,font= font_info2)
            self.today_isha_label = tk.Label(times,bg=bg_color, text="Ishaa", fg=text_color,font= font_info2)

            self.tomorrow_date_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info1)
            self.tomorrow_space_label = tk.Label(times,bg=bg_color, text="", fg=text_color,font= font_info)

            self.tomorrow_fajr_label = tk.Label(times,bg=bg_color, text="Fajr", fg=text_color,font= font_info2)
            self.tomorrow_shurooq_label = tk.Label(times,bg=bg_color, text="Shurooq", fg=text_color,font= font_info2)
            self.tomorrow_thuhr_label = tk.Label(times,bg=bg_color, text="Thuhr",fg=text_color,font= font_info2)
            self.tomorrow_asr_label = tk.Label(times,bg=bg_color, text="Asr", fg=text_color,font= font_info2)
            self.tomorrow_maghrib_label = tk.Label(times,bg=bg_color, text="Maghrib", fg=text_color,font= font_info2)
            self.tomorrow_isha_label = tk.Label(times,bg=bg_color, text="Ishaa", fg=text_color,font= font_info2)

            # today data
            self.today_fajr_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_fajr_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_shurooq_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            # today_shurooq_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_shurooq_iqama_label = tk.Label(times,bg=bg_color, text="", fg=text_color,font= font_info)
            self.today_thuhr_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_thuhr_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_asr_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_asr_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_maghrib_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_maghrib_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_isha_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_isha_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)

            # tomorrow data
            self.tomorrow_fajr_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_fajr_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_shurooq_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            # tomorrow_shurooq_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_shurooq_iqama_label = tk.Label(times,bg=bg_color, text="", fg=text_color,font= font_info)
            self.tomorrow_thuhr_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_thuhr_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_asr_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_asr_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_maghrib_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_maghrib_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_isha_athan_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_isha_iqama_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def update_photos(height_value):
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
        load1 = load.resize((height_value,height_value)) # reszing the ad photo
        photos.append(ImageTk.PhotoImage(load1))
    
    print()
    print(photo_path)
    print("Photos updated from \"", main_folder, "\" at", tm.strftime('%#m/%#d/%Y %#I:%M:%S %p') + "\n")
    
def quit(window):# close Admin window if cancel is clicked
    window.destroy()  
    
def display_time(labels, data, flyer, updated, ramadan, height_value):
    current_time = tm.strftime('%B %#d %#I:%M:%S %p') # calculate current time
    today = datetime.now().timetuple().tm_yday # calculate current day of the year
    hour_time = tm.strftime('%H:%M') # calculate current hour

    tomorrow = today + 1 # calculate tomorrow
    today_schedule = data.loc[data["Day_of_year"] == today] # read df and assign the row of today to today_schedule
    tomorrow_schedule = data.loc[data["Day_of_year"] == tomorrow] # read df and assign the row of tomorrow to tomorrow_schedule
    Fajr_Athan = today_schedule.iloc[0]["Fajr_Athan"].strftime('%#I:%M') # assign data with column title Fajr_Athan to Fajr_Athan
    Fajr_Iqama = today_schedule.iloc[0]["Fajr_Iqama"].strftime('%#I:%M')
    Sunrise = today_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%#I:%M')
    # Sunrise_Iqama = (datetime.combine(dt.date.today(), today_schedule.iloc[0]["Shurooq_Sunrise"]) + dt.timedelta(minutes=15)).strftime('%#I:%M')
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
    # Sunrise_Iqama2 = (datetime.combine(dt.date.today(), tomorrow_schedule.iloc[0]["Shurooq_Sunrise"]) + dt.timedelta(minutes=15)).strftime('%#I:%M')
    Thuhr_Athan2 = tomorrow_schedule.iloc[0]["Thuhr_Athan"].strftime('%#I:%M')
    Thuhr_Iqama2 = tomorrow_schedule.iloc[0]["Thuhr_Iqama"].strftime('%#I:%M')
    Asr_Athan2 = tomorrow_schedule.iloc[0]["Asr_Athan"].strftime('%#I:%M')
    Asr_Iqama2 = tomorrow_schedule.iloc[0]["Asr_Iqama"].strftime('%#I:%M')
    Maghrib_Athan2 = tomorrow_schedule.iloc[0]["Maghrib_Athan"].strftime('%#I:%M')
    Maghrib_Iqama2 = tomorrow_schedule.iloc[0]["Maghrib_Iqama"].strftime('%#I:%M')
    Ishaa_Athan2 = tomorrow_schedule.iloc[0]["Ishaa_Athan"].strftime('%#I:%M')
    Ishaa_Iqama2 = tomorrow_schedule.iloc[0]["Ishaa_Iqama"].strftime('%#I:%M')

    labels.today_date_label['text'] = today_schedule.iloc[0]["Day"] # to assign today in excel file to today_date_label text
    labels.tomorrow_date_label['text'] = tomorrow_schedule.iloc[0]["Day"] #to assign today+1 in excel file to tomorrow_date_label text
    labels.today_fajr_athan_label ['text'] = Fajr_Athan #to assign Fajir_Athan to today_fajr_athan_label text
    labels.today_fajr_iqama_label ['text'] = Fajr_Iqama
    labels.today_shurooq_athan_label ['text'] = Sunrise
    # today_shurooq_iqama_label ['text'] = Sunrise_Iqama
    labels.today_thuhr_athan_label ['text'] = Thuhr_Athan
    labels.today_thuhr_iqama_label ['text'] = Thuhr_Iqama
    labels.today_asr_athan_label ['text'] = Asr_Athan
    labels.today_asr_iqama_label ['text'] = Asr_Iqama
    labels.today_maghrib_athan_label ['text'] = Maghrib_Athan
    labels.today_maghrib_iqama_label ['text'] = Maghrib_Iqama
    labels.today_isha_athan_label ['text'] = Ishaa_Athan
    labels.today_isha_iqama_label ['text'] = Ishaa_Iqama

    labels.tomorrow_fajr_athan_label ['text'] = Fajr_Athan2
    labels.tomorrow_fajr_iqama_label ['text'] = Fajr_Iqama2
    labels.tomorrow_shurooq_athan_label ['text'] = Sunrise2
    # tomorrow_shurooq_iqama_label ['text'] = Sunrise_Iqama2
    labels.tomorrow_thuhr_athan_label ['text'] = Thuhr_Athan2
    labels.tomorrow_thuhr_iqama_label ['text'] = Thuhr_Iqama2
    labels.tomorrow_asr_athan_label ['text'] = Asr_Athan2
    labels.tomorrow_asr_iqama_label ['text'] = Asr_Iqama2
    labels.tomorrow_maghrib_athan_label ['text'] = Maghrib_Athan2
    labels.tomorrow_maghrib_iqama_label ['text'] = Maghrib_Iqama2
    labels.tomorrow_isha_athan_label ['text'] = Ishaa_Athan2
    labels.tomorrow_isha_iqama_label ['text'] = Ishaa_Iqama2

    next_prayer_color = _from_rgb((255, 0, 0))# to assign color to next prayer
    pre_prayer_color = _from_rgb((255,255,255)) if ramadan else _from_rgb((0,0,0))# to assign color to next prayer
    current_prayer_color = _from_rgb((0,200,0)) if ramadan else _from_rgb((0,50,0)) # to assign color to next prayer


    # to highlight the next prayer time

    if (":00" in hour_time):
        if (updated is False):
            update_photos(height_value)
            updated = True
    else:
        updated = False

    if(hour_time <= fajr_time):
        labels.today_isha_label['fg'] = pre_prayer_color
        labels.today_isha_athan_label['fg'] = pre_prayer_color
        labels.today_isha_iqama_label['fg'] = pre_prayer_color

        labels.tomorrow_fajr_label['fg'] = pre_prayer_color
        labels.tomorrow_fajr_athan_label['fg'] = pre_prayer_color
        labels.tomorrow_fajr_iqama_label['fg'] = pre_prayer_color

        labels.today_fajr_label['fg'] = next_prayer_color
        labels.today_fajr_athan_label['fg'] = next_prayer_color
        labels.today_fajr_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= fajr_time and hour_time < sunrise_time):
        labels.today_fajr_label['fg'] = current_prayer_color
        labels.today_fajr_athan_label['fg'] = current_prayer_color
        labels.today_fajr_iqama_label['fg'] = current_prayer_color

        labels.today_shurooq_label['fg'] = next_prayer_color
        labels.today_shurooq_athan_label['fg'] = next_prayer_color
        # today_shurooq_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= sunrise_time and hour_time < thuhr_time):
        labels.today_fajr_label['fg'] = pre_prayer_color
        labels.today_fajr_athan_label['fg'] = pre_prayer_color
        labels.today_fajr_iqama_label['fg'] = pre_prayer_color

        labels.today_shurooq_label['fg'] = current_prayer_color
        labels.today_shurooq_athan_label['fg'] = current_prayer_color
        # today_shurooq_iqama_label['fg'] = current_prayer_color

        labels.today_thuhr_label['fg'] = next_prayer_color
        labels.today_thuhr_athan_label['fg'] = next_prayer_color
        labels.today_thuhr_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= thuhr_time and hour_time < asr_time):
        labels.today_shurooq_label['fg'] = pre_prayer_color
        labels.today_shurooq_athan_label['fg'] = pre_prayer_color
        labels.today_shurooq_iqama_label['fg'] = pre_prayer_color
        
        labels.today_thuhr_label['fg'] = current_prayer_color
        labels.today_thuhr_athan_label['fg'] = current_prayer_color
        labels.today_thuhr_iqama_label['fg'] = current_prayer_color

        labels.today_asr_label['fg'] = next_prayer_color
        labels.today_asr_athan_label['fg'] = next_prayer_color
        labels.today_asr_iqama_label['fg'] = next_prayer_color
        
    elif(hour_time >= asr_time and hour_time < maghrib_time):
        labels.today_thuhr_label['fg'] = pre_prayer_color
        labels.today_thuhr_athan_label['fg'] = pre_prayer_color
        labels.today_thuhr_iqama_label['fg'] = pre_prayer_color
        
        labels.today_asr_label['fg'] = current_prayer_color
        labels.today_asr_athan_label['fg'] = current_prayer_color
        labels.today_asr_iqama_label['fg'] = current_prayer_color

        labels.today_maghrib_label['fg'] = next_prayer_color
        labels.today_maghrib_athan_label['fg'] = next_prayer_color
        labels.today_maghrib_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= maghrib_time and hour_time < isha_time):
        labels.today_asr_label['fg'] = pre_prayer_color
        labels.today_asr_athan_label['fg'] = pre_prayer_color
        labels.today_asr_iqama_label['fg'] = pre_prayer_color
        
        labels.today_maghrib_label['fg'] = current_prayer_color
        labels.today_maghrib_athan_label['fg'] = current_prayer_color
        labels.today_maghrib_iqama_label['fg'] = current_prayer_color

        labels.today_isha_label['fg'] = next_prayer_color
        labels.today_isha_athan_label['fg'] = next_prayer_color
        labels.today_isha_iqama_label['fg'] = next_prayer_color
        
    elif(hour_time >= isha_time):
        labels.today_maghrib_label['fg'] = pre_prayer_color
        labels.today_maghrib_athan_label['fg'] = pre_prayer_color
        labels.today_maghrib_iqama_label['fg'] = pre_prayer_color

        labels.today_isha_label['fg'] = current_prayer_color
        labels.today_isha_athan_label['fg'] = current_prayer_color
        labels.today_isha_iqama_label['fg'] = current_prayer_color

        labels.tomorrow_fajr_label['fg'] = next_prayer_color
        labels.tomorrow_fajr_athan_label['fg'] = next_prayer_color
        labels.tomorrow_fajr_iqama_label['fg'] = next_prayer_color

    labels.clock_label ['text'] = current_time # to assign current time to clock label

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
    labels.clock_label.after(1000,display_time, labels, data, flyer, updated, ramadan, height_value) # rerun display_time() after 1sec

    return updated

def main():
    parser = argparse.ArgumentParser(description="ICCH Prayer Time and Flyers Display")
    parser.add_argument("-r", action="store_true", help="enables ramadan mode")
    args = parser.parse_args()

    # reading prayer schedule excel file
    print(os.path.dirname(__file__) + '/prayer_schedule.xlsx')
    data = pd.read_excel(os.path.dirname(__file__) + '/prayer_schedule.xlsx',sheet_name=0,header=0) # read prayer time excelsheet

    #tk window declaration with name of Prayer Time Portland Oregon
    window = tk.Tk(className='Prayer Time Portland Oregon')
    # set window size

    width_value = window.winfo_screenwidth()
    height_value = window.winfo_screenheight()
    window.geometry("%dx%d+0+0" %(width_value, height_value))

    #set window text_color
    window.configure(bg='white')

    background_path = "/Ramadan.png" if args.r else "/Background.png"

    background = Image.open(os.path.dirname(__file__) + background_path)
    background = background.resize((width_value, height_value))
    bg = ImageTk.PhotoImage(background)

    update_photos(height_value if not args.r else int(height_value/2))

    bg_label = tk.Label(text="",bg='white', image = bg)
    flyer = tk.Button( command = lambda: update_photos(height_value if not args.r else int(height_value/2)) , image = photos[0], borderwidth=0) # defining flyer as image and using photo2 for it "flyer photo", also stops the program when hit
    window.bind("<Escape>", lambda e: quit(window))

    # defining font variables to be used for display
    font_info = 'Helvetica', round(30 * (height_value/1080)), 'bold'
    font_info1 = 'Helvetica', round(30 * (height_value/1080)), 'bold'
    font_info2 = 'Helvetica', round(30 * (height_value/1080)), 'bold'

    text_color = "white" if args.r else "black" # define text color
    bg_color = _from_rgb((0, 25, 125)) if args.r else "white"
    # defining the different variables to be shown with background color "bg", text color "fg", and font info "font_info"

    times = tk.Frame(window, width=width_value/3.4, height=height_value/1.35,bg=bg_color)

    labels = Labels(times, bg_color, text_color, font_info, font_info1, font_info2)

    bg_label.place(x=0, y=0)
    flyer.place(x=width_value-height_value if not args.r else width_value-height_value + int(height_value/2))
    times.place(x=120 * (width_value/1920), y=125 * (height_value/1080))

    labels.clock_label.grid(row =0, column=0, columnspan =3)
    labels.today_date_label.grid(row=1, column=1, columnspan = 2)
    labels.today_space_label.grid(row=2, column=0)
    labels.athan_label.grid(row=2, column=1)
    labels.iqama_label.grid(row=2, column=2)
    labels.today_fajr_label.grid(row=3, column=0)
    labels.today_shurooq_label.grid(row=4, column=0)
    labels.today_thuhr_label.grid(row=5, column=0)
    labels.today_asr_label.grid(row=6, column=0)
    labels.today_maghrib_label.grid(row=7, column=0)
    labels.today_isha_label.grid(row=8, column=0)

    labels.tomorrow_date_label.grid(row=11, column=1, columnspan = 2)
    labels.tomorrow_fajr_label.grid(row=12, column=0)
    labels.tomorrow_shurooq_label.grid(row=13, column=0)
    labels.tomorrow_thuhr_label.grid(row=14, column=0)
    labels.tomorrow_asr_label.grid(row=15, column=0)
    labels.tomorrow_maghrib_label.grid(row=16, column=0)
    labels.tomorrow_isha_label.grid(row=17, column=0)

    labels.today_fajr_athan_label.grid(row=3, column=1)
    labels.today_fajr_iqama_label.grid(row=3, column=2)
    labels.today_shurooq_athan_label.grid(row=4, column=1, columnspan=2)
    # today_shurooq_iqama_label.grid(row=4, column=2)
    labels.today_thuhr_athan_label.grid(row=5, column=1)
    labels.today_thuhr_iqama_label.grid(row=5, column=2)
    labels.today_asr_athan_label.grid(row=6, column=1)
    labels.today_asr_iqama_label.grid(row=6, column=2)
    labels.today_maghrib_athan_label.grid(row=7, column=1)
    labels.today_maghrib_iqama_label.grid(row=7, column=2)
    labels.today_isha_athan_label.grid(row=8, column=1)
    labels.today_isha_iqama_label.grid(row=8, column=2)

    labels.tomorrow_fajr_athan_label.grid(row=12, column=1)
    labels.tomorrow_fajr_iqama_label.grid(row=12, column=2)
    labels.tomorrow_shurooq_athan_label.grid(row=13, column=1, columnspan=2)
    # tomorrow_shurooq_iqama_label.grid(row=13, column=2)
    labels.tomorrow_thuhr_athan_label.grid(row=14, column=1)
    labels.tomorrow_thuhr_iqama_label.grid(row=14, column=2)
    labels.tomorrow_asr_athan_label.grid(row=15, column=1)
    labels.tomorrow_asr_iqama_label.grid(row=15, column=2)
    labels.tomorrow_maghrib_athan_label.grid(row=16, column=1)
    labels.tomorrow_maghrib_iqama_label.grid(row=16, column=2)
    labels.tomorrow_isha_athan_label.grid(row=17, column=1)
    labels.tomorrow_isha_iqama_label.grid(row=17, column=2)

    display_time(labels, data, flyer, False, args.r, height_value if not args.r else int(height_value/2)) # to call display_time() function
    window.resizable(False, True) # to make the window resizable
    window.bind()

    window.wm_attributes('-fullscreen', 1)
    window.bind()
    window.mainloop()

if __name__ == '__main__':
    main()