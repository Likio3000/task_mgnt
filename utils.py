import os
import json
import random
from datetime import datetime
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(BASE_DIR, 'progress.json')
TASK_COLORS_FILE = os.path.join(BASE_DIR, 'task_colors.json')

# Initialize Pygame Mixer
pygame.mixer.init()

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            progress = json.load(file)
            if 'daily_completed_hours' not in progress:
                progress['daily_completed_hours'] = 0
            if 'completed_tasks' not in progress:
                progress['completed_tasks'] = 0
            if 'last_updated' not in progress:
                progress['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            last_updated_date = datetime.strptime(progress['last_updated'], '%Y-%m-%d').date()
            current_date = datetime.now().date()
            if current_date > last_updated_date:
                progress['daily_completed_hours'] = 0
                progress['last_updated'] = current_date.strftime('%Y-%m-%d')
            return progress
    return {'completed_hours': 0, 'daily_completed_hours': 0, 'completed_tasks': 0, 'last_updated': datetime.now().strftime('%Y-%m-%d')}

def save_progress(progress):
    progress['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(progress, file)

def load_task_colors():
    if os.path.exists(TASK_COLORS_FILE):
        with open(TASK_COLORS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_task_colors(task_colors):
    with open(TASK_COLORS_FILE, 'w') as file:
        json.dump(task_colors, file)

def calculate_hours(start_time, end_time):
    start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
    return (end_dt - start_dt).total_seconds() / 3600

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
