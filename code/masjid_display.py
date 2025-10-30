"""
Created on Tue Apr  6 15:09:56 2021

@author: Mahdi Elghazali, Omar Nassar, and Yusuf Darwish
"""

import time as tm
from datetime import datetime
import pandas as pd
import os
import argparse
import trivia
import textwrap
import json
from stats import printAllStats
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                              QPushButton, QFrame, QVBoxLayout, QHBoxLayout, 
                              QGridLayout)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon

# declare and set the main directory for use in file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'config.json') 

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
    def __init__(self, parent, bg_color, text_color, font, is_ramadan=False):

        def make_label(parent, text="", bg_color=bg_color, text_color=text_color, font=font):
            label = QLabel(text, parent)
            # Force white text in ramadan mode
            final_color = "white" if is_ramadan else text_color
            label.setStyleSheet(f"background-color: transparent; color: {final_color}; border: none;")
            if font:
                label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            return label



        # Main clock and date labels
        self.clock_label = make_label(parent)
        # Force clock to be white in ramadan mode
        if is_ramadan:
            self.clock_label.setStyleSheet("background: transparent; color: white;")
        else:
            self.clock_label.setStyleSheet("background: transparent;")

        self.today_date_label = make_label(parent)
        self.today_space_label = make_label(parent, "")
        self.athan_label = make_label(parent, "Athan")
        self.iqama_label = make_label(parent, "Iqama")

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
        # self.tomorrow_shurooq_iqama_label = make_label(parent, "")
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
            self.winner_one_first.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_one_first.setFont(font1)
            self.winner_one_first.setAlignment(Qt.AlignCenter)

            self.winner_one_last = QLabel(winner_parent)
            self.winner_one_last.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_one_last.setFont(font1)
            self.winner_one_last.setAlignment(Qt.AlignCenter)
            
            self.winner_two_first = QLabel(winner_parent)
            self.winner_two_first.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_two_first.setFont(font1)
            self.winner_two_first.setAlignment(Qt.AlignCenter)
            
            self.winner_two_last = QLabel(winner_parent)
            self.winner_two_last.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_two_last.setFont(font1)
            self.winner_two_last.setAlignment(Qt.AlignCenter)

            self.winner_three_first = QLabel(winner_parent)
            self.winner_three_first.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_three_first.setFont(font1)
            self.winner_three_first.setAlignment(Qt.AlignCenter)
            
            self.winner_three_last = QLabel(winner_parent)
            self.winner_three_last.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.winner_three_last.setFont(font1)
            self.winner_three_last.setAlignment(Qt.AlignCenter)

            # question frame
            self.question_one = QLabel(question_parent)
            self.question_one.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_one.setFont(font2)
            self.question_one.setAlignment(Qt.AlignCenter)
            self.question_one.setWordWrap(True)
            
            self.question_one_options = QLabel(question_parent)
            self.question_one_options.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_one_options.setFont(font3)
            self.question_one_options.setAlignment(Qt.AlignCenter)
            self.question_one_options.setWordWrap(True)
            
            self.question_two = QLabel(question_parent)
            self.question_two.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_two.setFont(font2)
            self.question_two.setAlignment(Qt.AlignCenter)
            self.question_two.setWordWrap(True)
            
            self.question_two_options = QLabel(question_parent)
            self.question_two_options.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_two_options.setFont(font3)
            self.question_two_options.setAlignment(Qt.AlignCenter)
            self.question_two_options.setWordWrap(True)

            self.question_three = QLabel(question_parent)
            self.question_three.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_three.setFont(font2)
            self.question_three.setAlignment(Qt.AlignCenter)
            self.question_three.setWordWrap(True)
            
            self.question_three_options = QLabel(question_parent)
            self.question_three_options.setStyleSheet(f"background-color: {bg_color}; color: {text_color};")
            self.question_three_options.setFont(font3)
            self.question_three_options.setAlignment(Qt.AlignCenter)
            self.question_three_options.setWordWrap(True)

            # qr code
            self.trivia_qr = QLabel("")

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
        bg_label.setStyleSheet("background-color: black;")
        bg_label.setAlignment(Qt.AlignCenter)

        #colors, fonts
        text_color = "white" if self.args.r else "black"
        bg_color = rgb_to_hex((0, 25, 125)) if self.args.r else "white"
        font_size = round(30 * (height_value/1080))
        font = QFont('Helvetica', font_size, QFont.Bold)

        #prayer times frame
        
        times_frame = QFrame(central_widget)
        times_frame.setStyleSheet(f"background-color: {bg_color}; border: none;")
        times_frame.setAutoFillBackground(True)

        x_ratio = 0.0456
        y_ratio = 0.125
        w_ratio = 0.294
        h_ratio = 0.741

        left_shift_ratio = 0.01
        left_shift = int(width_value * left_shift_ratio)

        times_frame.setGeometry(
            int(width_value * x_ratio) - left_shift,
            int(height_value * y_ratio),
            int(width_value * w_ratio),
            int(height_value * h_ratio)
        )
        times_frame.show()

        print("")

        

        #create labels
        self.labels = Labels(times_frame, bg_color, text_color, font, is_ramadan=self.args.r)

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


        trivia.make_qr_with_link(social_link, "socials.png")
        trivia.make_qr_with_link(donate_link, "donate.png")
        trivia.make_qr_with_link(website_link, "website.png")

        qr_size = int(0.1157407407 * height_value)

        social_label = QLabel(central_widget)
        socials_image = QPixmap('socials.png').scaled(qr_size, qr_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        self.flyer.setStyleSheet("border: none; background: transparent;")

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
            
            # Winners frame with fixed size and position
            winners_frame = QFrame(central_widget)
            winners_layout = QVBoxLayout(winners_frame)
            winners_layout.setContentsMargins(10, 10, 10, 10)
            winners_layout.setSpacing(5)
            winners_frame.setStyleSheet(f"background-color: {bg_color}; border: none;")
            winners_frame.setAutoFillBackground(True)
            
            # Questions frame with fixed size and position
            questions_frame = QFrame(central_widget)
            questions_layout = QVBoxLayout(questions_frame)
            questions_layout.setContentsMargins(15, 15, 15, 15)
            questions_layout.setSpacing(5)
            questions_frame.setStyleSheet(f"background-color: {bg_color}; border: none;")
            questions_frame.setAutoFillBackground(True)
            
            # No frame needed, QR code will be positioned directly
            
            self.ramadan_labels = RamadanLabels(winners_frame, questions_frame, bg_color, text_color, font1, font2, font3)
            
            # winners layout
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
            winners_layout.addStretch()
            
            # questions layout
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
            questions_layout.addStretch()
            
            winners_w_ratio = 0.15
            winners_h_ratio = 0.25
            winners_x_ratio = 0.446
            winners_y_ratio = 0.134
            
            winners_frame.setGeometry(
                int(width_value * winners_x_ratio),
                int(height_value * winners_y_ratio),
                int(width_value * winners_w_ratio),
                int(height_value * winners_h_ratio)
            )
            
            questions_w_ratio = 0.28
            questions_h_ratio = 0.20
            questions_x_ratio = 0.555
            questions_y_ratio = 0.75
            
            questions_frame.setGeometry(
                int(width_value * questions_x_ratio),
                int(height_value * questions_y_ratio),
                int(width_value * questions_w_ratio),
                int(height_value * questions_h_ratio)
            )
            
                        
            winners_frame.show()
            questions_frame.show()
            
            update_trivia(day - 1, self.ramadan_labels, height_value, test=self.args.t)
            
            # Position QR code directly without frame - CENTERED ON SCREEN
            qr_size = int(height_value * 0.1851851852)
            pixmap = QPixmap('trivia.png')
            pixmap = pixmap.scaled(qr_size, qr_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.ramadan_labels.trivia_qr.setParent(central_widget)
            self.ramadan_labels.trivia_qr.setPixmap(pixmap)
            self.ramadan_labels.trivia_qr.setStyleSheet("background: transparent; border: none;")
            self.ramadan_labels.trivia_qr.setGeometry(
                int(width_value / 2 - qr_size / 2)+50,  # Center horizontally
                int(height_value / 2 - qr_size / 2)+54,  # Center vertically
                qr_size,
                qr_size
            )
            self.ramadan_labels.trivia_qr.show()
            
        else:
            self.ramadan_labels = None
        
        self.showFullScreen()

    
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
        
        # Reset all colors to default first
        all_prayer_labels = [
            (self.labels.today_fajr_label, self.labels.today_fajr_athan_label, self.labels.today_fajr_iqama_label),
            (self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, self.labels.today_shurooq_iqama_label),
            (self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, self.labels.today_thuhr_iqama_label),
            (self.labels.today_asr_label, self.labels.today_asr_athan_label, self.labels.today_asr_iqama_label),
            (self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, self.labels.today_maghrib_iqama_label),
            (self.labels.today_isha_label, self.labels.today_isha_athan_label, self.labels.today_isha_iqama_label),
            (self.labels.tomorrow_fajr_label, self.labels.tomorrow_fajr_athan_label, self.labels.tomorrow_fajr_iqama_label),
        ]
        
        for prayer_name, athan, iqama in all_prayer_labels:
            self.set_prayer_colors(prayer_name, athan, iqama, pre_prayer_color)
        
        # Update photo hourly
        if ":00" in hour_time:
            if not self.updated:
                screen = QApplication.primaryScreen().geometry()
                flyer_height = screen.height() if not self.args.r else int(screen.height()/1.5)
                update_photos(flyer_height)
                self.updated = True
        else:
            self.updated = False
        
        # Prayer time highlighting logic - now colors entire row
        if hour_time < fajr_time:
            self.ramadan_updated = False
            self.set_prayer_colors(self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, next_prayer_color)
        
        elif hour_time >= fajr_time and hour_time < sunrise_time:
            self.set_prayer_colors(self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  self.labels.today_shurooq_iqama_label, next_prayer_color)
        
        elif hour_time >= sunrise_time and hour_time < thuhr_time:
            self.set_prayer_colors(self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  self.labels.today_shurooq_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, next_prayer_color)
        
        elif hour_time >= thuhr_time and hour_time < asr_time:
            self.set_prayer_colors(self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, next_prayer_color)
        
        elif hour_time >= asr_time and hour_time < maghrib_time:
            self.set_prayer_colors(self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, next_prayer_color)
        
        elif hour_time >= maghrib_time and hour_time < isha_time:
            self.set_prayer_colors(self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, current_prayer_color)
            self.set_prayer_colors(self.labels.today_isha_label, self.labels.today_isha_athan_label, 
                                  self.labels.today_isha_iqama_label, next_prayer_color)
        
        elif hour_time >= isha_time:
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
        """set prayer label colors for entire row"""
        label.setStyleSheet(f"background-color: transparent; color: {color}; border: none;")
        athan_label.setStyleSheet(f"background-color: transparent; color: {color}; border: none;")
        if iqama_label:
            iqama_label.setStyleSheet(f"background-color: transparent; color: {color}; border: none;")


def rgb_to_hex(rgb):
      """convert rgb to hex"""
      r, g, b = rgb
      return f'#{r:02x}{g:02x}{b:02x}'

def update_photos(height_value):
    """Update flyer photos label"""
    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)
    
    main_folder = config["flyers"]
    if not os.path.exists(main_folder):
         main_folder = os.path.abspath(os.path.join(BASE_DIR, "..", "sample ads"))
    
    photo_path = os.listdir(main_folder) # array to store the path of the photos 
    photo_list = [] # array to store the list of the photos 
    photos.clear()

    print("\n[", end="")

    # assigning the whole path to the photo list
    for file in photo_path:
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            new_file = os.path.join(main_folder, file)
            photo_list.append(new_file)
            print(f"'{file}'", end=", " if file != photo_path[-1] else "")
        else:
            photo_path.remove(file)
    print("]")

    # reading and loading the photos with high quality scaling
    for file in photo_list:
        load = QPixmap(file)
        load1 = load.scaled(height_value, height_value, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        photos.append(load1)

    print(f"Photos updated from \"{os.path.abspath(main_folder)}\" at {tm.strftime('%#m/%#d/%Y %#I:%M:%S %p')} \n")


def update_trivia(day, ramadan_labels, height_value, test=False):
    """Updating trivia questions and winners as well as logging, sending emails, and generating QR code"""
    print(f"Day {day} of Ramadan")

    if (day < 0 or day > 30):
        winners = None
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
    current_time = tm.strftime('%B %#d %#I:%M %p') # calculate current time
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

def main():
    """run prayer screen"""
    parse = argparse.ArgumentParser(description="Prayer Times and Flyers")
    parse.add_argument("-r", action="store_true", help="turns on ramadan mode")
    parse.add_argument("-t", action="store_true", help="turns on test mode")
    args = parse.parse_args()

    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)

    # reading prayer schedule excel file
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