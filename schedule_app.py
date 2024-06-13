from tkinter import Tk, BooleanVar, Checkbutton, StringVar, OptionMenu, messagebox, ttk
from datetime import datetime, timedelta
import pygame
import os
from database import create_tables, add_activity_to_db
from utils import load_progress, save_progress, calculate_hours, play_sound, load_task_colors, save_task_colors
from activity_widgets import ActivityWidgets
from progress_widgets import ProgressWidgets
from task_management import TaskManagement

# Constants for sound files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_FILE = os.path.join(BASE_DIR, 'sound1.mp3')
ERROR_SOUND_FILE = os.path.join(BASE_DIR, 'error_sound.mp3')
TOTAL_HOURS = 10000
DAILY_GOAL_HOURS = 8

class SchedulePlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Planner")
        self.auto_refresh = BooleanVar(value=False)
        self.progress = load_progress()
        self.task_colors = load_task_colors()

        self.activity_widgets = ActivityWidgets(self.root, self.add_activity)
        self.task_management = TaskManagement(self.root, self.progress)
        self.progress_widgets = ProgressWidgets(self.root, self.progress)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.auto_refresh_check()
        self.schedule_daily_reset()

    def add_activity(self):
        title = self.activity_widgets.title_entry.get()
        description = self.activity_widgets.desc_entry.get()
        start_time = self.activity_widgets.start_entry.get()
        end_time = self.activity_widgets.end_entry.get()
        reward = self.activity_widgets.reward_var.get()
        color = getattr(self.activity_widgets, 'color', 'white')  # Get the color
        if title and start_time and end_time:
            try:
                datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                datetime.strptime(end_time, '%Y-%m-%d %H:%M')
                add_activity_to_db(title, description, start_time, end_time, reward)
                hours_completed = calculate_hours(start_time, end_time) * {"Low": 1, "Medium": 1.5, "High": 2}[reward]
                self.progress['completed_hours'] += hours_completed
                self.progress['daily_completed_hours'] += hours_completed

                if title not in self.task_colors:
                    self.task_colors[title] = color
                    save_task_colors(self.task_colors)

                save_progress(self.progress)
                play_sound(SOUND_FILE)
                self.progress_widgets.update_progress_bars()
                self.task_management.load_activities()
                self.activity_widgets.clear_entries()
            except ValueError:
                play_sound(ERROR_SOUND_FILE)
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD HH:MM")
        else:
            play_sound(ERROR_SOUND_FILE)
            messagebox.showerror("Error", "Please fill in all fields")

    def filter_activities(self, filter_option):
        self.task_management.filter_activities(filter_option)

    def auto_refresh_check(self):
        if self.auto_refresh.get():
            self.task_management.load_activities()
        self.root.after(10000, self.auto_refresh_check)

    def reset_daily_progress(self):
        self.progress['daily_completed_hours'] = 0
        save_progress(self.progress)
        self.progress_widgets.update_progress_bars()
        self.schedule_daily_reset()

    def schedule_daily_reset(self):
        now = datetime.now()
        midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delay = (midnight - now).total_seconds()
        self.root.after(int(delay * 1000), self.reset_daily_progress)

def main():
    create_tables()
    root = Tk()
    app = SchedulePlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
