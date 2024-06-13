from tkinter import messagebox, StringVar, OptionMenu, BooleanVar, Checkbutton
from tkinter import ttk
from datetime import datetime
import pygame
import os
from database import delete_activity_from_db, get_activities_from_db
from utils import generate_random_color, save_progress, load_task_colors, save_task_colors

# Custom messagebox with sound
def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

class TaskManagement:
    def __init__(self, parent, progress):
        self.parent = parent
        self.progress = progress
        self.task_colors = load_task_colors()

        self.tree_frame = ttk.Frame(self.parent)
        self.tree_frame.pack(pady=20)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        # Remove "ID" from the columns
        self.tree = ttk.Treeview(self.tree_frame, columns=("Title", "Description", "Start", "End", "Active", "Time Left", "Reward"), show='headings', yscrollcommand=self.tree_scroll.set)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Start", text="Start Time")
        self.tree.heading("End", text="End Time")
        self.tree.heading("Active", text="Is Active")
        self.tree.heading("Time Left", text="Time Left")
        self.tree.heading("Reward", text="Reward")
        self.tree.pack()

        self.tree_scroll.config(command=self.tree.yview)
        self.format_columns()

        self.load_activities()

        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(pady=10)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side="left", padx=5)
        self.clear_completed_button = ttk.Button(self.button_frame, text="Mark Completed Tasks", command=self.mark_completed_tasks)
        self.clear_completed_button.pack(side="left", padx=5)

        self.filter_var = StringVar()
        self.filter_var.set("All")
        self.filter_menu = OptionMenu(self.button_frame, self.filter_var, "All", "Active", command=self.filter_activities)
        self.filter_menu.pack(side="left", padx=5)

        self.auto_refresh = BooleanVar()
        self.auto_refresh_checkbutton = Checkbutton(self.button_frame, text="Auto Refresh", variable=self.auto_refresh)
        self.auto_refresh_checkbutton.pack(side="left", padx=5)

    def format_columns(self):
        self.tree.column("Start", width=100, anchor='center')
        self.tree.column("End", width=100, anchor='center')
        self.tree.column("Time Left", width=100, anchor='center')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree["show"] = "headings"

    def load_activities(self):
        self.filter_activities("All")

    def filter_activities(self, filter_option):
        for row in self.tree.get_children():
            self.tree.delete(row)
        activities = get_activities_from_db()
        now = datetime.now()
        for activity in activities:
            start_time = datetime.strptime(activity[3], '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(activity[4], '%Y-%m-%d %H:%M')
            is_active = "Yes" if start_time <= now <= end_time else "No"
            if filter_option == "Active" and is_active == "No":
                continue
            time_left = str(end_time - now).split('.')[0] if end_time > now else "Ended"

            task_name = activity[1]
            if task_name not in self.task_colors:
                self.task_colors[task_name] = generate_random_color()
                save_task_colors(self.task_colors)
            color = self.task_colors[task_name]

            # Insert values excluding the ID
            self.tree.insert('', 'end', values=(activity[1], activity[2], start_time.strftime('%Y-%m-%d %H:%M'), end_time.strftime('%Y-%m-%d %H:%M'), is_active, time_left, activity[5]), tags=(task_name,))
            self.tree.tag_configure(task_name, background=color)

    def delete_selected(self):
        selected_items = self.tree.selection()
        if selected_items:
            if messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(selected_items)} tasks?"):
                for item in selected_items:
                    # Get the activity ID from the hidden column (values[0])
                    activity_id = self.tree.item(item)['values'][0]
                    delete_activity_from_db(activity_id)
                    self.tree.delete(item)
                messagebox.showinfo("Success", "Activities deleted successfully!")
            else:
                messagebox.showinfo("Info", "Deletion cancelled.")
        else:
            messagebox.showerror("Error", "No task selected for deletion.")

    def mark_completed_tasks(self):
        current_year = datetime.now().year
        tasks_to_delete = []
        for item in self.tree.get_children():
            start_time = self.tree.item(item, 'values')[2]
            end_time = self.tree.item(item, 'values')[3]

            try:
                start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            except ValueError:
                start_dt = datetime.strptime(f"{current_year}-{start_time}", '%Y-%m-%d %H:%M')

            try:
                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            except ValueError:
                end_dt = datetime.strptime(f"{current_year}-{end_time}", '%Y-%m-%d %H:%M')

            now = datetime.now()

            if start_dt < now and end_dt < now:
                tasks_to_delete.append(self.tree.item(item)['values'][0])

        if tasks_to_delete:
            for task_id in tasks_to_delete:
                delete_activity_from_db(task_id)
            self.load_activities()
            self.progress['completed_tasks'] += len(tasks_to_delete)
            save_progress(self.progress)
            messagebox.showinfo("Success", "Completed tasks have been deleted successfully!")
        else:
            messagebox.showinfo("Info", "No completed tasks to delete.")
        self.update_progress_display()

    def update_progress_display(self):
        self.progress_widgets.update_progress_bars()
