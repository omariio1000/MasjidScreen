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
import os
import argparse
import trivia
import textwrap
import json

photos = [] # array to store the list of the resized photos 
tq_image = []
# declaring the counter for controlling the flyer animation
counter = 0
i =0
j =0
# declaring the time limit for controlling the flyer animation
Time = 10 # 10 seconds per photo
testDay = 0

global updated
global ramadan_updated

class Labels:
    def __init__(self, times, bg_color, text_color, font_info):
            self.clock_label = tk.Label(times,bg=bg_color, fg=text_color, font = font_info)

            self.today_date_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.today_space_label = tk.Label(times,bg=bg_color, text="", fg=text_color,font= font_info)
            self.athan_label = tk.Label(times,bg=bg_color, text="Athan", fg=text_color,font= font_info)
            self.iqama_label = tk.Label(times,bg=bg_color, text="Iqama", fg=text_color,font= font_info)
            self.today_fajr_label = tk.Label(times,bg=bg_color, text="Fajr", fg=text_color,font= font_info)
            self.today_shurooq_label = tk.Label(times,bg=bg_color, text="Shurooq", fg=text_color,font= font_info)
            self.today_thuhr_label = tk.Label(times,bg=bg_color, text="Thuhr", fg=text_color,font= font_info)
            self.today_asr_label = tk.Label(times,bg=bg_color, text="Asr", fg=text_color,font= font_info)
            self.today_maghrib_label = tk.Label(times,bg=bg_color, text="Maghrib", fg=text_color,font= font_info)
            self.today_isha_label = tk.Label(times,bg=bg_color, text="Ishaa", fg=text_color,font= font_info)

            self.tomorrow_date_label = tk.Label(times,bg=bg_color, fg=text_color,font= font_info)
            self.tomorrow_space_label = tk.Label(times,bg=bg_color, text="", fg=text_color,font= font_info)

            self.tomorrow_fajr_label = tk.Label(times,bg=bg_color, text="Fajr", fg=text_color,font= font_info)
            self.tomorrow_shurooq_label = tk.Label(times,bg=bg_color, text="Shurooq", fg=text_color,font= font_info)
            self.tomorrow_thuhr_label = tk.Label(times,bg=bg_color, text="Thuhr",fg=text_color,font= font_info)
            self.tomorrow_asr_label = tk.Label(times,bg=bg_color, text="Asr", fg=text_color,font= font_info)
            self.tomorrow_maghrib_label = tk.Label(times,bg=bg_color, text="Maghrib", fg=text_color,font= font_info)
            self.tomorrow_isha_label = tk.Label(times,bg=bg_color, text="Ishaa", fg=text_color,font= font_info)

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

class RamdadanLabels:
    def __init__(self, winnerFrame, questionFrame, bg_color, text_color, font_info1, font_info2, font_info3):
        # winner frame
        self.winner_one_first = tk.Label(winnerFrame, bg=bg_color, fg=text_color, font=font_info1)
        self.winner_one_last = tk.Label(winnerFrame, bg=bg_color, fg=text_color, font=font_info1)
        
        self.winner_two_first = tk.Label(winnerFrame, bg=bg_color, fg=text_color, font=font_info1)
        self.winner_two_last = tk.Label(winnerFrame, bg=bg_color, fg=text_color, font=font_info1)

        self.winner_three_first = tk.Label(winnerFrame, bg=bg_color, fg=text_color, font=font_info1)
        self.winner_three_last = tk.Label(winnerFrame, bg=bg_color, fg=text_color, font=font_info1)

        # question frame
        self.question_one = tk.Label(questionFrame, bg=bg_color, fg=text_color, font=font_info2)
        self.question_one_options = tk.Label(questionFrame, bg=bg_color, fg=text_color, font=font_info3)
        
        self.question_two = tk.Label(questionFrame, bg=bg_color, fg=text_color, font=font_info2)
        self.question_two_options = tk.Label(questionFrame, bg=bg_color, fg=text_color, font=font_info3)

        self.question_three = tk.Label(questionFrame, bg=bg_color, fg=text_color, font=font_info2)
        self.question_three_options = tk.Label(questionFrame, bg=bg_color, fg=text_color, font=font_info3)

        # qr code
        self.trivia_qr = tk.Label(text="")

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def update_photos(height_value):
    with open('../config.json', "r") as file:
        config = json.load(file)

    main_folder = config["flyers"]
    if not os.path.exists(main_folder):
        main_folder = os.path.dirname(__file__) + "\\..\\sample ads"

    photo_path = os.listdir(main_folder) # array to store the path of the photos 
    photo_list = [] # array to store the list of the photos 
    photos.clear()

    print("\n[", end="")

    # assigning the whole path to the photo list
    for file in photo_path:
        if (file.endswith(".png")):
            new_file = os.path.join(main_folder, file)
            photo_list.append(new_file)
            print(f"'{file}'", end=", " if file != photo_path[-1] else "")
        else:
            photo_path.remove(file)
    print("]")

    # reading and loading the photos
    for file in photo_list:
        load = Image.open(file)
        load1 = load.resize((height_value,height_value)) # reszing the ad photo
        photos.append(ImageTk.PhotoImage(load1))
    
    print("Photos updated from \"", main_folder, "\" at", tm.strftime('%#m/%#d/%Y %#I:%M:%S %p') + "\n")
    
def quit(window):# close Admin window if cancel is clicked
    window.destroy()  

def testHandler(ramadan_labels, height_value):
    global testDay
    testDay += 1
    update_trivia(testDay, ramadan_labels, height_value, test=True)

def update_trivia(day, ramadan_labels, height_value, test=False):
    print(f"Day {day} of Ramadan")

    if not trivia.check_winners_updated(str(day - 1)):
        winners = trivia.get_winners(day - 1)
        trivia.log_winners(str(day - 1), winners, test)
    else:
        winners = trivia.get_past_winners(str(day - 1))

    if winners:        
        if len(winners) >= 1:
            ramadan_labels.winner_one_first['text'] = winners[0][0].split(" ")[0]
            ramadan_labels.winner_one_last['text'] = winners[0][0].split(" ")[1]
            ramadan_labels.winner_two_first['text'] = ""
            ramadan_labels.winner_two_last['text'] = ""
            ramadan_labels.winner_three_first['text'] = ""
            ramadan_labels.winner_three_last['text'] = ""

        if len(winners) >= 2:
            ramadan_labels.winner_two_first['text'] = winners[1][0].split(" ")[0]
            ramadan_labels.winner_two_last['text'] = winners[1][0].split(" ")[1]


        if len(winners) >= 3:
            ramadan_labels.winner_three_first['text'] = winners[2][0].split(" ")[0]
            ramadan_labels.winner_three_last['text'] = winners[2][0].split(" ")[1]
    else:
        ramadan_labels.winner_one_first['text'] = "No Winners"
        ramadan_labels.winner_one_last['text'] = "Yesterday"
        ramadan_labels.winner_two_first['text'] = ""
        ramadan_labels.winner_two_last['text'] = ""
        ramadan_labels.winner_three_first['text'] = ""
        ramadan_labels.winner_three_last['text'] = ""

    question, option1, option2, option3 = trivia.get_form_questions_options(day)

    ramadan_labels.question_one['text'] = '\n'.join(textwrap.wrap(question[0], width=95))
    ramadan_labels.question_one_options['text'] = f"a) {option1[0]}  b) {option2[0]}  c) {option3[0]}"
    ramadan_labels.question_two['text'] = '\n'.join(textwrap.wrap(question[1], width=95))
    ramadan_labels.question_two_options['text'] = f"a) {option1[1]}  b) {option2[1]}  c) {option3[1]}"
    ramadan_labels.question_three['text'] = '\n'.join(textwrap.wrap(question[2], width=95))
    ramadan_labels.question_three_options['text'] = f"a) {option1[2]}  b) {option2[2]}  c) {option3[2]}"

    trivia.make_qr(day)
    trivia_qr_image = Image.open('trivia.png')
    trivia_qr_image = trivia_qr_image.resize((int(height_value * 0.1851851852), int(height_value * 0.1851851852)))
    tq_image.clear()
    tq_image.append(ImageTk.PhotoImage(trivia_qr_image))
    ramadan_labels.trivia_qr['image'] = tq_image[0]
    print()

def display_time(labels, data, flyer, updated, ramadan, height_value, flyer_height, ramadan_labels, ramadan_updated):
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
            update_photos(flyer_height)
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

        # If Ramadan this is where winner update logic will occur
        if ramadan and not ramadan_updated:
            update_trivia(trivia.get_trivia_day(), ramadan_labels, height_value)
            ramadan_updated = True
        
    elif(hour_time >= isha_time):
        ramadan_updated = False

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
    
    labels.clock_label.after(1000,display_time, labels, data, flyer, updated, ramadan, height_value, flyer_height, ramadan_labels, ramadan_updated) # rerun display_time() after 1sec

def main():
    parser = argparse.ArgumentParser(description="Prayer Time and Flyers Display")
    parser.add_argument("-r", action="store_true", help="enables ramadan mode")
    parser.add_argument("-t", action="store_true", help="enables test mode")
    args = parser.parse_args()

    # reading prayer schedule excel file
    data = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/../prayer_schedule.xlsx',sheet_name=0,header=0) # read prayer time excelsheet

    #tk window declaration with name of Prayer Time Portland Oregon
    window = tk.Tk(className='Prayer Time Portland Oregon')
    # set window size

    width_value = window.winfo_screenwidth()
    height_value = window.winfo_screenheight()
    window.geometry("%dx%d+0+0" %(width_value, height_value))

    #set window text_color
    window.configure(bg='white')

    background_path = "/../resources/Ramadan.png" if args.r else "/../resources/Background.png"

    background = Image.open(os.path.dirname(os.path.abspath(__file__)) + background_path)
    background = background.resize((width_value, height_value))
    bg = ImageTk.PhotoImage(background)

    with open('../config.json', "r") as file:
        config = json.load(file)

    socials_link = config["socials"]
    donate_link = config["donate"]
    website_link = config["website"]

    trivia.make_qr_with_link(socials_link, "socials.png")
    trivia.make_qr_with_link(donate_link, "donate.png")
    trivia.make_qr_with_link(website_link, "website.png")

    socials_qr_image = Image.open('socials.png')
    socials_qr_image = socials_qr_image.resize((int(0.1157407407 * height_value), int(0.1157407407 * height_value)))
    socials = ImageTk.PhotoImage(socials_qr_image)

    donate_qr_image = Image.open('donate.png')
    donate_qr_image = donate_qr_image.resize((int(0.1157407407 * height_value), int(0.1157407407 * height_value)))
    donate = ImageTk.PhotoImage(donate_qr_image)

    website_qr_image = Image.open('website.png')
    website_qr_image = website_qr_image.resize((int(0.1157407407 * height_value), int(0.1157407407 * height_value)))
    website = ImageTk.PhotoImage(website_qr_image)

    socials_label = tk.Label(text="",bg='white', image = socials)
    donate_label = tk.Label(text="", bg='white', image=donate)
    website_label = tk.Label(text="", bg='white', image=website)

    update_photos(height_value if not args.r else int(height_value/1.5))

    bg_label = tk.Label(text="",bg='white', image = bg)
    flyer = tk.Button( command = lambda: update_photos(height_value if not args.r else int(height_value/1.5)) , image = photos[0], borderwidth=0) # defining flyer as image and using photo2 for it "flyer photo", also stops the program when hit
    
    if args.t:
        testDay = 0
        flyer = tk.Button( command = lambda: testHandler(ramadan_labels, height_value), image = photos[0], borderwidth=0) # defining flyer as image and using photo2 for it "flyer photo", also stops the program when hit
        
    window.bind("<Escape>", lambda e: quit(window))

    # defining font variables to be used for display
    font_info = 'Helvetica', round(30 * (height_value/1080)), 'bold'


    text_color = "white" if args.r else "black" # define text color
    bg_color = _from_rgb((0, 25, 125)) if args.r else "white"
    # defining the different variables to be shown with background color "bg", text color "fg", and font info "font_info"

    times = tk.Frame(window, width=width_value/3.4, height=height_value/1.35,bg=bg_color)

    labels = Labels(times, bg_color, text_color, font_info)

    if args.r:
        font_info1 = 'Helvetica', round(24 * (height_value/1080)), 'bold'
        font_info2 = 'Helvetica', round(16 * (height_value/1080)), 'bold'
        font_info3 = 'Helvetica', round(14 * (height_value/1080))

        day = trivia.get_trivia_day()

        winners = tk.Frame(window, bg=bg_color)
        questions = tk.Frame(window, bg=bg_color)

        ramadan_labels = RamdadanLabels(winners, questions, bg_color, text_color, font_info1, font_info2, font_info3)

        ramadan_labels.trivia_qr.place(x=int(width_value * 0.4739583333), y=int(height_value * 0.4592013889))
        winners.place(x=int(width_value * 0.5260416667), y=int(height_value * 0.2893518519), anchor="center")
        questions.place(x=int(width_value * 0.71875), y=int(height_value * 0.8425925926), anchor="center")
        space_label_one = tk.Label(winners, height=1, text="", fg=bg_color, bg=bg_color)
        space_label_two = tk.Label(winners, height=1, text="", fg=bg_color, bg=bg_color)
        space_label_three = tk.Label(questions, height=1, text="", fg=bg_color, bg=bg_color)
        space_label_four = tk.Label(questions, height=1, text="", fg=bg_color, bg=bg_color)

        ramadan_labels.winner_one_first.grid(row=0)
        ramadan_labels.winner_one_last.grid(row=1)
        space_label_one.grid(row=2)
        ramadan_labels.winner_two_first.grid(row=3)
        ramadan_labels.winner_two_last.grid(row=4)
        space_label_two.grid(row=5)
        ramadan_labels.winner_three_first.grid(row=6)
        ramadan_labels.winner_three_last.grid(row=7)

        ramadan_labels.question_one.grid(row=0)
        ramadan_labels.question_one_options.grid(row=1)
        space_label_three.grid(row=2)
        ramadan_labels.question_two.grid(row=3)
        ramadan_labels.question_two_options.grid(row=4)
        space_label_four.grid(row=5)
        ramadan_labels.question_three.grid(row=6)
        ramadan_labels.question_three_options.grid(row=7)

        update_trivia(day, ramadan_labels, height_value)

    bg_label.place(x=0, y=0)
    flyer.place(x=width_value-height_value if not args.r else width_value-height_value + (height_value - int(height_value/1.5) - int(height_value * 0.0138888889)), y = int(height_value * 0.0138888889) if args.r else None)
    times.place(x=int(width_value * 0.1822916667), y=int(height_value * 0.5), anchor="center")

    socials_label.place(x=int(width_value * 0.3828125), y=int(height_value * 0.2844907407), anchor="center")
    donate_label.place(x=int(width_value * 0.3828125), y=int(height_value * 0.6273148148), anchor="center")
    website_label.place(x=int(width_value * 0.3828125), y=int(height_value * 0.8356481481), anchor="center")

    bg_label.lower()

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

    updated = False
    ramadan_updated = False
    display_time(labels, data, flyer, False, args.r, height_value, height_value if not args.r else int(height_value/1.5), ramadan_labels if args.r else None, False) # to call display_time() function
    window.resizable(False, True) # to make the window resizable
    window.bind()

    window.wm_attributes('-fullscreen', 1)
    window.bind()
    window.mainloop()

if __name__ == '__main__':
    main()