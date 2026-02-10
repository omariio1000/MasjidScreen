"""
Modern Masjid Display with Embedded Prayer Times Website
Created on February 2026

@author: Omar Nassar
"""

import time as tm
from datetime import datetime
import os
import argparse
import trivia
import ramadan_times
import textwrap
import json
from stats import printAllStats
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                              QFrame, QVBoxLayout, QHBoxLayout, QPushButton,
                              QGraphicsDropShadowEffect)
from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtGui import QPixmap, QFont, QColor, QFontDatabase, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage

# Base directory and config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'config.json')

tq_image = []
testDay = 0


class RamadanLabels:
    """Class to store ramadan trivia labels"""
    def __init__(self, winner_parent, question_parent, bg_color, text_color, font1, font2, font3):
        # Winner labels - combined first/last name (no border)
        label_style = f"background-color: {bg_color}; color: {text_color}; border: none;"
        
        self.winner_one = QLabel(winner_parent)
        self.winner_one.setStyleSheet(label_style)
        self.winner_one.setFont(font1)
        self.winner_one.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.winner_two = QLabel(winner_parent)
        self.winner_two.setStyleSheet(label_style)
        self.winner_two.setFont(font1)
        self.winner_two.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.winner_three = QLabel(winner_parent)
        self.winner_three.setStyleSheet(label_style)
        self.winner_three.setFont(font1)
        self.winner_three.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Question labels (no border - container has border)
        self.question_one = QLabel(question_parent)
        self.question_one.setStyleSheet(label_style)
        self.question_one.setFont(font2)
        self.question_one.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_one.setWordWrap(True)
        
        self.question_one_options = QLabel(question_parent)
        self.question_one_options.setStyleSheet(label_style)
        self.question_one_options.setFont(font3)
        self.question_one_options.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.question_one_options.setWordWrap(True)
        
        self.question_two = QLabel(question_parent)
        self.question_two.setStyleSheet(label_style)
        self.question_two.setFont(font2)
        self.question_two.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_two.setWordWrap(True)
        
        self.question_two_options = QLabel(question_parent)
        self.question_two_options.setStyleSheet(label_style)
        self.question_two_options.setFont(font3)
        self.question_two_options.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.question_two_options.setWordWrap(True)

        self.question_three = QLabel(question_parent)
        self.question_three.setStyleSheet(label_style)
        self.question_three.setFont(font2)
        self.question_three.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_three.setWordWrap(True)
        
        self.question_three_options = QLabel(question_parent)
        self.question_three_options.setStyleSheet(label_style)
        self.question_three_options.setFont(font3)
        self.question_three_options.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.question_three_options.setWordWrap(True)

        # QR code
        self.trivia_qr = QLabel("")


def update_trivia(day, ramadan_labels, height_value, test=False):
    """Update trivia questions and winners"""
    print(f"Day {day} of Ramadan")

    if day <= 0 or day > 30:
        trivia.make_qr_with_link("icc-hillsboro.org", 'trivia.png')
        ramadan_labels.question_one.setText('')
        ramadan_labels.question_one_options.setText('')

        if day > 0:
            ramadan_labels.question_two.setText("Thank you for participating!")
            ramadan_labels.question_two_options.setText("We hope you join us again next year inshaAllah!")
            ramadan_labels.question_two_options.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center fallback
        else:
            ramadan_labels.question_two.setText("Ramadan is starting soon!")
            ramadan_labels.question_two_options.setText("We hope you join us for trivia this year inshaAllah!")
            ramadan_labels.question_two_options.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center fallback

        ramadan_labels.question_three.setText('')
        ramadan_labels.question_three_options.setText('')

        ramadan_labels.winner_one.setText("")
        ramadan_labels.winner_two.setText("")
        ramadan_labels.winner_three.setText("")
    else:
        trivia.make_qr(day)
        question, option1, option2, option3, option4 = trivia.get_form_questions_options(day)
        
        # Helper to strip leading option letters like "A) " or "a. "
        import re
        def strip_option_prefix(opt):
            if not opt:
                return ""
            return re.sub(r'^[A-Da-d][\)\.\:]\s*', '', opt)
        
        def format_options(o1, o2, o3, o4):
            # Each option on its own line
            lines = [
                f"A) {strip_option_prefix(o1)}",
                f"B) {strip_option_prefix(o2)}",
                f"C) {strip_option_prefix(o3)}"
            ]
            if o4:
                lines.append(f"D) {strip_option_prefix(o4)}")
            return "\n".join(lines)
        
        if not question or len(question) < 3:
            ramadan_labels.question_one.setText('')
            ramadan_labels.question_one_options.setText('')
            ramadan_labels.question_two.setText("Trivia questions not available yet")
            ramadan_labels.question_two_options.setText("Please check back later!")
            ramadan_labels.question_two_options.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center fallback
            ramadan_labels.question_three.setText('')
            ramadan_labels.question_three_options.setText('')
        else:
            ramadan_labels.question_one.setText('\n'.join(textwrap.wrap(question[0], width=95)))
            ramadan_labels.question_one_options.setText(format_options(option1[0], option2[0], option3[0], option4[0] if len(option4) > 0 else ""))
            ramadan_labels.question_one_options.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Left for options
            ramadan_labels.question_two.setText('\n'.join(textwrap.wrap(question[1], width=95)))
            ramadan_labels.question_two_options.setText(format_options(option1[1], option2[1], option3[1], option4[1] if len(option4) > 1 else ""))
            ramadan_labels.question_two_options.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Left for options
            ramadan_labels.question_three.setText('\n'.join(textwrap.wrap(question[2], width=95)))
            ramadan_labels.question_three_options.setText(format_options(option1[2], option2[2], option3[2], option4[2] if len(option4) > 2 else ""))
            ramadan_labels.question_three_options.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Left for options

    if day >= 2 and day <= 31:
        if not trivia.check_winners_updated(str(day - 1)):
            winners = trivia.get_winners(day - 1)
            trivia.log_winners(str(day - 1), winners, test)
        else:
            winners = trivia.get_past_winners(str(day - 1))
        winners = [sublist[:1] for sublist in winners]
        print(f"Winners: {winners}")

        if winners:
            if len(winners) >= 1:
                name = winners[0][0]
                first = name.split(" ")[0].capitalize()
                last = name.split(" ")[-1].capitalize() if len(name.split(" ")) > 1 else ""
                ramadan_labels.winner_one.setText(f"{first} {last}".strip())
                ramadan_labels.winner_two.setText("")
                ramadan_labels.winner_three.setText("")

            if len(winners) >= 2:
                name = winners[1][0]
                first = name.split(" ")[0].capitalize()
                last = name.split(" ")[-1].capitalize() if len(name.split(" ")) > 1 else ""
                ramadan_labels.winner_two.setText(f"{first} {last}".strip())

            if len(winners) >= 3:
                name = winners[2][0]
                first = name.split(" ")[0].capitalize()
                last = name.split(" ")[-1].capitalize() if len(name.split(" ")) > 1 else ""
                ramadan_labels.winner_three.setText(f"{first} {last}".strip())
        else:
            ramadan_labels.winner_one.setText("No Winners Yesterday")
            ramadan_labels.winner_two.setText("")
            ramadan_labels.winner_three.setText("")
    elif day == 1:
        # Day 1: no previous winners to show
        ramadan_labels.winner_one.setText("First Day of Trivia!")
        ramadan_labels.winner_two.setText("")
        ramadan_labels.winner_three.setText("")

    pixmap = QPixmap('trivia.png')
    pixmap = pixmap.scaled(int(height_value * 0.22), int(height_value * 0.22), 
                           Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    tq_image.clear()
    tq_image.append(pixmap)
    # Update QR - works for both QLabel and QPushButton
    if hasattr(ramadan_labels.trivia_qr, 'setIcon'):
        ramadan_labels.trivia_qr.setIcon(QIcon(tq_image[0]))
        ramadan_labels.trivia_qr.setIconSize(tq_image[0].size())
    else:
        ramadan_labels.trivia_qr.setPixmap(tq_image[0])
    print("\nStats so far:")
    printAllStats()
    print()


class ModernDisplayWindow(QMainWindow):
    """Modern masjid display with embedded website"""
    
    # Color scheme for Ramadan overlays - Dark gray and green (masjid theme)
    CARD_BG = "#1a1a1a"
    ACCENT = "#2d2d2d"
    HIGHLIGHT = "#2e7d32"
    TEXT_PRIMARY = "#ffffff"
    
    def __init__(self, args, config):
        super().__init__()
        self.args = args
        self.config = config
        self.ramadan_updated = False
        
        self.init_ui()
        
        # Timer for Ramadan updates
        if self.args.r:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_display)
            self.timer.start(1000)
    
    def init_ui(self):
        self.setWindowTitle('ICCH Modern Display')
        
        # Screen dimensions
        screen = QApplication.primaryScreen().geometry()
        self.width_value = screen.width()
        self.height_value = screen.height()
        self.setGeometry(0, 0, self.width_value, self.height_value)
        
        # Central widget with background image
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: black;")
        
        # Background image label (scaled to cover, cropped if needed)
        bg_label = QLabel(central_widget)
        bg_label.setGeometry(0, 0, self.width_value, self.height_value)
        bg_path = os.path.join(BASE_DIR, '..', 'resources', 'ICCH Cover.png')
        bg_pixmap = QPixmap(bg_path)
        # Scale to fill (cover) - maintains aspect ratio, may crop
        scaled_pixmap = bg_pixmap.scaled(self.width_value, self.height_value,
                                         Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                         Qt.TransformationMode.SmoothTransformation)
        # Center crop if larger than screen
        if scaled_pixmap.width() > self.width_value or scaled_pixmap.height() > self.height_value:
            x = (scaled_pixmap.width() - self.width_value) // 2
            y = (scaled_pixmap.height() - self.height_value) // 2
            scaled_pixmap = scaled_pixmap.copy(x, y, self.width_value, self.height_value)
        bg_label.setPixmap(scaled_pixmap)
        bg_label.lower()  # Send to back
        
        # Create full-screen web view
        self.create_website_panel(central_widget)
        
        # Ramadan mode overlays
        if self.args.r:
            self.setup_ramadan_mode(central_widget)
        else:
            self.ramadan_labels = None
        
        self.showFullScreen()
    
    def create_website_panel(self, parent):
        """Create the embedded website panel - 16:9 in top-left for Ramadan mode"""
        # Create persistent profile FIRST with storage path (use absolute paths)
        cache_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'web_cache'))
        os.makedirs(cache_path, exist_ok=True)
        
        # Create a named profile (not default) so it persists properly
        self.web_profile = QWebEngineProfile("MasjidDisplay", self)
        self.web_profile.setPersistentStoragePath(cache_path)
        self.web_profile.setCachePath(os.path.join(cache_path, 'cache'))
        self.web_profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.web_profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Create page with the persistent profile
        self.web_page = QWebEnginePage(self.web_profile, self)
        
        # Create web view and set the persistent page
        self.web_view = QWebEngineView(parent)
        self.web_view.setPage(self.web_page)
        
        if self.args.r:
            # Ramadan mode: 16:9 web view in top-left corner
            # Calculate 16:9 dimensions that fit in top-left area
            web_width = int(self.width_value * 0.78)  # 78% of screen width
            web_height = int(web_width * 9 / 16)  # 16:9 aspect ratio
            self.web_view.setGeometry(0, 0, web_width, web_height)
        else:
            # Normal mode: full screen
            self.web_view.setGeometry(0, 0, self.width_value, self.height_value)
        
        # Configure web settings for proper rendering (PyQt6 syntax)
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        
        # Load the prayer times website
        prayer_url = self.config.get("prayer_website", "https://muslimplus.org")
        self.web_view.setUrl(QUrl(prayer_url))
        
        print(f"📱 Loading prayer times from: {prayer_url}")
    
    def setup_ramadan_mode(self, parent):
        """Setup Ramadan trivia display - web view top-left, trivia fills the rest"""
        bg_color = self.CARD_BG
        text_color = self.TEXT_PRIMARY
        
        # Load fonts
        font_path = os.path.join(BASE_DIR, '..', 'resources', 'fonts')
        for font_file in ["Helvetica.ttf", "Helvetica-Bold.ttf"]:
            full_path = os.path.join(font_path, font_file)
            if os.path.exists(full_path):
                QFontDatabase.addApplicationFont(full_path)
        
        font1 = QFont("Helvetica", int(24 * (self.height_value / 1080)), QFont.Weight.Bold)
        font2 = QFont("Helvetica", int(14 * (self.height_value / 1080)), QFont.Weight.Bold)  # Question text
        font3 = QFont("Helvetica", int(12 * (self.height_value / 1080)))  # Options text
        
        day = trivia.get_trivia_day()
        
        # Calculate web view dimensions (16:9 top-left)
        web_width = int(self.width_value * 0.78)
        web_height = int(web_width * 9 / 16)
        
        # Right panel width (area to the right of web view)
        right_panel_x = web_width + 10
        right_panel_width = self.width_value - right_panel_x - 10
        
        # Bottom panel height (area below web view)
        bottom_panel_y = web_height + 10
        bottom_panel_height = self.height_value - bottom_panel_y - 10
        
        # ===== WINNERS FRAME - Top Right =====
        winners_frame = QFrame(parent)
        winners_layout = QVBoxLayout(winners_frame)
        winners_layout.setContentsMargins(15, 15, 15, 15)
        winners_layout.setSpacing(15)
        winners_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(30, 30, 30, 0.92);
                border-radius: 12px;
                border: 2px solid {self.HIGHLIGHT};
            }}
            QFrame QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(5, 5)
        winners_frame.setGraphicsEffect(shadow)
        
        # Winners title - LARGER
        winners_title = QLabel("Yesterday's Winners", winners_frame)
        winners_title.setStyleSheet(f"background: transparent; color: {self.HIGHLIGHT}; font-weight: bold; border: none;")
        winners_title.setFont(QFont("Helvetica", int(22 * (self.height_value / 1080)), QFont.Weight.Bold))
        winners_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        winners_layout.addWidget(winners_title)
        
        # ===== QUESTIONS - 3 Individual Boxes =====
        # Container for question boxes (no background, just for layout)
        questions_container = QFrame(parent)
        questions_container.setStyleSheet("background: transparent;")
        questions_layout = QHBoxLayout(questions_container)
        questions_layout.setContentsMargins(10, 10, 10, 10)
        questions_layout.setSpacing(15)
        
        self.ramadan_labels = RamadanLabels(winners_frame, questions_container, "transparent", text_color, font1, font2, font3)
        
        # Winners layout (vertical) - 3 combined name labels, spaced out, no individual boxes
        winners_layout.addStretch(1)
        self.ramadan_labels.winner_one.setFont(QFont("Helvetica", int(20 * (self.height_value / 1080)), QFont.Weight.Bold))
        winners_layout.addWidget(self.ramadan_labels.winner_one)
        winners_layout.addStretch(1)
        self.ramadan_labels.winner_two.setFont(QFont("Helvetica", int(20 * (self.height_value / 1080)), QFont.Weight.Bold))
        winners_layout.addWidget(self.ramadan_labels.winner_two)
        winners_layout.addStretch(1)
        self.ramadan_labels.winner_three.setFont(QFont("Helvetica", int(20 * (self.height_value / 1080)), QFont.Weight.Bold))
        winners_layout.addWidget(self.ramadan_labels.winner_three)
        winners_layout.addStretch(1)
        
        # Style for question boxes - translucent grey with green border (only for direct QFrame, not children)
        question_box_style = f"""
            QFrame {{
                background-color: rgba(45, 45, 45, 0.88);
                border-radius: 10px;
                border: 2px solid {self.HIGHLIGHT};
            }}
            QFrame QLabel {{
                border: none;
                background: transparent;
            }}
        """
        
        # Question 1 box
        q1_container = QFrame(questions_container)
        q1_container.setStyleSheet(question_box_style)
        q1_layout = QVBoxLayout(q1_container)
        q1_layout.setContentsMargins(12, 8, 12, 8)
        q1_layout.setSpacing(4)
        q1_layout.addWidget(self.ramadan_labels.question_one)
        q1_layout.addWidget(self.ramadan_labels.question_one_options)
        questions_layout.addWidget(q1_container, 1)
        
        # Question 2 box
        q2_container = QFrame(questions_container)
        q2_container.setStyleSheet(question_box_style)
        q2_layout = QVBoxLayout(q2_container)
        q2_layout.setContentsMargins(12, 8, 12, 8)
        q2_layout.setSpacing(4)
        q2_layout.addWidget(self.ramadan_labels.question_two)
        q2_layout.addWidget(self.ramadan_labels.question_two_options)
        questions_layout.addWidget(q2_container, 1)
        
        # Question 3 box
        q3_container = QFrame(questions_container)
        q3_container.setStyleSheet(question_box_style)
        q3_layout = QVBoxLayout(q3_container)
        q3_layout.setContentsMargins(12, 8, 12, 8)
        q3_layout.setSpacing(4)
        q3_layout.addWidget(self.ramadan_labels.question_three)
        q3_layout.addWidget(self.ramadan_labels.question_three_options)
        questions_layout.addWidget(q3_container, 1)
        
        # Position winners frame - Top Right
        winners_w = right_panel_width
        winners_h = int(self.height_value * 0.28)
        winners_x = right_panel_x
        winners_y = 10
        winners_frame.setGeometry(winners_x, winners_y, winners_w, winners_h)
        
        # Position questions container - Full width bottom to screen edge
        questions_x = 10
        questions_y = bottom_panel_y
        questions_w = self.width_value - 20
        questions_h = self.height_value - bottom_panel_y - 10  # Full height to bottom
        questions_container.setGeometry(questions_x, questions_y, questions_w, questions_h)
        
        winners_frame.raise_()
        questions_container.raise_()
        winners_frame.show()
        questions_container.show()
        
        # Initial trivia update
        update_trivia(day - 1, self.ramadan_labels, self.height_value, test=self.args.t)
        
        # ===== QR CODE - Middle of right panel (Clickable) =====
        qr_size = int(self.height_value * 0.22)
        
        # Use QPushButton for clickable QR
        self.qr_button = QPushButton(parent)
        self.qr_button.setFixedSize(qr_size + 16, qr_size + 16)
        self.qr_button.setStyleSheet("""
            QPushButton {
                background: white;
                border-radius: 12px;
                border: none;
                padding: 6px;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
            QPushButton:pressed {
                background: #e0e0e0;
            }
        """)
        self.qr_button.clicked.connect(self.test_handler)
        
        # Set QR icon
        pixmap = QPixmap('trivia.png')
        pixmap = pixmap.scaled(qr_size, qr_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.qr_button.setIcon(QIcon(pixmap))
        self.qr_button.setIconSize(pixmap.size())
        
        # Position QR - Center of right panel vertically
        qr_x = right_panel_x + (right_panel_width - qr_size - 16) // 2
        # Middle of the space between winners and bottom of web view
        available_space = web_height - winners_h - 20
        qr_y = winners_y + winners_h + (available_space - qr_size - 70) // 2
        self.qr_button.setGeometry(qr_x, qr_y, qr_size + 16, qr_size + 16)
        
        # "Scan for today's questions" label below QR - two lines
        self.qr_label = QLabel("Scan for\nToday's Questions", parent)
        self.qr_label.setStyleSheet(f"background: transparent; color: {self.TEXT_PRIMARY};")
        self.qr_label.setFont(QFont("Helvetica", int(16 * (self.height_value / 1080)), QFont.Weight.Bold))
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_width = right_panel_width - 20
        self.qr_label.setGeometry(right_panel_x + 10, qr_y + qr_size + 35, label_width, 60)
        
        self.qr_button.raise_()
        self.qr_label.raise_()
        self.qr_button.show()
        self.qr_label.show()
        
        # Store reference for updates
        self.ramadan_labels.trivia_qr = self.qr_button
    
    def test_handler(self):
        """Test mode handler"""
        global testDay
        testDay += 1
        update_trivia(testDay, self.ramadan_labels, self.height_value, test=True)
    
    def update_display(self):
        """Update loop for Ramadan mode - triggers at Isha adhan time"""
        current_time = tm.strftime('%H:%M')
        current_day = trivia.get_trivia_day()
        
        # Get Isha time for current Ramadan day
        isha_time = ramadan_times.get_isha_time_for_day(current_day)
        
        if isha_time:
            # Check if we just hit Isha time (within 1 minute window)
            if current_time >= isha_time and current_time < self._add_minutes(isha_time, 1):
                if not self.ramadan_updated:
                    print(f"\n🌙 Isha adhan time ({isha_time}) - selecting winners and updating trivia...")
                    update_trivia(current_day, self.ramadan_labels, self.height_value)
                    self.ramadan_updated = True
            elif current_time >= self._add_minutes(isha_time, 1):
                # Reset flag after the 1-minute window
                if self.ramadan_updated:
                    self.ramadan_updated = False
        else:
            # Fallback to midnight if no Isha time available
            if current_time >= "00:00" and current_time < "00:01":
                if not self.ramadan_updated:
                    update_trivia(current_day, self.ramadan_labels, self.height_value)
                    self.ramadan_updated = True
            elif current_time >= "00:01":
                self.ramadan_updated = False
    
    def _add_minutes(self, time_str: str, minutes: int) -> str:
        """Add minutes to a HH:MM time string"""
        h, m = map(int, time_str.split(':'))
        m += minutes
        if m >= 60:
            h += 1
            m -= 60
        if h >= 24:
            h = 0
        return f"{h:02d}:{m:02d}"
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_F5:
            # Refresh website
            self.web_view.reload()
            print("🔄 Refreshed website")
        elif event.key() == Qt.Key.Key_Space and self.args.t and self.ramadan_labels:
            # Test mode: advance trivia day with spacebar
            self.test_handler()


def main():
    """Run modern prayer screen"""
    parser = argparse.ArgumentParser(description="Modern Masjid Display with Embedded Website")
    parser.add_argument("-r", action="store_true", help="Enable Ramadan mode (shows trivia overlays)")
    parser.add_argument("-t", action="store_true", help="Enable test mode")
    args = parser.parse_args()
    
    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)
    
    # Set default prayer website if not in config
    if "prayer_website" not in config:
        config["prayer_website"] = "https://muslimplus.org"
    
    print(f"\n🕌 Starting Modern Masjid Display")
    print(f"📱 Prayer times from: {config.get('prayer_website', 'muslimplus.org')}")
    if args.r:
        print("🌙 Ramadan mode enabled (trivia overlays)")
    if args.t:
        print("🧪 Test mode enabled (press Space to advance trivia day)")
    print()
    
    app = QApplication(sys.argv)
    window = ModernDisplayWindow(args, config)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
