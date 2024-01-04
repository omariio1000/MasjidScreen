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
from datetime import datetime, timedelta
#from datetime import timedelta
import pandas as pd
import numpy as np
import os

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


    
def quit():# close Admin window if cancel is clicked
    window.destroy()
    
    
    
    
    
def display_time():
    current_time =tm.strftime('%B %#d %Y %#I:%M:%S %p') # calculate current time
    today = datetime.now().timetuple().tm_yday # calculate current day of the year
    hour_time = tm.strftime('%H:%M') # calculate current hour

    tomorrow = today + 1 # calculate tomorrow
    today_schedule = data.loc[data["Day_of_year"] == today] # read df and assign the row of today to today_schedule
    tomorrow_schedule = data.loc[data["Day_of_year"] == tomorrow] # read df and assign the row of tomorrow to tomorrow_schedule
    Fajr_Athan = today_schedule.iloc[0]["Fajr_Athan"].strftime('%#I:%M') # assign data with column title Fajr_Athan to Fajr_Athan
    Fajr_Iqama = today_schedule.iloc[0]["Fajr_Iqama"].strftime('%#I:%M')
    Sunrise = today_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%#I:%M')
    Thuhr_Athan = today_schedule.iloc[0]["Thuhr_Athan"].strftime('%#I:%M')
    Thuhr_Iqama = today_schedule.iloc[0]["Thuhr_Iqama"].strftime('%#I:%M')
    Asr_Athan = today_schedule.iloc[0]["Asr_Athan"].strftime('%#I:%M')
    Asr_Iqama = today_schedule.iloc[0]["Asr_Iqama"].strftime('%#I:%M')
    Maghrib_Athan = today_schedule.iloc[0]["Maghrib_Athan"].strftime('%#I:%M')
    Maghrib_Iqama = today_schedule.iloc[0]["Maghrib_Iqama"].strftime('%#I:%M')
    Ishaa_Athan = today_schedule.iloc[0]["Ishaa_Athan"].strftime('%#I:%M')
    Ishaa_Iqama = today_schedule.iloc[0]["Ishaa_Iqama"].strftime('%#I:%M')

    fajr_time = today_schedule.iloc[0]["Fajr_Athan"].strftime('%H:%M')
    thuhr_time = today_schedule.iloc[0]["Thuhr_Athan"].strftime('%H:%M')
    asr_time = today_schedule.iloc[0]["Asr_Athan"].strftime('%H:%M')
    maghrib_time = today_schedule.iloc[0]["Maghrib_Athan"].strftime('%H:%M')
    isha_time = today_schedule.iloc[0]["Ishaa_Athan"].strftime('%H:%M')

    Fajr_Athan2 = tomorrow_schedule.iloc[0]["Fajr_Athan"].strftime('%#I:%M')
    Fajr_Iqama2 = tomorrow_schedule.iloc[0]["Fajr_Iqama"].strftime('%#I:%M')
    Sunrise2 = tomorrow_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%#I:%M')
    Thuhr_Athan2 = tomorrow_schedule.iloc[0]["Thuhr_Athan"].strftime('%#I:%M')
    Thuhr_Iqama2 = tomorrow_schedule.iloc[0]["Thuhr_Iqama"].strftime('%#I:%M')
    Asr_Athan2 = tomorrow_schedule.iloc[0]["Asr_Athan"].strftime('%#I:%M')
    Asr_Iqama2 = tomorrow_schedule.iloc[0]["Asr_Iqama"].strftime('%#I:%M')
    Maghrib_Athan2 = tomorrow_schedule.iloc[0]["Maghrib_Athan"].strftime('%#I:%M')
    Maghrib_Iqama2 = tomorrow_schedule.iloc[0]["Maghrib_Iqama"].strftime('%#I:%M')
    Ishaa_Athan2 = tomorrow_schedule.iloc[0]["Ishaa_Athan"].strftime('%#I:%M')
    Ishaa_Iqama2 = tomorrow_schedule.iloc[0]["Ishaa_Iqama"].strftime('%#I:%M')


    today_label['text'] = today_schedule.iloc[0]["Day"] # to assign today in excel file to today_label text
    tomorrow_label['text'] = tomorrow_schedule.iloc[0]["Day"] #to assign today+1 in excel file to tomorrow_label text
    today_fajr_athan_label ['text'] = Fajr_Athan #to assign Fajir_Athan to today_fajr_athan_label text
    today_fajr_iqama_label ['text'] = Fajr_Iqama
    today_sunrise_label ['text'] = Sunrise
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
    tomorrow_sunrise_label ['text'] = Sunrise2
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
    current_prayer_color = _from_rgb((0,180,0)) # to assign color to next prayer
    #hour_time = Ishaa_Iqama
    #print(hour_time)

    # to highlight the next prayer time
    if(hour_time<= fajr_time):
        today_isha_label['fg']= pre_prayer_color
        today_isha_athan_label['fg'] = pre_prayer_color
        today_isha_iqama_label['fg'] = pre_prayer_color

        tomorrow_fajr_label['fg']= pre_prayer_color
        tomorrow_fajr_athan_label['fg'] = pre_prayer_color
        tomorrow_fajr_iqama_label['fg'] = pre_prayer_color

        today_fajr_label['fg']= next_prayer_color
        today_fajr_athan_label['fg'] = next_prayer_color
        today_fajr_iqama_label['fg'] = next_prayer_color

    elif(hour_time >= fajr_time and hour_time <= thuhr_time):
        today_fajr_label['fg']= pre_prayer_color
        today_fajr_athan_label['fg'] = pre_prayer_color
        today_fajr_iqama_label['fg'] = pre_prayer_color

        today_sunrise_label['fg'] = current_prayer_color

        today_thuhr_label['fg']= next_prayer_color
        today_thuhr_athan_label['fg'] = next_prayer_color
        today_thuhr_iqama_label['fg'] = next_prayer_color
    elif(hour_time >= thuhr_time and hour_time <= asr_time):
        today_sunrise_label['fg'] = pre_prayer_color
        
        today_thuhr_label['fg']= current_prayer_color
        today_thuhr_athan_label['fg'] = current_prayer_color
        today_thuhr_iqama_label['fg'] = current_prayer_color

        today_asr_label['fg']= next_prayer_color
        today_asr_athan_label['fg'] = next_prayer_color
        today_asr_iqama_label['fg'] = next_prayer_color
    elif(hour_time >=asr_time and hour_time <= maghrib_time):
        today_thuhr_label['fg']= pre_prayer_color
        today_thuhr_athan_label['fg'] = pre_prayer_color
        today_thuhr_iqama_label['fg'] = pre_prayer_color
        
        today_asr_label['fg']= current_prayer_color
        today_asr_athan_label['fg'] = current_prayer_color
        today_asr_iqama_label['fg'] = current_prayer_color

        today_maghrib_label['fg']= next_prayer_color
        today_maghrib_athan_label['fg'] = next_prayer_color
        today_maghrib_iqama_label['fg'] = next_prayer_color
    elif(hour_time >= maghrib_time and hour_time <= isha_time):
        today_asr_label['fg']= pre_prayer_color
        today_asr_athan_label['fg'] = pre_prayer_color
        today_asr_iqama_label['fg'] = pre_prayer_color
        
        today_maghrib_label['fg']= current_prayer_color
        today_maghrib_athan_label['fg'] = current_prayer_color
        today_maghrib_iqama_label['fg'] = current_prayer_color

        today_isha_label['fg']= next_prayer_color
        today_isha_athan_label['fg'] = next_prayer_color
        today_isha_iqama_label['fg'] = next_prayer_color
    elif(hour_time >= isha_time):
        today_maghrib_label['fg']= pre_prayer_color
        today_maghrib_athan_label['fg'] = pre_prayer_color
        today_maghrib_iqama_label['fg'] = pre_prayer_color

        today_isha_label['fg']= current_prayer_color
        today_isha_athan_label['fg'] = current_prayer_color
        today_isha_iqama_label['fg'] = current_prayer_color

        tomorrow_fajr_label['fg']= next_prayer_color
        tomorrow_fajr_athan_label['fg'] = next_prayer_color
        tomorrow_fajr_iqama_label['fg'] = next_prayer_color

    clock_label ['text'] = current_time # to assign current time to clock label
# to flash the different announcements every 30 sec
    global counter
    global i    
    
    if(counter <Time and i< len(photos)):
        add_photo_now = photos[i]
        counter += 1
    else:
        add_photo_now = photos[i]
        counter = 0
        i+=1
        
    if (i == len(photos)):
        i = 0
    
    add['image'] = add_photo_now
    clock_label.after(1000,display_time) # rerun display_time() after 1sec


# reading prayer schedule excel file
data = pd.read_excel('prayer_schedule.xlsx',sheet_name=0,header=0) # read prayer time excelsheet

#tk window declaration with name of Prayer Time Portland Oregon
window = tk.Tk(className='Prayer Time Portland Oregon')
# set window size

#window.geometry("1600x1200")
width_value = window.winfo_screenwidth()
height_value = window.winfo_screenheight()
window.geometry("%dx%d+0+0" %(width_value, height_value))

stop = 0
#set window text_color
window.configure(bg='white')
#window.rowconfigure(0, minsize=50)
#window.rowconfigure(1, minsize=50, weight =1)

photo_list =[] # array to store the list of the photos 
photos = [] # array to store the list of the resized photos 

#main_folder ="/home/ubuntu/Desktop/ptd/ads"
# main_folder ="C://Users//ICCH_//Desktop//ptd//ads"
#main_folder ="C://Users//ICCH_//My Drive//Ads transfer"
main_folder ="C://Users//melghaza//OneDrive - Intel Corporation//Desktop//ICCH//prayer_time_display//My_prayer_time_display//Version8//Ads"
# main_folder = os.path.dirname(__file__) + "/ads"
photo_path =os.listdir(main_folder) # array to store the path of the photos 

background = Image.open("background.png")
background = background.resize((width_value, height_value))
bg = ImageTk.PhotoImage(background)

# declaring the counter for controlling the add animation
counter = 0
i =0
j =0
# declaring the time limit for controlling the add animation
Time = 10 # 10 seconds per photo

# assigning the whole path to the photo list
for file in photo_path:
    new_file = os.path.join(main_folder, file)
    photo_list.append(new_file)

# reading and loading the photos
for file in photo_list:
    load = Image.open(file)
    load1 = load.resize((height_value,height_value)) # reszing the ad photo to 1520*1080
    photos.append(ImageTk.PhotoImage(load1))
   

bg_label = tk.Label(text="",bg='white', image = bg)
add = tk.Button( command = quit , image = photos[0], borderwidth=0) # defining add as image and using photo2 for it "add photo", also stops the program when hit
#add = tk.Button( command=launch , image = photos[0]) # defining add as image and using photo2 for it "add photo", also stops the program when hit

# defining font variables to be used for display
font_info = 'Helvetica', round(24 * (height_value/1080)), 'bold'
font_info1 = 'Helvetica', round(24 * (height_value/1080)), 'bold'
font_info2 = 'Helvetica', round(24 * (height_value/1080)), 'bold'

text_color = "black" # define text color
# defining the different variables to be shown with background color "bg", text color "fg", and font info "font_info"

times = tk.Frame(window, width=width_value/3.2, height=height_value/1.5, bg='white')

clock_label = tk.Label(times, bg='white', fg=text_color, font = font_info2)

today_label = tk.Label(times, bg='white', fg=text_color,font= font_info1)
label1a = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)
label2a = tk.Label(times, bg='white', text="Athan", fg=text_color,font= font_info2)
label3a = tk.Label(times, bg='white', text="Iqama", fg=text_color,font= font_info2)
today_fajr_label = tk.Label(times, bg='white', text="Fajr", fg=text_color,font= font_info2)
today_thuhr_label = tk.Label(times, bg='white', text="Thuhr", fg=text_color,font= font_info2)
today_asr_label = tk.Label(times, bg='white', text="Asr", fg=text_color,font= font_info2)
today_maghrib_label = tk.Label(times, bg='white', text="Maghrib", fg=text_color,font= font_info2)
today_isha_label = tk.Label(times, bg='white', text="Ishaa", fg=text_color,font= font_info2)

tomorrow_label = tk.Label(times, bg='white', fg=text_color,font= font_info1)
label1b = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)
#label2b = tk.Label(times, bg='white', text="Athan", bg=text_color, fg="white",font= font_info)
#label3b = tk.Label(times, bg='white', text="Iqama", bg=text_color, fg="white",font= font_info)
tomorrow_fajr_label = tk.Label(times, bg='white', text="Fajr", fg=text_color,font= font_info2)
tomorrow_thuhr_label = tk.Label(times, bg='white', text="Thuhr",fg=text_color,font= font_info2)
tomorrow_asr_label = tk.Label(times, bg='white', text="Asr", fg=text_color,font= font_info2)
tomorrow_maghrib_label = tk.Label(times, bg='white', text="Maghrib", fg=text_color,font= font_info2)
tomorrow_isha_label = tk.Label(times, bg='white', text="Ishaa", fg=text_color,font= font_info2)
label9 = tk.Label(times, bg='white', text="", fg=text_color,font= font_info)

# today data
today_fajr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_fajr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
today_sunrise_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
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
tomorrow_sunrise_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_thuhr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_thuhr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_asr_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_asr_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_maghrib_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_maghrib_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_isha_athan_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
tomorrow_isha_iqama_label = tk.Label(times, bg='white', fg=text_color,font= font_info)
# define grid and the postion of the different variables in the grid
# bg_label.grid(row=0, column=0)
bg_label.place(x=0, y=0)
add.place(x=width_value-height_value)
times.place(x=208 * (width_value/1920), y=223 * (height_value/1080))

# label0.grid(row=0, columnspan=3)
# add.grid(row= 0, column = 4, rowspan =18)
clock_label.grid(row =0, column=0, columnspan =3)
today_label.grid(row=1, column=1, columnspan = 2)
label1a.grid(row=2, column=0)
label2a.grid(row=2, column=1)
label3a.grid(row=2, column=2)
today_fajr_label.grid(row=3, column=0)
today_thuhr_label.grid(row=4, column=0)
today_asr_label.grid(row=5, column=0)
today_maghrib_label.grid(row=6, column=0)
today_isha_label.grid(row=7, column=0)
tomorrow_label.grid(row=9, column=1, columnspan = 2)

tomorrow_fajr_label.grid(row=11, column=0)
tomorrow_thuhr_label.grid(row=12, column=0)
tomorrow_asr_label.grid(row=13, column=0)
tomorrow_maghrib_label.grid(row=14, column=0)
tomorrow_isha_label.grid(row=15, column=0)

today_fajr_athan_label.grid(row=3, column=1)
today_fajr_iqama_label.grid(row=3, column=2)
today_thuhr_athan_label.grid(row=4, column=1)
today_thuhr_iqama_label.grid(row=4, column=2)
today_asr_athan_label.grid(row=5, column=1)
today_asr_iqama_label.grid(row=5, column=2)
today_maghrib_athan_label.grid(row=6, column=1)
today_maghrib_iqama_label.grid(row=6, column=2)
today_isha_athan_label.grid(row=7, column=1)
today_isha_iqama_label.grid(row=7, column=2)

tomorrow_fajr_athan_label.grid(row=11, column=1)
tomorrow_fajr_iqama_label.grid(row=11, column=2)
tomorrow_thuhr_athan_label.grid(row=12, column=1)
tomorrow_thuhr_iqama_label.grid(row=12, column=2)
tomorrow_asr_athan_label.grid(row=13, column=1)
tomorrow_asr_iqama_label.grid(row=13, column=2)
tomorrow_maghrib_athan_label.grid(row=14, column=1)
tomorrow_maghrib_iqama_label.grid(row=14, column=2)
tomorrow_isha_athan_label.grid(row=15, column=1)
tomorrow_isha_iqama_label.grid(row=15, column=2)
# label0b.grid(row=17, columnspan=3)

display_time() # to call display_time() function
window.resizable(False, True) # to make the window resizable
window.bind()
#to get red of the tilte par
#window.overrideredirect(1)
# window.wm_attributes('-type','splash')
window.wm_attributes('-fullscreen', 1)
window.bind()
window.mainloop()

