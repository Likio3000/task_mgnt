from tkinter import Label, ttk

class ProgressWidgets:
    def __init__(self, parent, progress):
        self.progress = progress

        Label(parent, text="OVERALL GOAL").pack(pady=5)
        self.progress_bar = ttk.Progressbar(parent, length=500)
        self.progress_bar.pack(pady=5)
        self.progress_label = Label(parent, text=f"{self.progress['completed_hours']:.2f} / 10000")
        self.progress_label.pack(pady=5)

        Label(parent, text="DAILY GOAL").pack(pady=5)
        self.daily_progress_bar = ttk.Progressbar(parent, length=500)
        self.daily_progress_bar.pack(pady=5)
        self.daily_progress_label = Label(parent, text=f"{self.progress['daily_completed_hours']} / 8")
        self.daily_progress_label.pack(pady=5)

        self.update_progress_bars()

    def update_progress_bars(self):
        progress_ratio = self.progress['completed_hours'] / 10000
        self.progress_bar['value'] = progress_ratio * 100
        self.progress_label.config(text=f"{self.progress['completed_hours']:.2f} / 10000")

        daily_progress_ratio = self.progress['daily_completed_hours'] / 8
        self.daily_progress_bar['value'] = daily_progress_ratio * 100
        self.daily_progress_label.config(text=f"{self.progress['daily_completed_hours']} / 8")
