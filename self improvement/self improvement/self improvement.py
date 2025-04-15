import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os
import time

class MultiAppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Toolkit")
        self.root.geometry("800x600")
        
        # Create container frame
        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Initialize frames
        self.frames = {}
        for F in (MainMenu, ChallengeApp, CountdownTimerApp, GoalTrackerApp):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainMenu)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Productivity Toolkit", font=('Arial', 16))
        label.pack(pady=20)
        
        btn1 = ttk.Button(self, text="30-Day Challenge Tracker",
                         command=lambda: controller.show_frame(ChallengeApp))
        btn1.pack(fill="x", padx=100, pady=10)
        
        btn2 = ttk.Button(self, text="Countdown Timer",
                         command=lambda: controller.show_frame(CountdownTimerApp))
        btn2.pack(fill="x", padx=100, pady=10)
        
        btn3 = ttk.Button(self, text="Goal Tracker",
                         command=lambda: controller.show_frame(GoalTrackerApp))
        btn3.pack(fill="x", padx=100, pady=10)
        
        quit_btn = ttk.Button(self, text="Exit", command=root.destroy)
        quit_btn.pack(fill="x", padx=100, pady=30)

class ChallengeApp(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=5)
        
        back_btn = ttk.Button(nav_frame, text="← Back to Menu",
                             command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(side="left", padx=5)
        
        title_label = ttk.Label(nav_frame, text="30-Day Challenge Tracker", font=('Arial', 12))
        title_label.pack(side="left", expand=True)
        
        # Challenge data
        self.challenge_name = ""
        self.start_date = None
        self.current_day = 0
        self.completed_days = []
        self.data_file = "challenge_data.json"
        
        # Load existing data
        self.load_data()
        
        # Create GUI
        self.create_widgets()
        
        # Update display
        self.update_display()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.challenge_name = data.get('challenge_name', "")
                start_date_str = data.get('start_date', "")
                if start_date_str:
                    self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                self.completed_days = data.get('completed_days', [])
                
                if self.start_date:
                    today = datetime.now().date()
                    delta = today - self.start_date
                    self.current_day = delta.days + 1
                    if self.current_day > 30:
                        self.current_day = 30
    
    def save_data(self):
        data = {
            'challenge_name': self.challenge_name,
            'start_date': self.start_date.strftime("%Y-%m-%d") if self.start_date else "",
            'completed_days': self.completed_days
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)
    
    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Challenge setup section
        setup_frame = ttk.LabelFrame(self.main_frame, text="Challenge Setup", padding="10")
        setup_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(setup_frame, text="Challenge Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(setup_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5)
        if self.challenge_name:
            self.name_entry.insert(0, self.challenge_name)
        
        ttk.Label(setup_frame, text="Start Date:").grid(row=1, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(setup_frame, width=15)
        self.date_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        if self.start_date:
            self.date_entry.insert(0, self.start_date.strftime("%Y-%m-%d"))
        
        self.setup_btn = ttk.Button(setup_frame, text="Start Challenge", command=self.setup_challenge)
        self.setup_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.main_frame, text="Challenge Progress", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="", font=('Arial', 12))
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        self.day_label = ttk.Label(progress_frame, text="", font=('Arial', 10))
        self.day_label.pack(pady=5)
        
        # Calendar frame
        self.calendar_frame = ttk.Frame(progress_frame)
        self.calendar_frame.pack(pady=10)
        
        # Mark day complete button
        self.mark_btn = ttk.Button(progress_frame, text="Mark Today as Complete", 
                                  command=self.mark_day_complete, state=tk.DISABLED)
        self.mark_btn.pack(pady=5)
        
        # Reset button
        ttk.Button(self.main_frame, text="Reset Challenge", command=self.reset_challenge).pack(pady=5)
    
    def update_display(self):
        if self.start_date:
            today = datetime.now().date()
            delta = today - self.start_date
            self.current_day = delta.days + 1
            
            if self.current_day < 1:
                self.progress_label.config(text="Challenge starts soon!")
                self.progress_bar['value'] = 0
                self.mark_btn.config(state=tk.DISABLED)
            elif self.current_day > 30:
                self.progress_label.config(text=f"Challenge completed! {len(self.completed_days)}/30 days")
                self.progress_bar['value'] = 100
                self.mark_btn.config(state=tk.DISABLED)
            else:
                self.progress_label.config(text=f"Day {self.current_day} of 30: {self.challenge_name}")
                progress = (len(self.completed_days) / 30) * 100
                self.progress_bar['value'] = progress
                
                if self.current_day not in self.completed_days:
                    self.mark_btn.config(state=tk.NORMAL)
                else:
                    self.mark_btn.config(state=tk.DISABLED)
            
            self.day_label.config(text=f"Completed days: {len(self.completed_days)}/30")
            self.update_calendar()
        else:
            self.progress_label.config(text="No active challenge")
            self.progress_bar['value'] = 0
            self.day_label.config(text="")
            self.mark_btn.config(state=tk.DISABLED)
    
    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        if not self.start_date:
            return
        
        for i in range(30):
            row = i // 7
            col = i % 7
            day_num = i + 1
            
            day_frame = ttk.Frame(self.calendar_frame, relief=tk.RIDGE, borderwidth=1)
            day_frame.grid(row=row, column=col, padx=2, pady=2)
            
            day_label = ttk.Label(day_frame, text=str(day_num), width=3)
            day_label.pack()
            
            if day_num in self.completed_days:
                day_frame.config(style='Success.TFrame')
                day_label.config(style='Success.TLabel')
            elif day_num == self.current_day and self.current_day <= 30:
                day_frame.config(style='Current.TFrame')
                day_label.config(style='Current.TLabel')
    
    def setup_challenge(self):
        name = self.name_entry.get().strip()
        date_str = self.date_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a challenge name")
            return
        
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date_str)
        
        try:
            start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return
        
        self.challenge_name = name
        self.start_date = start_date
        self.completed_days = []
        self.save_data()
        self.update_display()
        
        messagebox.showinfo("Success", f"Challenge '{name}' started on {start_date}")
    
    def mark_day_complete(self):
        if self.current_day not in self.completed_days:
            self.completed_days.append(self.current_day)
            self.completed_days.sort()
            self.save_data()
            self.update_display()
    
    def reset_challenge(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to reset the challenge?"):
            self.challenge_name = ""
            self.start_date = None
            self.completed_days = []
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.save_data()
            self.update_display()

class CountdownTimerApp(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=5)
        
        back_btn = ttk.Button(nav_frame, text="← Back to Menu",
                             command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(side="left", padx=5)
        
        title_label = ttk.Label(nav_frame, text="Countdown Timer", font=('Arial', 12))
        title_label.pack(side="left", expand=True)
        
        # Timer variables
        self.running = False
        self.remaining_time = 0
        self.end_time = 0
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Time input section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=(0, 20))
        
        ttk.Label(input_frame, text="Hours:").grid(row=0, column=0, padx=5)
        self.hours_entry = ttk.Entry(input_frame, width=5)
        self.hours_entry.grid(row=0, column=1, padx=5)
        self.hours_entry.insert(0, "0")
        
        ttk.Label(input_frame, text="Minutes:").grid(row=0, column=2, padx=5)
        self.minutes_entry = ttk.Entry(input_frame, width=5)
        self.minutes_entry.grid(row=0, column=3, padx=5)
        self.minutes_entry.insert(0, "0")
        
        ttk.Label(input_frame, text="Seconds:").grid(row=0, column=4, padx=5)
        self.seconds_entry = ttk.Entry(input_frame, width=5)
        self.seconds_entry.grid(row=0, column=5, padx=5)
        self.seconds_entry.insert(0, "0")
        
        # Timer display
        self.time_display = tk.Label(
            main_frame, 
            text="00:00:00", 
            font=("Helvetica", 48),
            fg="black"
        )
        self.time_display.pack(pady=20)
        
        # Button controls
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        self.start_button = ttk.Button(
            button_frame, 
            text="Start", 
            command=self.start_timer
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ttk.Button(
            button_frame, 
            text="Pause", 
            command=self.pause_timer,
            state=tk.DISABLED
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = ttk.Button(
            button_frame, 
            text="Reset", 
            command=self.reset_timer,
            state=tk.DISABLED
        )
        self.reset_button.grid(row=0, column=2, padx=5)
        
        self.update_display()
        
    def start_timer(self):
        if self.running:
            return
            
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            
            if hours < 0 or minutes < 0 or seconds < 0:
                raise ValueError("Negative values not allowed")
            if minutes >= 60 or seconds >= 60:
                raise ValueError("Minutes/seconds must be < 60")
                
            self.remaining_time = hours * 3600 + minutes * 60 + seconds
            
            if self.remaining_time <= 0:
                raise ValueError("Time must be greater than 0")
                
            self.end_time = time.time() + self.remaining_time
            self.running = True
            self.update_buttons()
            self.countdown()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
    
    def pause_timer(self):
        self.running = False
        self.update_buttons()
    
    def reset_timer(self):
        self.running = False
        self.remaining_time = 0
        self.update_display()
        self.update_buttons()
        self.time_display.config(fg="black")
    
    def countdown(self):
        if not self.running:
            return
            
        self.remaining_time = max(0, self.end_time - time.time())
        
        if self.remaining_time <= 0:
            self.timer_complete()
        else:
            self.update_display()
            self.after(1000, self.countdown)
    
    def timer_complete(self):
        self.running = False
        self.remaining_time = 0
        self.update_display()
        self.update_buttons()
        self.time_display.config(fg="red")
        messagebox.showinfo("Timer Complete", "The countdown has finished!")
    
    def update_display(self):
        hours = int(self.remaining_time // 3600)
        minutes = int((self.remaining_time % 3600) // 60)
        seconds = int(self.remaining_time % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_display.config(text=time_str)
    
    def update_buttons(self):
        if self.running:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            if self.remaining_time > 0:
                self.reset_button.config(state=tk.NORMAL)
            else:
                self.reset_button.config(state=tk.DISABLED)

class GoalTrackerApp(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=5)
        
        back_btn = ttk.Button(nav_frame, text="← Back to Menu",
                             command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(side="left", padx=5)
        
        title_label = ttk.Label(nav_frame, text="Goal Tracker", font=('Arial', 12))
        title_label.pack(side="left", expand=True)
        
        # Initialize data storage
        self.goals = []
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add goal section
        add_frame = ttk.LabelFrame(main_frame, text="Add New Goal")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Goal entry fields
        ttk.Label(add_frame, text="Goal:").grid(row=0, column=0, padx=5, pady=5)
        self.goal_entry = ttk.Entry(add_frame, width=40)
        self.goal_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Target Date:").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(add_frame, width=15)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Add button
        add_btn = ttk.Button(add_frame, text="Add Goal", command=self.add_goal)
        add_btn.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        
        # Goals list section
        list_frame = ttk.LabelFrame(main_frame, text="My Goals")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for goals
        columns = ("id", "goal", "date", "progress", "status")
        self.goals_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", selectmode="browse"
        )
        
        # Configure columns
        self.goals_tree.heading("id", text="ID")
        self.goals_tree.heading("goal", text="Goal")
        self.goals_tree.heading("date", text="Target Date")
        self.goals_tree.heading("progress", text="Progress")
        self.goals_tree.heading("status", text="Status")
        
        self.goals_tree.column("id", width=50, anchor=tk.CENTER)
        self.goals_tree.column("goal", width=300)
        self.goals_tree.column("date", width=100, anchor=tk.CENTER)
        self.goals_tree.column("progress", width=100, anchor=tk.CENTER)
        self.goals_tree.column("status", width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.goals_tree.yview)
        self.goals_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.goals_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        edit_btn = ttk.Button(btn_frame, text="Edit", command=self.edit_goal)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_goal)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        complete_btn = ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete)
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        update_progress_btn = ttk.Button(btn_frame, text="Update Progress", command=self.update_progress)
        update_progress_btn.pack(side=tk.LEFT, padx=5)
    
    def add_goal(self):
        goal = self.goal_entry.get()
        date = self.date_entry.get()
        
        if not goal:
            messagebox.showerror("Error", "Goal cannot be empty")
            return
            
        goal_id = len(self.goals) + 1
        self.goals.append({
            "id": goal_id,
            "goal": goal,
            "date": date,
            "progress": "0%",
            "status": "Not Started"
        })
        
        self.update_goals_list()
        self.clear_entries()
    
    def update_goals_list(self):
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)
            
        for goal in self.goals:
            self.goals_tree.insert("", tk.END, values=(
                goal["id"],
                goal["goal"],
                goal["date"],
                goal["progress"],
                goal["status"]
            ))
    
    def clear_entries(self):
        self.goal_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
    
    def edit_goal(self):
        selected = self.goals_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a goal to edit")
            return
            
        item = self.goals_tree.item(selected[0])
        goal_id = item["values"][0]
        
        goal_to_edit = next((g for g in self.goals if g["id"] == goal_id), None)
        if not goal_to_edit:
            return
            
        self.open_edit_window(goal_to_edit)
    
    def open_edit_window(self, goal):
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Goal")
        
        ttk.Label(edit_win, text="Goal:").grid(row=0, column=0, padx=5, pady=5)
        goal_entry = ttk.Entry(edit_win, width=40)
        goal_entry.grid(row=0, column=1, padx=5, pady=5)
        goal_entry.insert(0, goal["goal"])
        
        ttk.Label(edit_win, text="Target Date:").grid(row=1, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(edit_win, width=15)
        date_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        date_entry.insert(0, goal["date"])
        
        def save_changes():
            goal["goal"] = goal_entry.get()
            goal["date"] = date_entry.get()
            self.update_goals_list()
            edit_win.destroy()
            
        save_btn = ttk.Button(edit_win, text="Save", command=save_changes)
        save_btn.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
    
    def delete_goal(self):
        selected = self.goals_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a goal to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this goal?"):
            item = self.goals_tree.item(selected[0])
            goal_id = item["values"][0]
            
            self.goals = [g for g in self.goals if g["id"] != goal_id]
            self.update_goals_list()
    
    def mark_complete(self):
        selected = self.goals_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a goal")
            return
            
        item = self.goals_tree.item(selected[0])
        goal_id = item["values"][0]
        
        goal = next((g for g in self.goals if g["id"] == goal_id), None)
        if goal:
            goal["status"] = "Completed"
            goal["progress"] = "100%"
            self.update_goals_list()
    
    def update_progress(self):
        selected = self.goals_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a goal")
            return
            
        item = self.goals_tree.item(selected[0])
        goal_id = item["values"][0]
        current_progress = item["values"][3]
        
        self.open_progress_dialog(goal_id, current_progress)
    
    def open_progress_dialog(self, goal_id, current_progress):
        progress_win = tk.Toplevel(self)
        progress_win.title("Update Progress")
        
        ttk.Label(progress_win, text="Progress (%):").grid(row=0, column=0, padx=5, pady=5)
        progress_entry = ttk.Entry(progress_win, width=10)
        progress_entry.grid(row=0, column=1, padx=5, pady=5)
        progress_entry.insert(0, current_progress.replace("%", ""))
        
        def save_progress():
            try:
                progress = int(progress_entry.get())
                if progress < 0 or progress > 100:
                    raise ValueError
                    
                goal = next((g for g in self.goals if g["id"] == goal_id), None)
                if goal:
                    goal["progress"] = f"{progress}%"
                    
                    if progress == 0:
                        goal["status"] = "Not Started"
                    elif progress == 100:
                        goal["status"] = "Completed"
                    else:
                        goal["status"] = "In Progress"
                        
                    self.update_goals_list()
                    progress_win.destroy()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid percentage (0-100)")
        
        save_btn = ttk.Button(progress_win, text="Save", command=save_progress)
        save_btn.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Create custom styles
    style = ttk.Style()
    style.configure('Success.TFrame', background='lightgreen')
    style.configure('Success.TLabel', background='lightgreen')
    style.configure('Current.TFrame', background='lightblue')
    style.configure('Current.TLabel', background='lightblue')
    
    app = MultiAppLauncher(root)
    root.mainloop()