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
                              QGridLayout, QSizePolicy)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon, QFontDatabase, QFontMetrics

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
    def __init__(self, parent, bg_color, text_color, font, font2, is_ramadan=False):

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
        self.today_fajr_athan_label = make_label(parent,font=font2)
        self.today_fajr_iqama_label = make_label(parent,font=font2)
        self.today_shurooq_athan_label = make_label(parent,font=font2)
        self.today_shurooq_iqama_label = make_label(parent, "",font=font2)
        self.today_thuhr_athan_label = make_label(parent,font=font2)
        self.today_thuhr_iqama_label = make_label(parent,font=font2)
        self.today_asr_athan_label = make_label(parent,font=font2)
        self.today_asr_iqama_label = make_label(parent,font=font2)
        self.today_maghrib_athan_label = make_label(parent,font=font2)
        self.today_maghrib_iqama_label = make_label(parent,font=font2)
        self.today_isha_athan_label = make_label(parent,font=font2)
        self.today_isha_iqama_label = make_label(parent,font=font2)

        # Tomorrow's Athan/Iqama times
        self.tomorrow_fajr_athan_label = make_label(parent,font=font2)
        self.tomorrow_fajr_iqama_label = make_label(parent,font=font2)
        self.tomorrow_shurooq_athan_label = make_label(parent,font=font2)
        # self.tomorrow_shurooq_iqama_label = make_label(parent, "",font=font2)
        self.tomorrow_thuhr_athan_label = make_label(parent,font=font2)
        self.tomorrow_thuhr_iqama_label = make_label(parent,font=font2)
        self.tomorrow_asr_athan_label = make_label(parent,font=font2)
        self.tomorrow_asr_iqama_label = make_label(parent,font=font2)
        self.tomorrow_maghrib_athan_label = make_label(parent,font=font2)
        self.tomorrow_maghrib_iqama_label = make_label(parent,font=font2)
        self.tomorrow_isha_athan_label = make_label(parent,font=font2)
        self.tomorrow_isha_iqama_label = make_label(parent,font=font2)


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

        font0=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica.ttf")
        font1=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica-Bold.ttf")
        font2=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica-BoldOblique.ttf")
        font3=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica-Compressed.otf")
        font4=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica-Light.ttf")
        font5=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica-Oblique.ttf")
        font6=QFontDatabase.addApplicationFont("../resources/fonts/Helvetica-Rounded-Bold.otf")

        HELVETICA = QFontDatabase.applicationFontFamilies(font0)[0]
        HELVETICA_BOLD = QFontDatabase.applicationFontFamilies(font1)[0]
        HELVETICA_BOLD_OBLIQUE = QFontDatabase.applicationFontFamilies(font2)[0]
        HELVETICA_COMPRESSED = QFontDatabase.applicationFontFamilies(font3)[0]
        HELVETICA_LIGHT = QFontDatabase.applicationFontFamilies(font4)[0]
        HELVETICA_OBLIQUE = QFontDatabase.applicationFontFamilies(font5)[0]
        HELVETICA_ROUNDED_BOLD = QFontDatabase.applicationFontFamilies(font6)[0]

        #colors, fonts - ICCH Theme
        if self.args.r:
            # Ramadan mode - C theme
            self.dark_green = rgb_to_hex((22, 0, 150))  # Dark blue for Ramadan
            self.tan = rgb_to_hex((100, 149, 237))  # Cornflower blue for Ramadan headers
            self.gold = rgb_to_hex((255, 255, 255))  # White for clock outline in Ramadan
            self.dark_gray = rgb_to_hex((25, 25, 112))  # Midnight blue for clock background in Ramadan
        else:
            # Normal mode - Clean white/light gray theme
            self.dark_green = rgb_to_hex((245, 245, 245))  # Very light gray background
            self.tan = rgb_to_hex((220, 220, 220))  # Light gray for section headers
            self.gold = rgb_to_hex((180, 180, 180))  # Medium gray for clock outline
            self.dark_gray = rgb_to_hex((255, 255, 255))  # White for clock background
        
        self.light_green = rgb_to_hex((144, 238, 144))  # Light green for current prayer
        self.light_red = rgb_to_hex((255, 100, 100))  # Light red for next prayer
        
        text_color = "white" if self.args.r else "black"  # White text for Ramadan, black for normal
        bg_color = self.dark_green  # Use theme-appropriate background
        section_bg = self.tan  # Theme-appropriate section headers
        font_size = round(20 * (height_value/1080))  # Scaled down from 30
        font = QFont(HELVETICA_BOLD, font_size, QFont.Bold)
        header_font = QFont(HELVETICA_BOLD, round(font_size * 1.1), QFont.Bold)  # Slightly larger for headers
        clock_font = QFont(HELVETICA_BOLD, round(font_size * 1.15), QFont.Bold)  # Larger for clock

        #prayer times frame

        print("")
        print("")
        
        times_frame = QFrame(central_widget)
        border_color = self.tan if self.args.r else rgb_to_hex((200, 200, 200))  # Light gray border for normal mode
        times_frame.setStyleSheet(f"background-color: {bg_color}; border: 3px solid {border_color};")
        times_frame.setAutoFillBackground(True)

        x_ratio = 0.0325
        y_ratio = 0.05
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

        font_file = "quran_font.ttf"
        font_path = os.path.join(BASE_DIR, "..", "resources", "fonts", font_file)

        # Load the font
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id == -1:
            print(f"❌ Failed to load font at {font_path}")
        else:
            loaded_fonts = QFontDatabase.applicationFontFamilies(font_id)
            if loaded_fonts:
                font_family = loaded_fonts[0]
                print(f"✅ Loaded font family: {font_family}")

        ayah_frame = QFrame(central_widget)
        ayah_frame.setStyleSheet(f"background-color: transparent; border: none;")
        ayah_frame.setAutoFillBackground(True)
        ayah_frame.setAttribute(Qt.WA_TranslucentBackground, True)
        
        ayah_x = int(width_value * x_ratio) - left_shift
        ayah_y = int(height_value * y_ratio) + int(height_value * h_ratio) + 47
        ayah_w = int(width_value * w_ratio)
        ayah_h = int(height_value * 0.17)  
        
        ayah_frame.setGeometry(ayah_x, ayah_y, ayah_w, ayah_h)
        ayah_frame.show()
        
        #get todays ayah
        daily_ayah = self.get_daily_ayah()
        
        #create ayah labels
        ayah_layout = QVBoxLayout(ayah_frame)
        ayah_layout.setContentsMargins(15, 15, 15, 15)
        ayah_layout.setSpacing(10)
        
        #ayah (arabic)
        arabic_font_size = round(20 * (height_value / 1080))

        arabic_font = QFont(font_family, arabic_font_size)
        #arabic_font.setBold(True)

        self.ayah_arabic = QLabel(daily_ayah['arabic'], ayah_frame)
        self.ayah_arabic.setStyleSheet(f"background-color: transparent; color: white; border: none;")
        self.ayah_arabic.setFont(arabic_font)
        self.ayah_arabic.setAlignment(Qt.AlignCenter)
        self.ayah_arabic.setWordWrap(True)

        
        #translation
        translation_font = QFont(HELVETICA, round(13 * (height_value/1080)))
        self.ayah_translation = QLabel(daily_ayah['translation'], ayah_frame)
        self.ayah_translation.setStyleSheet(f"background-color: transparent; color: white; border: none;")
        self.ayah_translation.setFont(translation_font)
        self.ayah_translation.setAlignment(Qt.AlignCenter)
        self.ayah_translation.setWordWrap(True)
        
        #reference
        reference_font = QFont(HELVETICA_OBLIQUE, round(12 * (height_value/1080)), QFont.StyleItalic)
        self.ayah_reference = QLabel(daily_ayah['reference'], ayah_frame)
        self.ayah_reference.setStyleSheet(f"background-color: transparent; color: white; border: none;")
        self.ayah_reference.setFont(reference_font)
        self.ayah_reference.setAlignment(Qt.AlignCenter)
        
        ayah_layout.addWidget(self.ayah_arabic)
        ayah_layout.addWidget(self.ayah_translation)
        ayah_layout.addWidget(self.ayah_reference)
        ayah_layout.addStretch()
        
        #store ayah 
        self.current_ayah_day = datetime.now().timetuple().tm_yday

        #create labels
        self.labels = Labels(times_frame, bg_color, text_color, font, header_font, is_ramadan=self.args.r)
        
        # Set clock font to stand out with gold/gray outline and background
        self.labels.clock_label.setFont(clock_font)
        clock_text_color = "white" if self.args.r else "black"
        # Padding to prevent text clipping at borders (more bottom padding for descenders)
        padding_px = 3
        border_px = 1
        self.labels.clock_label.setStyleSheet(f"background-color: {self.dark_gray}; color: {clock_text_color}; border: {border_px}px solid {self.gold}; padding: {padding_px}px {padding_px}px {padding_px + 3}px {padding_px}px; border-radius: 5px; line-height: 1.3;")

        # Center alignment to make best use of available space
        self.labels.clock_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.labels.clock_label.setWordWrap(False)
        
        # Allow natural sizing without forced heights
        self.labels.clock_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        grid = QGridLayout(times_frame)
        grid.setContentsMargins(15, 15, 15, 15)
        grid.setSpacing(3)  # Minimal spacing between rows
        grid.setVerticalSpacing(5)
        
        # Create section headers with theme-appropriate colors
        today_header = QLabel("TODAY", times_frame)
        header_text_color = "white" if self.args.r else "black"
        today_header.setStyleSheet(f"background-color: {section_bg}; color: {header_text_color}; border: none; padding: 5px; border-radius: 3px;")
        today_header.setFont(header_font)
        today_header.setAlignment(Qt.AlignCenter)
        
        tomorrow_header = QLabel("TOMORROW", times_frame)
        tomorrow_header.setStyleSheet(f"background-color: {section_bg}; color: {header_text_color}; border: none; padding: 5px; border-radius: 3px;")
        tomorrow_header.setFont(header_font)
        tomorrow_header.setAlignment(Qt.AlignCenter)
        
        # Set date labels to use theme-appropriate colors
        date_text_color = "white" if self.args.r else "black"
        self.labels.today_date_label.setStyleSheet(f"background-color: transparent; color: {date_text_color}; border: none;")
        self.labels.today_date_label.setFont(font)
        self.labels.today_date_label.setAlignment(Qt.AlignCenter)
        
        self.labels.tomorrow_date_label.setStyleSheet(f"background-color: transparent; color: {date_text_color}; border: none;")
        self.labels.tomorrow_date_label.setFont(font)
        self.labels.tomorrow_date_label.setAlignment(Qt.AlignCenter)
        
        # Create frames for each prayer row to give them visible borders
        self.today_fajr_frame = QFrame(times_frame)
        self.today_shurooq_frame = QFrame(times_frame)
        self.today_thuhr_frame = QFrame(times_frame)
        self.today_asr_frame = QFrame(times_frame)
        self.today_maghrib_frame = QFrame(times_frame)
        self.today_isha_frame = QFrame(times_frame)
        self.tomorrow_fajr_frame = QFrame(times_frame)
        
        # Style all frames with borders
        frame_border_color = self.tan if self.args.r else rgb_to_hex((200, 200, 200))
        frame_style = f"background-color: rgba(255, 255, 255, 0.05); border: 1px solid {frame_border_color}; border-radius: 3px;"
        for frame in [self.today_fajr_frame, self.today_shurooq_frame, self.today_thuhr_frame, 
                      self.today_asr_frame, self.today_maghrib_frame, self.today_isha_frame, 
                      self.tomorrow_fajr_frame]:
            frame.setStyleSheet(frame_style)
            frame_layout = QHBoxLayout(frame)
            frame_layout.setContentsMargins(5, 3, 5, 3)
            frame_layout.setSpacing(10)
        
        # Add widgets to frames
        self.today_fajr_frame.layout().addWidget(self.labels.today_fajr_label)
        self.today_fajr_frame.layout().addWidget(self.labels.today_fajr_athan_label)
        self.today_fajr_frame.layout().addWidget(self.labels.today_fajr_iqama_label)
        
        # For Shurooq, set fixed widths to match other rows
        shurooq_layout = self.today_shurooq_frame.layout()
        shurooq_layout.addWidget(self.labels.today_shurooq_label)
        shurooq_layout.addWidget(self.labels.today_shurooq_athan_label)
        # Add empty space placeholder for iqama column to maintain alignment
        empty_iqama = QLabel("", self.today_shurooq_frame)
        empty_iqama.setStyleSheet("background-color: transparent; border: none;")
        shurooq_layout.addWidget(empty_iqama)
        
        self.today_thuhr_frame.layout().addWidget(self.labels.today_thuhr_label)
        self.today_thuhr_frame.layout().addWidget(self.labels.today_thuhr_athan_label)
        self.today_thuhr_frame.layout().addWidget(self.labels.today_thuhr_iqama_label)
        
        self.today_asr_frame.layout().addWidget(self.labels.today_asr_label)
        self.today_asr_frame.layout().addWidget(self.labels.today_asr_athan_label)
        self.today_asr_frame.layout().addWidget(self.labels.today_asr_iqama_label)
        
        self.today_maghrib_frame.layout().addWidget(self.labels.today_maghrib_label)
        self.today_maghrib_frame.layout().addWidget(self.labels.today_maghrib_athan_label)
        self.today_maghrib_frame.layout().addWidget(self.labels.today_maghrib_iqama_label)
        
        self.today_isha_frame.layout().addWidget(self.labels.today_isha_label)
        self.today_isha_frame.layout().addWidget(self.labels.today_isha_athan_label)
        self.today_isha_frame.layout().addWidget(self.labels.today_isha_iqama_label)
        
        self.tomorrow_fajr_frame.layout().addWidget(self.labels.tomorrow_fajr_label)
        self.tomorrow_fajr_frame.layout().addWidget(self.labels.tomorrow_fajr_athan_label)
        self.tomorrow_fajr_frame.layout().addWidget(self.labels.tomorrow_fajr_iqama_label)
        
        # Create header row frame
        header_frame = QFrame(times_frame)
        header_frame.setStyleSheet(f"background-color: {self.tan}; border-radius: 3px;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(5, 3, 5, 3)
        header_layout.setSpacing(10)
        header_layout.addWidget(self.labels.today_space_label)
        header_layout.addWidget(self.labels.athan_label)
        header_layout.addWidget(self.labels.iqama_label)
        
        # Style header labels with theme-appropriate colors
        header_label_color = "white" if self.args.r else "black"
        self.labels.today_space_label.setStyleSheet(f"background-color: transparent; color: {header_label_color}; border: none;")
        self.labels.athan_label.setStyleSheet(f"background-color: transparent; color: {header_label_color}; border: none;")
        self.labels.iqama_label.setStyleSheet(f"background-color: transparent; color: {header_label_color}; border: none;")
        
        # Clock at top
        grid.addWidget(self.labels.clock_label, 0, 0, 1, 1)
        
        # TODAY SECTION
        grid.addWidget(today_header, 1, 0, 1, 1)
        grid.addWidget(self.labels.today_date_label, 2, 0, 1, 1)
        
        # Column headers for today
        grid.addWidget(header_frame, 3, 0, 1, 1)
        
        # Today's prayers - each in its own framed row
        grid.addWidget(self.today_fajr_frame, 4, 0)
        grid.addWidget(self.today_shurooq_frame, 5, 0)
        grid.addWidget(self.today_thuhr_frame, 6, 0)
        grid.addWidget(self.today_asr_frame, 7, 0)
        grid.addWidget(self.today_maghrib_frame, 8, 0)
        grid.addWidget(self.today_isha_frame, 9, 0)
        
        # TOMORROW SECTION
        grid.addWidget(tomorrow_header, 11, 0, 1, 1)
        grid.addWidget(self.labels.tomorrow_date_label, 12, 0, 1, 1)
        
        # Tomorrow's prayers
        grid.addWidget(self.tomorrow_fajr_frame, 13, 0)
        
        # Add tomorrow's other prayers to grid with proper alignment
        tomorrow_shurooq_frame = QFrame(times_frame)
        tomorrow_shurooq_frame.setStyleSheet(frame_style)
        layout_sh = QHBoxLayout(tomorrow_shurooq_frame)
        layout_sh.setContentsMargins(5, 3, 5, 3)
        layout_sh.setSpacing(10)
        layout_sh.addWidget(self.labels.tomorrow_shurooq_label)
        layout_sh.addWidget(self.labels.tomorrow_shurooq_athan_label)
        # Add empty space placeholder for iqama column to maintain alignment
        empty_iqama_tom = QLabel("", tomorrow_shurooq_frame)
        empty_iqama_tom.setStyleSheet("background-color: transparent; border: none;")
        layout_sh.addWidget(empty_iqama_tom)
        grid.addWidget(tomorrow_shurooq_frame, 14, 0)
        
        tomorrow_thuhr_frame = QFrame(times_frame)
        tomorrow_thuhr_frame.setStyleSheet(frame_style)
        layout_th = QHBoxLayout(tomorrow_thuhr_frame)
        layout_th.setContentsMargins(5, 3, 5, 3)
        layout_th.setSpacing(10)
        layout_th.addWidget(self.labels.tomorrow_thuhr_label)
        layout_th.addWidget(self.labels.tomorrow_thuhr_athan_label)
        layout_th.addWidget(self.labels.tomorrow_thuhr_iqama_label)
        grid.addWidget(tomorrow_thuhr_frame, 15, 0)
        
        tomorrow_asr_frame = QFrame(times_frame)
        tomorrow_asr_frame.setStyleSheet(frame_style)
        layout_as = QHBoxLayout(tomorrow_asr_frame)
        layout_as.setContentsMargins(5, 3, 5, 3)
        layout_as.setSpacing(10)
        layout_as.addWidget(self.labels.tomorrow_asr_label)
        layout_as.addWidget(self.labels.tomorrow_asr_athan_label)
        layout_as.addWidget(self.labels.tomorrow_asr_iqama_label)
        grid.addWidget(tomorrow_asr_frame, 16, 0)
        
        tomorrow_maghrib_frame = QFrame(times_frame)
        tomorrow_maghrib_frame.setStyleSheet(frame_style)
        layout_ma = QHBoxLayout(tomorrow_maghrib_frame)
        layout_ma.setContentsMargins(5, 3, 5, 3)
        layout_ma.setSpacing(10)
        layout_ma.addWidget(self.labels.tomorrow_maghrib_label)
        layout_ma.addWidget(self.labels.tomorrow_maghrib_athan_label)
        layout_ma.addWidget(self.labels.tomorrow_maghrib_iqama_label)
        grid.addWidget(tomorrow_maghrib_frame, 17, 0)
        
        tomorrow_isha_frame = QFrame(times_frame)
        tomorrow_isha_frame.setStyleSheet(frame_style)
        layout_is = QHBoxLayout(tomorrow_isha_frame)
        layout_is.setContentsMargins(5, 3, 5, 3)
        layout_is.setSpacing(10)
        layout_is.addWidget(self.labels.tomorrow_isha_label)
        layout_is.addWidget(self.labels.tomorrow_isha_athan_label)
        layout_is.addWidget(self.labels.tomorrow_isha_iqama_label)
        grid.addWidget(tomorrow_isha_frame, 18, 0)
        
        # Store frames for color updates
        self.tomorrow_shurooq_frame = tomorrow_shurooq_frame
        self.tomorrow_thuhr_frame = tomorrow_thuhr_frame
        self.tomorrow_asr_frame = tomorrow_asr_frame
        self.tomorrow_maghrib_frame = tomorrow_maghrib_frame
        self.tomorrow_isha_frame = tomorrow_isha_frame
        
        # Store grid for column highlighting
        self.prayer_grid = grid

        #qr codes

        social_link = self.config["socials"]
        donate_link = self.config["donate"]
        website_link = self.config["website"]


        trivia.make_qr_with_link(social_link, "socials.png")
        trivia.make_qr_with_link(donate_link, "donate.png")
        trivia.make_qr_with_link(website_link, "website.png")

        # --- Social QR ---
        social_x_ratio = 0.3475
        social_y_ratio = 0.200
        social_w_ratio = 0.1157
        social_h_ratio = 0.1157

        social_label = QLabel(central_widget)
        social_pixmap = QPixmap('socials.png').scaled(int(width_value * social_w_ratio),
                                                    int(height_value * social_h_ratio),
                                                    Qt.KeepAspectRatio,
                                                    Qt.SmoothTransformation)
        social_label.setPixmap(social_pixmap)
        social_label.setGeometry(int(width_value * social_x_ratio),
                                int(height_value * social_y_ratio),
                                social_pixmap.width(),
                                social_pixmap.height())

        # --- Donate QR ---
        donate_x_ratio = 0.3480
        donate_y_ratio = 0.525
        donate_w_ratio = 0.1157
        donate_h_ratio = 0.1157

        donate_label = QLabel(central_widget)
        donate_pixmap = QPixmap('donate.png').scaled(int(width_value * donate_w_ratio),
                                                    int(height_value * donate_h_ratio),
                                                    Qt.KeepAspectRatio,
                                                    Qt.SmoothTransformation)
        donate_label.setPixmap(donate_pixmap)
        donate_label.setGeometry(int(width_value * donate_x_ratio),
                                int(height_value * donate_y_ratio),
                                donate_pixmap.width(),
                                donate_pixmap.height())

        # --- Website QR ---
        website_x_ratio = 0.3470
        website_y_ratio = 0.725
        website_w_ratio = 0.1157
        website_h_ratio = 0.1157

        website_label = QLabel(central_widget)
        website_pixmap = QPixmap('website.png').scaled(int(width_value * website_w_ratio),
                                                    int(height_value * website_h_ratio),
                                                    Qt.KeepAspectRatio,
                                                    Qt.SmoothTransformation)
        website_label.setPixmap(website_pixmap)
        website_label.setGeometry(int(width_value * website_x_ratio),
                                int(height_value * website_y_ratio),
                                website_pixmap.width(),
                                website_pixmap.height())


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
            font1 = QFont(HELVETICA_BOLD, round(24 * (height_value/1080)), QFont.Bold)
            font2 = QFont(HELVETICA_BOLD, round(16 * (height_value/1080)), QFont.Bold)
            font3 = QFont(HELVETICA, round(14 * (height_value/1080)))
            
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
            winners_x_ratio = 0.451
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
                int(height_value / 2 - qr_size / 2)+42,  # Center vertically
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

         # Update ayah daily
        current_day = datetime.now().timetuple().tm_yday
        if current_day != self.current_ayah_day:
            daily_ayah = self.get_daily_ayah()
            self.ayah_arabic.setText(daily_ayah['arabic'])
            self.ayah_translation.setText(daily_ayah['translation'])
            self.ayah_reference.setText(daily_ayah['reference'])
            self.current_ayah_day = current_day
            print(f"Ayah updated for day {current_day}")
        
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
        
        # Color highlighting - now highlights entire row with background color
        pre_prayer_color = "white" if self.args.r else "black"  # Theme-appropriate text for non-active prayers
        current_prayer_text = "black"  # Black text on light green background for better visibility
        next_prayer_text = "black"  # Black text on light red background for better visibility
        
        # Reset all row frame backgrounds to default first
        frame_border_color = self.tan if self.args.r else rgb_to_hex((200, 200, 200))
        default_frame_style = f"background-color: rgba(255, 255, 255, 0.05); border: 1px solid {frame_border_color}; border-radius: 3px;"
        
        all_prayer_frames = [
            (self.today_fajr_frame, self.labels.today_fajr_label, self.labels.today_fajr_athan_label, self.labels.today_fajr_iqama_label),
            (self.today_shurooq_frame, self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, self.labels.today_shurooq_iqama_label),
            (self.today_thuhr_frame, self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, self.labels.today_thuhr_iqama_label),
            (self.today_asr_frame, self.labels.today_asr_label, self.labels.today_asr_athan_label, self.labels.today_asr_iqama_label),
            (self.today_maghrib_frame, self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, self.labels.today_maghrib_iqama_label),
            (self.today_isha_frame, self.labels.today_isha_label, self.labels.today_isha_athan_label, self.labels.today_isha_iqama_label),
            (self.tomorrow_fajr_frame, self.labels.tomorrow_fajr_label, self.labels.tomorrow_fajr_athan_label, self.labels.tomorrow_fajr_iqama_label),
        ]
        
        for frame, prayer_name, athan, iqama in all_prayer_frames:
            frame.setStyleSheet(default_frame_style)
            self.set_prayer_label_colors(prayer_name, athan, iqama, pre_prayer_color)
        
        # Update photo hourly
        if ":00" in hour_time:
            if not self.updated:
                screen = QApplication.primaryScreen().geometry()
                flyer_height = screen.height() if not self.args.r else int(screen.height()/1.5)
                update_photos(flyer_height)
                self.updated = True
        else:
            self.updated = False
        
        # Prayer time highlighting logic - now colors entire row frame background
        if hour_time < fajr_time:
            self.ramadan_updated = False
            self.set_prayer_frame_colors(self.today_fajr_frame, self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, self.light_red, next_prayer_text)
        
        elif hour_time >= fajr_time and hour_time < sunrise_time:
            self.set_prayer_frame_colors(self.today_fajr_frame, self.labels.today_fajr_label, self.labels.today_fajr_athan_label, 
                                  self.labels.today_fajr_iqama_label, self.light_green, current_prayer_text)
            self.set_prayer_frame_colors(self.today_shurooq_frame, self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  self.labels.today_shurooq_iqama_label, self.light_red, next_prayer_text)
        
        elif hour_time >= sunrise_time and hour_time < thuhr_time:
            self.set_prayer_frame_colors(self.today_shurooq_frame, self.labels.today_shurooq_label, self.labels.today_shurooq_athan_label, 
                                  self.labels.today_shurooq_iqama_label, self.light_green, current_prayer_text)
            self.set_prayer_frame_colors(self.today_thuhr_frame, self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, self.light_red, next_prayer_text)
        
        elif hour_time >= thuhr_time and hour_time < asr_time:
            self.set_prayer_frame_colors(self.today_thuhr_frame, self.labels.today_thuhr_label, self.labels.today_thuhr_athan_label, 
                                  self.labels.today_thuhr_iqama_label, self.light_green, current_prayer_text)
            self.set_prayer_frame_colors(self.today_asr_frame, self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, self.light_red, next_prayer_text)
        
        elif hour_time >= asr_time and hour_time < maghrib_time:
            self.set_prayer_frame_colors(self.today_asr_frame, self.labels.today_asr_label, self.labels.today_asr_athan_label, 
                                  self.labels.today_asr_iqama_label, self.light_green, current_prayer_text)
            self.set_prayer_frame_colors(self.today_maghrib_frame, self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, self.light_red, next_prayer_text)
        
        elif hour_time >= maghrib_time and hour_time < isha_time:
            self.set_prayer_frame_colors(self.today_maghrib_frame, self.labels.today_maghrib_label, self.labels.today_maghrib_athan_label, 
                                  self.labels.today_maghrib_iqama_label, self.light_green, current_prayer_text)
            self.set_prayer_frame_colors(self.today_isha_frame, self.labels.today_isha_label, self.labels.today_isha_athan_label, 
                                  self.labels.today_isha_iqama_label, self.light_red, next_prayer_text)
        
        elif hour_time >= isha_time:
            self.set_prayer_frame_colors(self.today_isha_frame, self.labels.today_isha_label, self.labels.today_isha_athan_label, 
                                  self.labels.today_isha_iqama_label, self.light_green, current_prayer_text)
            self.set_prayer_frame_colors(self.tomorrow_fajr_frame, self.labels.tomorrow_fajr_label, self.labels.tomorrow_fajr_athan_label, 
                                  self.labels.tomorrow_fajr_iqama_label, self.light_red, next_prayer_text)
            
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
    
    def set_prayer_frame_colors(self, frame, label, athan_label, iqama_label, bg_color, text_color):
        """Set prayer frame and label colors for entire row with background"""
        frame_border_color = self.tan if self.args.r else rgb_to_hex((200, 200, 200))
        frame.setStyleSheet(f"background-color: {bg_color}; border: 2px solid {frame_border_color}; border-radius: 3px;")
        self.set_prayer_label_colors(label, athan_label, iqama_label, text_color)
    
    def set_prayer_label_colors(self, label, athan_label, iqama_label, text_color):
        """Set text color for prayer labels"""
        label.setStyleSheet(f"background-color: transparent; color: {text_color}; border: none;")
        athan_label.setStyleSheet(f"background-color: transparent; color: {text_color}; border: none;")
        if iqama_label and iqama_label.text():  # Only style iqama if it has text (Shurooq doesn't)
            iqama_label.setStyleSheet(f"background-color: transparent; color: {text_color}; border: none;")

    def get_daily_ayah(self):
        """Get daily ayah"""
        ayahs_path = os.path.join(BASE_DIR, '..', 'ayahs.json')

        try:
            with open(ayahs_path, 'r', encoding='utf-8') as f:
                ayahs_data = json.load(f)
                ayahs = ayahs_data['ayahs']

            # Use day of year to get days

            day_of_year = datetime.now().timetuple().tm_yday
            ayah_index = day_of_year % len(ayahs)

            return ayahs[ayah_index]
        except FileNotFoundError:
            return {
                "arabic": "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
                "translation": "In the name of Allah, the Most Gracious, the Most Merciful.",
                "reference": "Al-Fatihah 1:1"
            }
        except Exception as e:
            print(f"Error loading ayahs: {e}")
            return {
                "arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                "translation": "In the name of Allah, the Most Gracious, the Most Merciful.",
                "reference": "Al-Fatihah 1:1"
            }
        
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
