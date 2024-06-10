from tkinter import Tk
from schedule_app import SchedulePlannerApp
from database import create_tables

def main():
    create_tables()
    root = Tk()
    app = SchedulePlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
