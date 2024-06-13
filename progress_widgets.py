from tkinter import Label, ttk

class ProgressWidgets:
    def __init__(self, parent, progress):
        self.progress = progress

        # Create custom styles for the progress bars
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Red.Horizontal.TProgressbar", troughcolor='white', background='red')
        self.style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green')

        Label(parent, text="10000 HOURS GOAL").pack(pady=5)
        self.progress_bar = ttk.Progressbar(parent, length=500, style="Red.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=5)
        self.progress_label = Label(parent, text=f"{self.progress['completed_hours']:.2f} / 10000")
        self.progress_label.pack(pady=5)

        Label(parent, text="DAILY GOAL").pack(pady=5)
        self.daily_progress_bar = ttk.Progressbar(parent, length=500, style="Green.Horizontal.TProgressbar")
        self.daily_progress_bar.pack(pady=5)
        self.daily_progress_label = Label(parent, text=f"{self.progress['daily_completed_hours']:.2f} / 8")
        self.daily_progress_label.pack(pady=5)

        # New section for completed tasks
        Label(parent, text="COMPLETED TASKS").pack(pady=5)
        self.completed_tasks_label = Label(parent, text=f"Total Completed Tasks: {self.progress['completed_tasks']}")
        self.completed_tasks_label.pack(pady=5)

        self.update_progress_bars()

    def update_progress_bars(self):
        progress_ratio = self.progress['completed_hours'] / 10000
        self.progress_bar['value'] = progress_ratio * 100
        self.progress_label.config(text=f"{self.progress['completed_hours']:.2f} / 10000")

        daily_progress_ratio = self.progress['daily_completed_hours'] / 8
        self.daily_progress_bar['value'] = daily_progress_ratio * 100
        self.daily_progress_label.config(text=f"{self.progress['daily_completed_hours']:.2f} / 8")

        # Update completed tasks label
        self.completed_tasks_label.config(text=f"Total Completed Tasks: {self.progress['completed_tasks']}")
