"""
Started Oct 20 2025 @14:40

Created by Yusuf Darwish, designed by Mahdi Elghazali and Omar Nassar

@author: Mahdi Elghazali and Omar Nassar

Converted from Tkinter to Pyqt5"""

import sys
import os
import time as tm
from datetime import datetime
import pandas as pd
import argparse
import json
import textwrap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                              QPushButton, QFrame, QVBoxLayout, QHBoxLayout, 
                              QGridLayout)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
import trivia
from stats import printAllStats

# declare and set the main directory for use in file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


config_path = os.path.join(BASE_DIR, '..', 'config.json') 

photos = [] # array to store the list of the resized photos 
tq_image = [] # workaround to store trivia qr code and update during run time

# counters for controlling the flyer animation
counter = 0
i =0
j =0

Time = 10 # time limit (seconds) for controlling the flyer animation
testDay = 0 #iterate through ramdadan days in test mode

global updated
global ramadan_updated

class Labels:
    """Class to store prayer time labels for cleaner code"""
    def __init__(self, parent, bg_color, text_color, font):

        def make_label(parent, text="", bg_color=bg_color, text_color=text_color, font=font):
            label = QLabel(text, parent)
            label.setStyleSheet(f"background-color: transparent; color: {text_color}; border: none;")
            if font:
                label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            return label



        # Main clock and date labels
        self.clock_label = make_label(parent)
        self.today_date_label = make_label(parent)
        self.today_space_label = make_label(parent, "")
        self.athan_label = make_label(parent, "Athan")
        self.iqama_label = make_label(parent, "Iqama")

        self.clock_label.setStyleSheet("background: transparent;")

        # Today's prayer names
        self.today_fajr_label = make_label(parent, "Fajr")
        self.today_shurooq_label = make_label(parent, "Shurooq")
        self.today_thuhr_label = make_label(parent, "Thuhr")
        self.today_asr_label = make_label(parent, "Asr")
        self.today_maghrib_label = make_label(parent, "Maghrib")
        self.today_isha_label = make_label(parent, "Isha")

        # Tomorrow's prayer names
        self.tomorrow_date_label = make_label(parent)
        self.tomorrow_space_label = make_label(parent, "")
        self.tomorrow_fajr_label = make_label(parent, "Fajr")
        self.tomorrow_shurooq_label = make_label(parent, "Shurooq")
        self.tomorrow_thuhr_label = make_label(parent, "Thuhr")
        self.tomorrow_asr_label = make_label(parent, "Asr")
        self.tomorrow_maghrib_label = make_label(parent, "Maghrib")
        self.tomorrow_isha_label = make_label(parent, "Isha")

        # Today's Athan/Iqama times
        self.today_fajr_athan_label = make_label(parent)
        self.today_fajr_iqama_label = make_label(parent)
        self.today_shurooq_athan_label = make_label(parent)
        self.today_shurooq_iqama_label = make_label(parent, "")
        self.today_thuhr_athan_label = make_label(parent)
        self.today_thuhr_iqama_label = make_label(parent)
        self.today_asr_athan_label = make_label(parent)
        self.today_asr_iqama_label = make_label(parent)
        self.today_maghrib_athan_label = make_label(parent)
        self.today_maghrib_iqama_label = make_label(parent)
        self.today_isha_athan_label = make_label(parent)
        self.today_isha_iqama_label = make_label(parent)

        # Tomorrow's Athan/Iqama times
        self.tomorrow_fajr_athan_label = make_label(parent)
        self.tomorrow_fajr_iqama_label = make_label(parent)
        self.tomorrow_shurooq_athan_label = make_label(parent)
        self.tomorrow_shurooq_iqama_label = make_label(parent, "")
        self.tomorrow_thuhr_athan_label = make_label(parent)
        self.tomorrow_thuhr_iqama_label = make_label(parent)
        self.tomorrow_asr_athan_label = make_label(parent)
        self.tomorrow_asr_iqama_label = make_label(parent)
        self.tomorrow_maghrib_athan_label = make_label(parent)
        self.tomorrow_maghrib_iqama_label = make_label(parent)
        self.tomorrow_isha_athan_label = make_label(parent)
        self.tomorrow_isha_iqama_label = make_label(parent)


class RamadanLabels:
      """Class to store ramadan trivia labels"""

      def __init__(self, winner_parent, question_parent, bg_color, text_color, font1, font2, font3):
            
            # winner frame
            self.winner_one_first = QLabel(winner_parent)
            self.winner_one_first.setStyleSheet(f"background-color: {bg_color}: color: {text_color}")
            self.winner_one_first.setFont(font1)

            self.winner_one_last = QLabel(winner_parent)
            self.winner_one_last.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_one_last.setFont(font1)
            
            self.winner_two_first = QLabel(winner_parent)
            self.winner_two_first.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_two_first.setFont(font1)
            
            self.winner_two_last = QLabel(winner_parent)
            self.winner_two_last.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_two_last.setFont(font1)

            self.winner_three_first = QLabel(winner_parent)
            self.winner_three_first.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_three_first.setFont(font1)
            
            self.winner_three_last = QLabel(winner_parent)
            self.winner_three_last.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_three_last.setFont(font1)

            # question frame
            self.question_one = QLabel(question_parent)
            self.question_one.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_one.setFont(font2)
            
            self.question_one_options = QLabel(question_parent)
            self.question_one_options.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_one_options.setFont(font3)
            
            self.question_two = QLabel(question_parent)
            self.question_two.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_two.setFont(font2)
            
            self.question_two_options = QLabel(question_parent)
            self.question_two_options.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_two_options.setFont(font3)

            self.question_three = QLabel(question_parent)
            self.question_three.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_three.setFont(font2)
            
            self.question_three_options = QLabel(question_parent)
            self.question_three_options.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_three_options.setFont(font3)

            # qr code
            self.trivia_qr = QLabel("")

def rgb_to_hex(rgb):
      """convert rgb to hex"""
      r, g, b = rgb
      return f'#{r:02x}{g:02x}{b:02x}'

def update_photos(height_value):
    """Update flyer photos label"""
    with open(config_path, "r") as file:
        config = json.load(file)
    
    main_folder = config["flyers"]
    if not os.path.exists(main_folder):
         main_folder = os.path.join(os.path.dirname(__file__), "..", "sample ads")
         main_folder = os.path.abspath(main_folder)
    
    photo_path = os.listdir(main_folder)
    photo_list = []
    photos.clear()

    print("\n[", end="")

    #assigning whole path to photo list

    for file in photo_path:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            new_file = os.path.join(main_folder, file)
            photo_list.append(new_file)
            print(f"'{file}", end=", " if file != photo_path[-1] else "")
        else:
            photo_path.remove(file)
    
    print("]")

    # reading and loading the photos

    for file in photo_list:
        load = QPixmap(file)
        load1 = load.scaled(height_value,height_value, Qt.KeepAspectRatio) 
        photos.append(load1)

    print(f"Photos updated from \"{os.path.abspath(main_folder)}\" at {tm.strftime('%#m/%#d/%Y %#I:%M:%S %p')} \n")


def update_trivia(day, ramadan_labels, height_value, test=False):
    """Updating trivia questions and winners"""
    print(f"Day {day} of Ramadan")

    if (day < 0 or day > 30):
        trivia.make_qr_with_link("icc-hillsboro.org", 'trivia.png')
        ramadan_labels.question_one.setText('')
        ramadan_labels.question_one_options.setText('')

        if day > 0:
            ramadan_labels.question_two.setText("Thank you for participating!")
            ramadan_labels.question_two_options.setText("We hope you join us again next year inshaAllah!")
        else:
            ramadan_labels.question_two.setText("Ramadan is starting soon!")
            ramadan_labels.question_two_options.setText("We hope you join us for trivia this year inshaAllah!")

        ramadan_labels.question_three.setText('')
        ramadan_labels.question_three_options.setText('')

        ramadan_labels.winner_one_first.setText("")
        ramadan_labels.winner_one_last.setText("")
        ramadan_labels.winner_two_first.setText("")
        ramadan_labels.winner_two_last.setText("")
        ramadan_labels.winner_three_first.setText("")
        ramadan_labels.winner_three_last.setText("")
    else:
        trivia.make_qr(day)
        question, option1, option2, option3 = trivia.get_form_questions_options(day)
        ramadan_labels.question_one.setText('\n'.join(textwrap.wrap(question[0], width=95)))
        ramadan_labels.question_one_options.setText(f"a) {option1[0]}  b) {option2[0]}  c) {option3[0]}")
        ramadan_labels.question_two.setText('\n'.join(textwrap.wrap(question[1], width=95)))
        ramadan_labels.question_two_options.setText(f"a) {option1[1]}  b) {option2[1]}  c) {option3[1]}")
        ramadan_labels.question_three.setText('\n'.join(textwrap.wrap(question[2], width=95)))
        ramadan_labels.question_three_options.setText(f"a) {option1[2]}  b) {option2[2]}  c) {option3[2]}")

    if day <= 31:
        if not trivia.check_winners_updated(str(day - 1)):
            winners = trivia.get_winners(day - 1)
            trivia.log_winners(str(day - 1), winners, test)
        else:
            winners = trivia.get_past_winners(str(day - 1))
        winners = [sublist[:1] for sublist in winners]
        print(f"Winners: {winners}")

        if winners:
            if len(winners) >= 1:
                ramadan_labels.winner_one_first.setText(winners[0][0].split(" ")[0].capitalize())
                ramadan_labels.winner_one_last.setText(winners[0][0].split(" ")[-1].capitalize())
                ramadan_labels.winner_two_first.setText("")
                ramadan_labels.winner_two_last.setText("")
                ramadan_labels.winner_three_first.setText("")
                ramadan_labels.winner_three_last.setText("")

            if len(winners) >= 2:
                ramadan_labels.winner_two_first.setText(winners[1][0].split(" ")[0].capitalize())
                ramadan_labels.winner_two_last.setText(winners[1][0].split(" ")[-1].capitalize())

            if len(winners) >= 3:
                ramadan_labels.winner_three_first.setText(winners[2][0].split(" ")[0].capitalize())
                ramadan_labels.winner_three_last.setText(winners[2][0].split(" ")[-1].capitalize())
        else:
            ramadan_labels.winner_one_first.setText("No Winners")
            ramadan_labels.winner_one_last.setText("Yesterday")
            ramadan_labels.winner_two_first.setText("")
            ramadan_labels.winner_two_last.setText("")
            ramadan_labels.winner_three_first.setText("")
            ramadan_labels.winner_three_last.setText("")

    pixmap = QPixmap('trivia.png')
    pixmap = pixmap.scaled(int(height_value * 0.1851851852), int(height_value * 0.1851851852), 
                           Qt.KeepAspectRatio, Qt.SmoothTransformation)
    tq_image.clear()
    tq_image.append(pixmap)
    ramadan_labels.trivia_qr.setPixmap(tq_image[0])
    print("\nStats so far:")
    printAllStats()
    print()

def display_time(labels, data, flyer, updated, ramadan, height_value, flyer_height, ramadan_labels, ramadan_updated, test):
    """Main program loop that updates times"""
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

    next_prayer_color = rgb_to_hex((255, 0, 0))# to assign color to next prayer
    pre_prayer_color = rgb_to_hex((255,255,255)) if ramadan else rgb_to_hex((0,0,0))# to assign color to next prayer
    current_prayer_color = rgb_to_hex((0,200,0)) if ramadan else rgb_to_hex((0,50,0)) # to assign color to next prayer


    # to highlight the next prayer time

    if (":00" in hour_time):
        if (updated is False):
            update_photos(flyer_height)
            updated = True
    else:
        updated = False

    if(hour_time < fajr_time):
        ramadan_updated = False

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

        # If Ramadan this is where winner update logic will occur
        if ramadan and not ramadan_updated and not test:
            update_trivia(trivia.get_trivia_day(), ramadan_labels, height_value)
            ramadan_updated = True

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
    
    labels.clock_label.after(1000,display_time, labels, data, flyer, updated, ramadan, height_value, flyer_height, ramadan_labels, ramadan_updated, test) # rerun display_time() after 1sec

class PrayerTimesWindow(QMainWindow):
    def __init__(self, args, config, data):
        super().__init__()
        self.args = args
        self.config = config
        self.data = data
        self.updated = False
        self.ramadan_updated = False

        self.init_ui()

        #timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_time)
        self.timer.start(1000)
    
    def init_ui(self):
        self.setWindowTitle('PyQt5 Prayer Times ICCH - IKworks')

        #dimensions
        screen = QApplication.primaryScreen().geometry()
        width_value = screen.width()
        height_value = screen.height()

        self.setGeometry(0, 0, width_value, height_value)

        #widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #background
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        bg_file = "Ramadan.png" if self.args.r else "Background.png"
        background_path = os.path.join(BASE_DIR, '..', 'resources', bg_file)

        bg_label = QLabel(central_widget)
        bg_image = QPixmap(background_path)
        bg_image = bg_image.scaled(width_value, height_value, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        bg_label.setPixmap(bg_image)
        bg_label.setGeometry(0, 0, width_value, height_value)
        bg_label.setStyleSheet("background-color: black;")  # fills any subpixel edge
        bg_label.setAlignment(Qt.AlignCenter)

        #colors, fonts
        text_color = "white" if self.args.r else "black"
        bg_color = rgb_to_hex((0, 25, 125)) if self.args.r else "white"
        font_size = round(30 * (height_value/1080))
        font = QFont('Helvetica', font_size, QFont.Bold)

        #prayer times frame
        times_frame = QFrame(central_widget)
        times_frame.setStyleSheet(f"background-color: {bg_color};")
        times_frame.setGeometry(50, 80, 564, 900)
        times_frame.setAttribute(Qt.WA_TranslucentBackground, False)
        times_frame.setAutoFillBackground(True)
        times_frame.setStyleSheet(f"background-color: {bg_color};")  

        times_frame.setStyleSheet("background: transparent;")

        times_frame.setAutoFillBackground(False)
        times_frame.setStyleSheet("background: transparent; border: none;")

        #footer
        
        footer_label = QLabel("Created & Updated by Yusuf Darwish, IKworks team ©2025", central_widget)
        footer_label.setFont(QFont('Veranda', 12))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("background-color: #1a7689; color: white;")
        footer_label.setGeometry(
            times_frame.x() +17,
            times_frame.y() + times_frame.height() + 10,  # small margin
            times_frame.width(),
            30
        )
        footer_label.show()


        #create labels
        self.labels = Labels(times_frame, bg_color, text_color, font)

        grid = QGridLayout(times_frame)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setSpacing(5)
        grid.addWidget(self.labels.clock_label, 0, 0, 1, 3)
        grid.addWidget(self.labels.today_date_label, 1, 1, 1, 2)
        grid.addWidget(self.labels.today_space_label, 2, 0)
        grid.addWidget(self.labels.athan_label, 2, 1)
        grid.addWidget(self.labels.iqama_label, 2, 2)
        grid.addWidget(self.labels.today_fajr_label, 3, 0)
        grid.addWidget(self.labels.today_shurooq_label, 4, 0)
        grid.addWidget(self.labels.today_thuhr_label, 5, 0)
        grid.addWidget(self.labels.today_asr_label, 6, 0)
        grid.addWidget(self.labels.today_maghrib_label, 7, 0)
        grid.addWidget(self.labels.today_isha_label, 8, 0)
        
        grid.addWidget(self.labels.tomorrow_date_label, 11, 1, 1, 2)
        grid.addWidget(self.labels.tomorrow_fajr_label, 12, 0)
        grid.addWidget(self.labels.tomorrow_shurooq_label, 13, 0)
        grid.addWidget(self.labels.tomorrow_thuhr_label, 14, 0)
        grid.addWidget(self.labels.tomorrow_asr_label, 15, 0)
        grid.addWidget(self.labels.tomorrow_maghrib_label, 16, 0)
        grid.addWidget(self.labels.tomorrow_isha_label, 17, 0)
        
        grid.addWidget(self.labels.today_fajr_athan_label, 3, 1)
        grid.addWidget(self.labels.today_fajr_iqama_label, 3, 2)
        grid.addWidget(self.labels.today_shurooq_athan_label, 4, 1, 1, 2)
        grid.addWidget(self.labels.today_thuhr_athan_label, 5, 1)
        grid.addWidget(self.labels.today_thuhr_iqama_label, 5, 2)
        grid.addWidget(self.labels.today_asr_athan_label, 6, 1)
        grid.addWidget(self.labels.today_asr_iqama_label, 6, 2)
        grid.addWidget(self.labels.today_maghrib_athan_label, 7, 1)
        grid.addWidget(self.labels.today_maghrib_iqama_label, 7, 2)
        grid.addWidget(self.labels.today_isha_athan_label, 8, 1)
        grid.addWidget(self.labels.today_isha_iqama_label, 8, 2)
        
        grid.addWidget(self.labels.tomorrow_fajr_athan_label, 12, 1)
        grid.addWidget(self.labels.tomorrow_fajr_iqama_label, 12, 2)
        grid.addWidget(self.labels.tomorrow_shurooq_athan_label, 13, 1, 1, 2)
        grid.addWidget(self.labels.tomorrow_thuhr_athan_label, 14, 1)
        grid.addWidget(self.labels.tomorrow_thuhr_iqama_label, 14, 2)
        grid.addWidget(self.labels.tomorrow_asr_athan_label, 15, 1)
        grid.addWidget(self.labels.tomorrow_asr_iqama_label, 15, 2)
        grid.addWidget(self.labels.tomorrow_maghrib_athan_label, 16, 1)
        grid.addWidget(self.labels.tomorrow_maghrib_iqama_label, 16, 2)
        grid.addWidget(self.labels.tomorrow_isha_athan_label, 17, 1)
        grid.addWidget(self.labels.tomorrow_isha_iqama_label, 17, 2)

        #qr codes

        social_link = self.config["socials"]
        donate_link = self.config["donate"]
        website_link = self.config["website"]
        ikcode_link = self.config["ikworks"]

        trivia.make_qr_with_link(social_link, "socials.png")
        trivia.make_qr_with_link(donate_link, "donate.png")
        trivia.make_qr_with_link(website_link, "website.png")

        qr_size = int(0.1157407407 * height_value)

        social_label = QLabel(central_widget)
        socials_image = QPixmap('socials.png').scaled(qr_size, qr_size, Qt.KeepAspectRatio)
        social_label.setPixmap(socials_image)
        social_label.setGeometry(int(width_value * 0.3828125) - qr_size//2, 
                                  int(height_value * 0.2844907407) - qr_size//2, 
                                  qr_size, qr_size)
        
        donate_label = QLabel(central_widget)
        donate_pixmap = QPixmap('donate.png').scaled(qr_size, qr_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        donate_label.setPixmap(donate_pixmap)
        donate_label.setGeometry(int(width_value * 0.3828125) - qr_size//2, 
                                 int(height_value * 0.6273148148) - qr_size//2, 
                                 qr_size, qr_size)
        
        website_label = QLabel(central_widget)
        website_pixmap = QPixmap('website.png').scaled(qr_size, qr_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        website_label.setPixmap(website_pixmap)
        website_label.setGeometry(int(width_value * 0.3828125) - qr_size//2, 
                                  int(height_value * 0.8356481481) - qr_size//2, 
                                  qr_size, qr_size)

        #flyer

        flyer_height = height_value if not self.args.r else int(height_value/1.5)
        update_photos(flyer_height)

        self.flyer = QPushButton(central_widget)
        if photos:
            self.flyer.setIcon(QIcon(photos[0]))
            self.flyer.setIconSize(QSize(flyer_height, flyer_height))
        self.flyer.setFlat(True)
        self.flyer.setStyleSheet("border: none;")

        if self.args.t:
            global testDay
            testDay = 0
            self.flyer.clicked.connect(self.test_handler)
        else:
            self.flyer.clicked.connect(lambda: update_photos(flyer_height))
        
        flyer_x = width_value - height_value if not self.args.r else width_value - height_value + (height_value - int(height_value/1.5) - int(height_value * 0.0138888889))
        flyer_y = int(height_value * 0.0138888889) if self.args.r else 0
        self.flyer.setGeometry(flyer_x, flyer_y, flyer_height, flyer_height)

        #ramadan mode
        if self.args.r:
            font1 = QFont('Helvetica', round(24 * (height_value/1080)), QFont.Bold)
            font2 = QFont('Helvetica', round(16 * (height_value/1080)), QFont.Bold)
            font3 = QFont('Helvetica', round(14 * (height_value/1080)))
            
            day = trivia.get_trivia_day()
            
            winners_frame = QWidget(central_widget)
            winners_layout = QVBoxLayout(winners_frame)
            winners_frame.setStyleSheet(f"background-color: {bg_color};")
            
            questions_frame = QWidget(central_widget)
            questions_layout = QVBoxLayout(questions_frame)
            questions_frame.setStyleSheet(f"background-color: {bg_color};")
            
            self.ramadan_labels = RamadanLabels(winners_frame, questions_frame, bg_color, text_color, font1, font2, font3)
            
            # winners
            winners_layout.addWidget(self.ramadan_labels.winner_one_first)
            winners_layout.addWidget(self.ramadan_labels.winner_one_last)
            space1 = QLabel("")
            space1.setStyleSheet(f"background-color: {bg_color};")
            winners_layout.addWidget(space1)
            winners_layout.addWidget(self.ramadan_labels.winner_two_first)
            winners_layout.addWidget(self.ramadan_labels.winner_two_last)
            space2 = QLabel("")
            space2.setStyleSheet(f"background-color: {bg_color};")
            winners_layout.addWidget(space2)
            winners_layout.addWidget(self.ramadan_labels.winner_three_first)
            winners_layout.addWidget(self.ramadan_labels.winner_three_last)
            
            # questions
            questions_layout.addWidget(self.ramadan_labels.question_one)
            questions_layout.addWidget(self.ramadan_labels.question_one_options)
            space3 = QLabel("")
            space3.setStyleSheet(f"background-color: {bg_color};")
            questions_layout.addWidget(space3)
            questions_layout.addWidget(self.ramadan_labels.question_two)
            questions_layout.addWidget(self.ramadan_labels.question_two_options)
            space4 = QLabel("")
            space4.setStyleSheet(f"background-color: {bg_color};")
            questions_layout.addWidget(space4)
            questions_layout.addWidget(self.ramadan_labels.question_three)
            questions_layout.addWidget(self.ramadan_labels.question_three_options)
            
            # frames
            winners_frame.move(int(width_value * 0.5260416667) - winners_frame.width()//2, 
                              int(height_value * 0.279) - winners_frame.height()//2)
            questions_frame.move(int(width_value * 0.71875) - questions_frame.width()//2, 
                                int(height_value * 0.8425925926) - questions_frame.height()//2)
            
            # qr code
            self.ramadan_labels.trivia_qr.setParent(central_widget)
            self.ramadan_labels.trivia_qr.move(int(width_value * 0.4739583333), 
                                               int(height_value * 0.4592013889))
            
            update_trivia(day - 1, self.ramadan_labels, height_value, test=self.args.t)
        else:
            self.ramadan_labels = None
        
        self.showFullScreen()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: transparent;")

    
    def test_handler(self):
        """test mode handler"""
        global testDay
        testDay += 1
        screen = QApplication.primaryScreen().geometry()
        update_trivia(testDay, self.ramadan_labels, screen.height(), test=True)
    
    def keyPressEvent(self, event):
        """key press handler"""
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def display_time(self):
        """Main update loop"""
        global counter, i
        
        current_time = tm.strftime('%B %#d %#I:%M:%S %p')
        today = datetime.now().timetuple().tm_yday
        hour_time = tm.strftime('%H:%M')
        
        tomorrow = today + 1
        today_schedule = self.data.loc[self.data["Day_of_year"] == today]
        tomorrow_schedule = self.data.loc[self.data["Day_of_year"] == tomorrow]
        
        # Extract today's times
        Fajr_Athan = today_schedule.iloc[0]["Fajr_Athan"].strftime('%#I:%M')
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
        sunrise_time = today_schedule.iloc[0]["Shurooq_Sunrise"].strftime('%H:%M')
        thuhr_time = today_schedule.iloc[0]["Thuhr_Athan"].strftime('%H:%M')
        asr_time = today_schedule.iloc[0]["Asr_Athan"].strftime('%H:%M')
        maghrib_time = today_schedule.iloc[0]["Maghrib_Athan"].strftime('%H:%M')
        isha_time = today_schedule.iloc[0]["Ishaa_Athan"].strftime('%H:%M')
        
        # Extract tomorrow's times
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
        
        # Update labels
        self.labels.today_date_label.setText(today_schedule.iloc[0]["Day"])
        self.labels.tomorrow_date_label.setText(tomorrow_schedule.iloc[0]["Day"])
        self.labels.today_fajr_athan_label.setText(Fajr_Athan)
        self.labels.today_fajr_iqama_label.setText(Fajr_Iqama)
        self.labels.today_shurooq_athan_label.setText(Sunrise)
        self.labels.today_thuhr_athan_label.setText(Thuhr_Athan)
        self.labels.today_thuhr_iqama_label.setText(Thuhr_Iqama)
        self.labels.today_asr_athan_label.setText(Asr_Athan)
        self.labels.today_asr_iqama_label.setText(Asr_Iqama)
        self.labels.today_maghrib_athan_label.setText(Maghrib_Athan)
        self.labels.today_maghrib_iqama_label.setText(Maghrib_Iqama)
        self.labels.today_isha_athan_label.setText(Ishaa_Athan)
        self.labels.today_isha_iqama_label.setText(Ishaa_Iqama)
        
        self.labels.tomorrow_fajr_athan_label.setText(Fajr_Athan2)
        self.labels.tomorrow_fajr_iqama_label.setText(Fajr_Iqama2)
        self.labels.tomorrow_shurooq_athan_label.setText(Sunrise2)
        self.labels.tomorrow_thuhr_athan_label.setText(Thuhr_Athan2)
        self.labels.tomorrow_thuhr_iqama_label.setText(Thuhr_Iqama2)
        self.labels.tomorrow_asr_athan_label.setText(Asr_Athan2)
        self.labels.tomorrow_asr_iqama_label.setText(Asr_Iqama2)
        self.labels.tomorrow_maghrib_athan_label.setText(Maghrib_Athan2)
        self.labels.tomorrow_maghrib_iqama_label.setText(Maghrib_Iqama2)
        self.labels.tomorrow_isha_athan_label.setText(Ishaa_Athan2)
        self.labels.tomorrow_isha_iqama_label.setText(Ishaa_Iqama2)
        
        # Color highlighting
        next_prayer_color = rgb_to_hex((255, 0, 0))
        pre_prayer_color = rgb_to_hex((255, 255, 255)) if self.args.r else rgb_to_hex((0, 0, 0))
        current_prayer_color = rgb_to_hex((0, 200, 0)) if self.args.r else rgb_to_hex((0, 50, 0))
        
        # Update photo hourly
        if ":00" in hour_time:
            if not self.updated:
                screen = QApplication.primaryScreen().geometry()
                flyer_height = screen.height() if not self.args.r else int(screen.height()/1.5)
                update_photos(flyer_height)
                self.updated = True
        else:
            self.updated = False
        
        # Prayer time highlighting logic
        if hour_time < fajr_time:
            self.ramadan_updated = False
            self.set_prayer_colors(self.labels.today_isha_label, self.labels.today_isha_athan_label, 
                                  self.labels.today_isha_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.tomorrow_fajr_label, self.labels.tomorrow_fajr_athan_label, 
                                  self.labels.tomorrow_fajr_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, next_prayer_color)
        
        elif hour_time >= fajr_time and hour_time < sunrise_time:
            self.set_prayer_colors(self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  None, next_prayer_color)
        
        elif hour_time >= sunrise_time and hour_time < thuhr_time:
            self.set_prayer_colors(self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  None, current_prayer_color)
            self.set_prayer_colors(self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, next_prayer_color)
        
        elif hour_time >= thuhr_time and hour_time < asr_time:
            self.set_prayer_colors(self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  self.labels.today_shurooq_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, next_prayer_color)
        
        elif hour_time >= asr_time and hour_time < maghrib_time:
            self.set_prayer_colors(self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, next_prayer_color)
        
        elif hour_time >= maghrib_time and hour_time < isha_time:
            self.set_prayer_colors(self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_isha_label, self.labels.today_isha_athan_label, 
                                  self.labels.today_isha_iqama_label, next_prayer_color)
        
        elif hour_time >= isha_time:
            self.set_prayer_colors(self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, pre_prayer_color)
            self.set_prayer_colors(self.labels.today_isha_label, self.labels.today_isha_athan_label, 
                                  self.labels.today_isha_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.tomorrow_fajr_label, self.labels.tomorrow_fajr_athan_label, 
                                  self.labels.tomorrow_fajr_iqama_label, next_prayer_color)
            
            if self.args.r and not self.ramadan_updated and not self.args.t:
                screen = QApplication.primaryScreen().geometry()
                update_trivia(trivia.get_trivia_day(), self.ramadan_labels, screen.height())
                self.ramadan_updated = True
        
        self.labels.clock_label.setText(current_time)
        
        # Update flyer animation
        if i >= len(photos) - 1:
            i = 0
        
        if counter < Time and i < len(photos):
            counter += 1
        else:
            counter = 0
            i += 1
        
        if photos:
            icon = QIcon(photos[i if i < len(photos) else 0])
            self.flyer.setIcon(icon)
    
    def set_prayer_colors(self, label, athan_label, iqama_label, color):
        """set prayer label colors"""
        style = label.styleSheet()
        new_style = style.split(';')[0]+f': color: {color};'
        label.setStyleSheet(new_style)
        athan_label.setStyleSheet(athan_label.styleSheet().split(';')[0]+f': color: {color};')
        if iqama_label:
            iqama_label.setStyleSheet(iqama_label.styleSheet().split(';')[0] + f'; color: {color};')

def main():
    """run prayer screen"""
    parse = argparse.ArgumentParser(description="Prayer Times and Flyers")
    parse.add_argument("-r", action="store_true", help="turns on ramadan mode")
    parse.add_argument("-t", action="store_true", help="turns on test mode")
    args = parse.parse_args()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(BASE_DIR, '..', 'config.json')
    config_path = os.path.normpath(config_path)
    with open(config_path, "r") as file:
        config = json.load(file)

    # reading prayer schedule excel file (CFOF)
    prayer_schedule_path = config["prayer_schedule"]
    if not os.path.exists(prayer_schedule_path):
        prayer_schedule_path = os.path.dirname(os.path.abspath(__file__)) + '/../prayer_schedule.xlsx'
    data = pd.read_excel(prayer_schedule_path,sheet_name=0,header=0) # read prayer time excelsheet

    print(f"\nGetting prayer times from \"{os.path.abspath(prayer_schedule_path)}\"\n")

    app = QApplication(sys.argv)
    window = PrayerTimesWindow(args, config, data)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    

        

