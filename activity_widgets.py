from tkinter import Frame, Label, Entry, Button, OptionMenu, StringVar, messagebox
from datetime import datetime, timedelta

class ActivityWidgets:
    def __init__(self, parent, add_activity_callback):
        self.frame = Frame(parent)
        self.frame.pack(pady=20)

        self.title_label = Label(self.frame, text="Title")
        self.title_label.grid(row=0, column=0)
        self.title_entry = Entry(self.frame)
        self.title_entry.grid(row=0, column=1)

        self.desc_label = Label(self.frame, text="Description")
        self.desc_label.grid(row=1, column=0)
        self.desc_entry = Entry(self.frame)
        self.desc_entry.grid(row=1, column=1)

        self.start_label = Label(self.frame, text="Start Time")
        self.start_label.grid(row=2, column=0)
        self.start_entry = Entry(self.frame)
        self.start_entry.grid(row=2, column=1)
        self.start_now_button = Button(self.frame, text="Now", command=self.set_start_time_now)
        self.start_now_button.grid(row=2, column=2)
        self.start_today_button = Button(self.frame, text="Today", command=self.set_start_date_today)
        self.start_today_button.grid(row=2, column=3)

        self.add_start_30min_button = Button(self.frame, text="+30 Min", command=lambda: self.increment_start_time(30))
        self.add_start_30min_button.grid(row=2, column=4)
        self.add_start_1hr_button = Button(self.frame, text="+1 Hr", command=lambda: self.increment_start_time(60))
        self.add_start_1hr_button.grid(row=2, column=5)
        self.add_start_2hr_button = Button(self.frame, text="+2 Hr", command=lambda: self.increment_start_time(120))
        self.add_start_2hr_button.grid(row=2, column=6)
        self.add_start_4hr_button = Button(self.frame, text="+4 Hr", command=lambda: self.increment_start_time(240))
        self.add_start_4hr_button.grid(row=2, column=7)
        self.add_start_1day_button = Button(self.frame, text="+1 Day", command=lambda: self.increment_start_time(1440))
        self.add_start_1day_button.grid(row=2, column=8)

        self.end_label = Label(self.frame, text="End Time")
        self.end_label.grid(row=3, column=0)
        self.end_entry = Entry(self.frame)
        self.end_entry.grid(row=3, column=1)
        self.end_now_button = Button(self.frame, text="Now", command=self.set_end_time_now)
        self.end_now_button.grid(row=3, column=2)
        self.end_today_button = Button(self.frame, text="Today", command=self.set_end_date_today)
        self.end_today_button.grid(row=3, column=3)

        self.add_end_30min_button = Button(self.frame, text="+30 Min", command=lambda: self.increment_end_time(30))
        self.add_end_30min_button.grid(row=3, column=4)
        self.add_end_1hr_button = Button(self.frame, text="+1 Hr", command=lambda: self.increment_end_time(60))
        self.add_end_1hr_button.grid(row=3, column=5)
        self.add_end_2hr_button = Button(self.frame, text="+2 Hr", command=lambda: self.increment_end_time(120))
        self.add_end_2hr_button.grid(row=3, column=6)
        self.add_end_4hr_button = Button(self.frame, text="+4 Hr", command=lambda: self.increment_end_time(240))
        self.add_end_4hr_button.grid(row=3, column=7)
        self.add_end_1day_button = Button(self.frame, text="+1 Day", command=lambda: self.increment_end_time(1440))
        self.add_end_1day_button.grid(row=3, column=8)

        self.reward_label = Label(self.frame, text="Reward")
        self.reward_label.grid(row=4, column=0)
        self.reward_var = StringVar()
        self.reward_options = ["Low", "Medium", "High"]
        self.reward_var.set(self.reward_options[0])
        self.reward_menu = OptionMenu(self.frame, self.reward_var, *self.reward_options)
        self.reward_menu.grid(row=4, column=1)

        self.add_button = Button(self.frame, text="Add Activity", command=add_activity_callback, bg='red')
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Add buttons for predefined tasks with specific colors
        self.coding_button = Button(self.frame, text="Coding Session", command=lambda: self.set_coding_session(add_activity_callback), bg='lightblue')
        self.coding_button.grid(row=6, column=0, pady=10)
        self.break_button = Button(self.frame, text="Break", command=lambda: self.set_break(add_activity_callback), bg='lightgreen')
        self.break_button.grid(row=6, column=1, pady=10)
        self.scheduling_button = Button(self.frame, text="Scheduling", command=lambda: self.set_scheduling(add_activity_callback), bg='lightcoral')
        self.scheduling_button.grid(row=6, column=2, pady=10)
        self.eating_button = Button(self.frame, text="Eating Break", command=lambda: self.set_eating_break(add_activity_callback), bg='lightyellow')
        self.eating_button.grid(row=6, column=3, pady=10)

        self.add_custom_task_button()  # Add this line

    # Predefined task methods with color
    def set_coding_session(self, add_activity_callback):
        self.set_task("Coding Session", "A basic coding session", timedelta(minutes=55), color='lightblue')
        add_activity_callback()

    def set_break(self, add_activity_callback):
        self.set_task("Break", "A small break from coding", timedelta(minutes=5), color='lightgreen')
        add_activity_callback()

    def set_scheduling(self, add_activity_callback):
        self.set_task("Scheduling", "A scheduling session", timedelta(minutes=10), "High", color='lightcoral')
        add_activity_callback()

    def set_eating_break(self, add_activity_callback):
        self.set_task("Eating Break", "A small eating break", timedelta(hours=1), "Low", color='lightyellow')
        add_activity_callback()

    def set_task(self, title, description, duration, reward="Low", color="white"):
        now = datetime.now()
        self.title_entry.delete(0, 'end')
        self.title_entry.insert(0, title)
        self.desc_entry.delete(0, 'end')
        self.desc_entry.insert(0, description)
        self.start_entry.delete(0, 'end')
        self.start_entry.insert(0, now.strftime('%Y-%m-%d %H:%M'))
        self.end_entry.delete(0, 'end')
        self.end_entry.insert(0, (now + duration).strftime('%Y-%m-%d %H:%M'))
        self.reward_var.set(reward)
        self.color = color

    # Helper methods for setting start and end times
    def set_start_time_now(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.start_entry.delete(0, 'end')
        self.start_entry.insert(0, now)

    def set_end_time_now(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.end_entry.delete(0, 'end')
        self.end_entry.insert(0, now)

    def set_start_date_today(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.start_entry.delete(0, 'end')
        self.start_entry.insert(0, today + " 00:00")

    def set_end_date_today(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.end_entry.delete(0, 'end')
        self.end_entry.insert(0, today + " 23:59")

    def increment_start_time(self, minutes):
        start_time_str = self.start_entry.get()
        if start_time_str:
            try:
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format in start time. Please use YYYY-MM-DD HH:MM")
                return
        else:
            start_time = datetime.now()

        new_start_time = start_time + timedelta(minutes=minutes)
        self.start_entry.delete(0, 'end')
        self.start_entry.insert(0, new_start_time.strftime('%Y-%m-%d %H:%M'))

    def increment_end_time(self, minutes):
        start_time_str = self.start_entry.get()
        end_time_str = self.end_entry.get()
        if end_time_str:
            try:
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format in end time. Please use YYYY-MM-DD HH:MM")
                return
        else:
            if start_time_str:
                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format in start time. Please use YYYY-MM-DD HH:MM")
                    return
            else:
                start_time = datetime.now()
            end_time = start_time

        new_end_time = end_time + timedelta(minutes=minutes)
        self.end_entry.delete(0, 'end')
        self.end_entry.insert(0, new_end_time.strftime('%Y-%m-%d %H:%M'))

    # Method to clear form entries
    def clear_entries(self):
        self.title_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.start_entry.delete(0, 'end')
        self.end_entry.delete(0, 'end')
        self.reward_var.set(self.reward_options[0])

    def add_custom_task_button(self):
        self.custom_button_frame = Frame(self.frame)
        self.custom_button_frame.grid(row=7, column=0, columnspan=9, pady=10)
        
        self.custom_title_label = Label(self.custom_button_frame, text="Custom Task Title")
        self.custom_title_label.grid(row=0, column=0)
        self.custom_title_entry = Entry(self.custom_button_frame)
        self.custom_title_entry.grid(row=0, column=1)

        self.custom_desc_label = Label(self.custom_button_frame, text="Description")
        self.custom_desc_label.grid(row=0, column=2)
        self.custom_desc_entry = Entry(self.custom_button_frame)
        self.custom_desc_entry.grid(row=0, column=3)

        self.custom_duration_label = Label(self.custom_button_frame, text="Duration (mins)")
        self.custom_duration_label.grid(row=0, column=4)
        self.custom_duration_entry = Entry(self.custom_button_frame)
        self.custom_duration_entry.grid(row=0, column=5)

        self.custom_reward_label = Label(self.custom_button_frame, text="Reward")
        self.custom_reward_label.grid(row=0, column=6)
        self.custom_reward_var = StringVar()
        self.custom_reward_var.set(self.reward_options[0])
        self.custom_reward_menu = OptionMenu(self.custom_button_frame, self.custom_reward_var, *self.reward_options)
        self.custom_reward_menu.grid(row=0, column=7)

        self.custom_color_label = Label(self.custom_button_frame, text="Color")
        self.custom_color_label.grid(row=0, column=8)
        self.custom_color_entry = Entry(self.custom_button_frame)
        self.custom_color_entry.grid(row=0, column=9)

        self.add_custom_button = Button(self.custom_button_frame, text="Add Custom Task Button", command=self.create_custom_task_button, bg='purple')
        self.add_custom_button.grid(row=1, column=0, columnspan=10, pady=10)

    def create_custom_task_button(self):
        title = self.custom_title_entry.get()
        description = self.custom_desc_entry.get()
        duration = self.custom_duration_entry.get()
        reward = self.custom_reward_var.get()
        color = self.custom_color_entry.get()

        if title and description and duration and reward and color:
            try:
                duration = int(duration)
                new_button = Button(self.frame, text=title, command=lambda: self.set_task(title, description, timedelta(minutes=duration), reward, color), bg=color)
                new_button.grid(row=8, column=0, pady=10)
            except ValueError:
                messagebox.showerror("Error", "Invalid duration value. Please enter an integer.")
        else:
            messagebox.showerror("Error", "Please fill in all fields for the custom task.")
