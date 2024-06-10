from tkinter import Frame, Label, Entry, Button, OptionMenu, StringVar, Canvas, messagebox
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

        self.end_label = Label(self.frame, text="End Time")
        self.end_label.grid(row=3, column=0)
        self.end_entry = Entry(self.frame)
        self.end_entry.grid(row=3, column=1)
        self.end_now_button = Button(self.frame, text="Now", command=self.set_end_time_now)
        self.end_now_button.grid(row=3, column=2)
        self.end_today_button = Button(self.frame, text="Today", command=self.set_end_date_today)
        self.end_today_button.grid(row=3, column=3)

        self.add_30min_button = Button(self.frame, text="+30 Min", command=lambda: self.increment_end_time_from_start(30))
        self.add_30min_button.grid(row=3, column=4)
        self.add_1hr_button = Button(self.frame, text="+1 Hr", command=lambda: self.increment_end_time_from_start(60))
        self.add_1hr_button.grid(row=3, column=5)
        self.add_2hr_button = Button(self.frame, text="+2 Hr", command=lambda: self.increment_end_time_from_start(120))
        self.add_2hr_button.grid(row=3, column=6)
        self.add_4hr_button = Button(self.frame, text="+4 Hr", command=lambda: self.increment_end_time_from_start(240))
        self.add_4hr_button.grid(row=3, column=7)
        self.add_1day_button = Button(self.frame, text="+1 Day", command=lambda: self.increment_end_time_from_start(1440))
        self.add_1day_button.grid(row=3, column=8)

        self.reward_label = Label(self.frame, text="Reward")
        self.reward_label.grid(row=4, column=0)
        self.reward_var = StringVar()
        self.reward_options = ["Low", "Medium", "High"]
        self.reward_var.set(self.reward_options[0])
        self.reward_menu = OptionMenu(self.frame, self.reward_var, *self.reward_options)
        self.reward_menu.grid(row=4, column=1)

        self.add_button = Button(self.frame, text="Add Activity", command=add_activity_callback, bg='red')
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Add buttons for predefined tasks
        self.coding_button = Button(self.frame, text="Coding Session", command=self.set_coding_session, bg='lightblue')
        self.coding_button.grid(row=6, column=0, pady=10)
        self.break_button = Button(self.frame, text="Break", command=self.set_break, bg='lightgreen')
        self.break_button.grid(row=6, column=1, pady=10)
        self.scheduling_button = Button(self.frame, text="Scheduling", command=self.set_scheduling, bg='lightcoral')
        self.scheduling_button.grid(row=6, column=2, pady=10)
        self.eating_button = Button(self.frame, text="Eating Break", command=self.set_eating_break, bg='lightyellow')
        self.eating_button.grid(row=6, column=3, pady=10)

    # Predefined task methods
    def set_coding_session(self):
        self.set_task("Coding Session", "A basic coding session", timedelta(minutes=55))

    def set_break(self):
        self.set_task("Break", "A small break from coding", timedelta(minutes=5))

    def set_scheduling(self):
        self.set_task("Scheduling", "A scheduling session", timedelta(minutes=10), "High")

    def set_eating_break(self):
        self.set_task("Eating Break", "A small eating break", timedelta(hours=1), "Low")

    def set_task(self, title, description, duration, reward="Low"):
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

    def increment_end_time_from_start(self, minutes):
        start_time_str = self.start_entry.get()
        if start_time_str:
            try:
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
                new_end_time = start_time + timedelta(minutes=minutes)
                self.end_entry.delete(0, 'end')
                self.end_entry.insert(0, new_end_time.strftime('%Y-%m-%d %H:%M'))
            except ValueError:
                messagebox.showerror("Error", "Invalid date format in start time. Please use YYYY-MM-DD HH:MM")
        else:
            messagebox.showerror("Error", "Start time must be set before incrementing end time")

    # Method to clear form entries
    def clear_entries(self):
        self.title_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.start_entry.delete(0, 'end')
        self.end_entry.delete(0, 'end')
        self.reward_var.set(self.reward_options[0])
