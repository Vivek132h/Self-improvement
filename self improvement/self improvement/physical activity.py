import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class FitnessTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker Pro")
        self.root.geometry("900x600")
        
        # Initialize data
        self.workouts = []
        self.challenges = []
        self.settings = {
            "default_location": "Gym",
            "notifications": True,
            "theme": "Light"
        }
        self.load_data()
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_workout_tab()
        self.create_challenges_tab()
        self.create_stats_tab()
        self.create_settings_tab()
        
        # Update dashboard initially
        self.update_dashboard()
    
    def load_data(self):
        """Load saved data from files"""
        try:
            if os.path.exists('workouts.json'):
                with open('workouts.json', 'r') as f:
                    self.workouts = json.load(f)
            
            if os.path.exists('challenges.json'):
                with open('challenges.json', 'r') as f:
                    self.challenges = json.load(f)
                    
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    self.settings = json.load(f)
        except:
            pass
    
    def save_data(self):
        """Save data to files"""
        with open('workouts.json', 'w') as f:
            json.dump(self.workouts, f)
        
        with open('challenges.json', 'w') as f:
            json.dump(self.challenges, f)
            
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def create_dashboard_tab(self):
        """Create the dashboard tab"""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        # Welcome label
        self.welcome_label = ttk.Label(
            self.dashboard_tab, 
            text="Your Fitness Dashboard",
            font=('Helvetica', 16, 'bold')
        )
        self.welcome_label.pack(pady=10)
        
        # Stats frame
        self.stats_frame = ttk.LabelFrame(self.dashboard_tab, text="Quick Stats")
        self.stats_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Stats labels (will be updated)
        self.workouts_count_label = ttk.Label(self.stats_frame, text="Workouts this week: 0")
        self.workouts_count_label.pack(pady=5)
        
        self.active_challenges_label = ttk.Label(self.stats_frame, text="Active challenges: 0")
        self.active_challenges_label.pack(pady=5)
        
        self.calories_burned_label = ttk.Label(self.stats_frame, text="Calories burned this month: 0")
        self.calories_burned_label.pack(pady=5)
        
        # Recent workouts frame
        self.recent_workouts_frame = ttk.LabelFrame(self.dashboard_tab, text="Recent Workouts")
        self.recent_workouts_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.recent_workouts_tree = ttk.Treeview(
            self.recent_workouts_frame, 
            columns=('Date', 'Type', 'Duration', 'Calories'),
            show='headings'
        )
        self.recent_workouts_tree.heading('Date', text='Date')
        self.recent_workouts_tree.heading('Type', text='Type')
        self.recent_workouts_tree.heading('Duration', text='Duration (min)')
        self.recent_workouts_tree.heading('Calories', text='Calories')
        
        self.recent_workouts_tree.column('Date', width=120)
        self.recent_workouts_tree.column('Type', width=120)
        self.recent_workouts_tree.column('Duration', width=120)
        self.recent_workouts_tree.column('Calories', width=120)
        
        self.recent_workouts_tree.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_workout_tab(self):
        """Create the workout logging tab"""
        self.workout_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.workout_tab, text="Log Workout")
        
        # Workout form
        self.workout_form_frame = ttk.LabelFrame(self.workout_tab, text="Log New Workout")
        self.workout_form_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Date
        ttk.Label(self.workout_form_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.workout_date_entry = ttk.Entry(self.workout_form_frame)
        self.workout_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.workout_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Workout type
        ttk.Label(self.workout_form_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.workout_type_combo = ttk.Combobox(
            self.workout_form_frame, 
            values=["Gym", "Home Workout", "Running", "Cycling", "Swimming", "Yoga", "Other"]
        )
        self.workout_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.workout_type_combo.set(self.settings.get("default_location", "Gym"))
        
        # Duration
        ttk.Label(self.workout_form_frame, text="Duration (min):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.workout_duration_entry = ttk.Entry(self.workout_form_frame)
        self.workout_duration_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Calories
        ttk.Label(self.workout_form_frame, text="Calories burned:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.workout_calories_entry = ttk.Entry(self.workout_form_frame)
        self.workout_calories_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Notes
        ttk.Label(self.workout_form_frame, text="Notes:").grid(row=4, column=0, padx=5, pady=5, sticky='ne')
        self.workout_notes_text = tk.Text(self.workout_form_frame, height=5, width=30)
        self.workout_notes_text.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        
        # Submit button
        self.submit_workout_button = ttk.Button(
            self.workout_form_frame, 
            text="Log Workout", 
            command=self.log_workout
        )
        self.submit_workout_button.grid(row=5, column=1, padx=5, pady=10, sticky='e')
        
        # Workout history
        self.workout_history_frame = ttk.LabelFrame(self.workout_tab, text="Workout History")
        self.workout_history_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.workout_history_tree = ttk.Treeview(
            self.workout_history_frame, 
            columns=('Date', 'Type', 'Duration', 'Calories', 'Notes'),
            show='headings'
        )
        self.workout_history_tree.heading('Date', text='Date')
        self.workout_history_tree.heading('Type', text='Type')
        self.workout_history_tree.heading('Duration', text='Duration (min)')
        self.workout_history_tree.heading('Calories', text='Calories')
        self.workout_history_tree.heading('Notes', text='Notes')
        
        self.workout_history_tree.column('Date', width=100)
        self.workout_history_tree.column('Type', width=100)
        self.workout_history_tree.column('Duration', width=80)
        self.workout_history_tree.column('Calories', width=80)
        self.workout_history_tree.column('Notes', width=200)
        
        self.workout_history_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate workout history
        self.update_workout_history()
    
    def create_challenges_tab(self):
        """Create the challenges tab"""
        self.challenges_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.challenges_tab, text="Challenges")
        
        # Create challenge frame
        self.create_challenge_frame = ttk.LabelFrame(self.challenges_tab, text="Create New Challenge")
        self.create_challenge_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Challenge name
        ttk.Label(self.create_challenge_frame, text="Challenge Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.challenge_name_entry = ttk.Entry(self.create_challenge_frame)
        self.challenge_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Challenge type
        ttk.Label(self.create_challenge_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.challenge_type_combo = ttk.Combobox(
            self.create_challenge_frame, 
            values=["Workout Count", "Calorie Goal", "Duration Goal", "Streak"]
        )
        self.challenge_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Target value
        ttk.Label(self.create_challenge_frame, text="Target:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.challenge_target_entry = ttk.Entry(self.create_challenge_frame)
        self.challenge_target_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Timeframe
        ttk.Label(self.create_challenge_frame, text="Timeframe (days):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.challenge_timeframe_entry = ttk.Entry(self.create_challenge_frame)
        self.challenge_timeframe_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Start date
        ttk.Label(self.create_challenge_frame, text="Start Date:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.challenge_start_date_entry = ttk.Entry(self.create_challenge_frame)
        self.challenge_start_date_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.challenge_start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Create button
        self.create_challenge_button = ttk.Button(
            self.create_challenge_frame, 
            text="Create Challenge", 
            command=self.create_challenge
        )
        self.create_challenge_button.grid(row=5, column=1, padx=5, pady=10, sticky='e')
        
        # Active challenges frame
        self.active_challenges_frame = ttk.LabelFrame(self.challenges_tab, text="Active Challenges")
        self.active_challenges_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.active_challenges_tree = ttk.Treeview(
            self.active_challenges_frame, 
            columns=('Name', 'Type', 'Target', 'Progress', 'End Date'),
            show='headings'
        )
        self.active_challenges_tree.heading('Name', text='Name')
        self.active_challenges_tree.heading('Type', text='Type')
        self.active_challenges_tree.heading('Target', text='Target')
        self.active_challenges_tree.heading('Progress', text='Progress')
        self.active_challenges_tree.heading('End Date', text='End Date')
        
        self.active_challenges_tree.column('Name', width=150)
        self.active_challenges_tree.column('Type', width=100)
        self.active_challenges_tree.column('Target', width=80)
        self.active_challenges_tree.column('Progress', width=100)
        self.active_challenges_tree.column('End Date', width=100)
        
        self.active_challenges_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate active challenges
        self.update_active_challenges()
    
    def create_stats_tab(self):
        """Create the statistics tab"""
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistics")
        
        # TODO: Add charts and detailed statistics
        ttk.Label(self.stats_tab, text="Workout Statistics (Coming Soon)", font=('Helvetica', 14)).pack(pady=20)
        
        # Placeholder for future charts
        self.stats_canvas = tk.Canvas(self.stats_tab, bg='white', height=300)
        self.stats_canvas.pack(fill='both', expand=True, padx=10, pady=5)
        self.stats_canvas.create_text(150, 150, text="Charts and graphs will appear here", fill='gray')
    
    def create_settings_tab(self):
        """Create the settings tab"""
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        # General settings frame
        self.general_settings_frame = ttk.LabelFrame(self.settings_tab, text="General Settings")
        self.general_settings_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Default workout location
        ttk.Label(self.general_settings_frame, text="Default Workout Location:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.default_location_combo = ttk.Combobox(
            self.general_settings_frame, 
            values=["Gym", "Home Workout", "Running", "Cycling", "Swimming", "Yoga", "Other"]
        )
        self.default_location_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.default_location_combo.set(self.settings.get("default_location", "Gym"))
        
        # Notifications
        self.notifications_var = tk.BooleanVar(value=self.settings.get("notifications", True))
        self.notifications_check = ttk.Checkbutton(
            self.general_settings_frame, 
            text="Enable Notifications", 
            variable=self.notifications_var
        )
        self.notifications_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        
        # Theme
        ttk.Label(self.general_settings_frame, text="Theme:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.theme_combo = ttk.Combobox(
            self.general_settings_frame, 
            values=["Light", "Dark", "System"]
        )
        self.theme_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.theme_combo.set(self.settings.get("theme", "Light"))
        
        # Save button
        self.save_settings_button = ttk.Button(
            self.general_settings_frame, 
            text="Save Settings", 
            command=self.save_settings
        )
        self.save_settings_button.grid(row=3, column=1, padx=5, pady=10, sticky='e')
    
    def log_workout(self):
        """Log a new workout"""
        date = self.workout_date_entry.get()
        workout_type = self.workout_type_combo.get()
        duration = self.workout_duration_entry.get()
        calories = self.workout_calories_entry.get()
        notes = self.workout_notes_text.get("1.0", tk.END).strip()
        
        # Validate inputs
        if not all([date, workout_type, duration]):
            messagebox.showerror("Error", "Please fill in all required fields (Date, Type, Duration)")
            return
            
        try:
            duration = float(duration)
            calories = float(calories) if calories else 0
        except ValueError:
            messagebox.showerror("Error", "Duration and Calories must be numbers")
            return
            
        # Add workout to list
        workout = {
            "date": date,
            "type": workout_type,
            "duration": duration,
            "calories": calories,
            "notes": notes
        }
        self.workouts.append(workout)
        
        # Save data
        self.save_data()
        
        # Update UI
        self.update_workout_history()
        self.update_dashboard()
        
        # Clear form
        self.workout_duration_entry.delete(0, tk.END)
        self.workout_calories_entry.delete(0, tk.END)
        self.workout_notes_text.delete("1.0", tk.END)
        
        messagebox.showinfo("Success", "Workout logged successfully!")
    
    def create_challenge(self):
        """Create a new challenge"""
        name = self.challenge_name_entry.get()
        challenge_type = self.challenge_type_combo.get()
        target = self.challenge_target_entry.get()
        timeframe = self.challenge_timeframe_entry.get()
        start_date = self.challenge_start_date_entry.get()
        
        # Validate inputs
        if not all([name, challenge_type, target, timeframe, start_date]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            target = float(target)
            timeframe = int(timeframe)
        except ValueError:
            messagebox.showerror("Error", "Target and Timeframe must be numbers")
            return
            
        # Add challenge to list
        challenge = {
            "name": name,
            "type": challenge_type,
            "target": target,
            "timeframe": timeframe,
            "start_date": start_date,
            "progress": 0
        }
        self.challenges.append(challenge)
        
        # Save data
        self.save_data()
        
        # Update UI
        self.update_active_challenges()
        self.update_dashboard()
        
        # Clear form
        self.challenge_name_entry.delete(0, tk.END)
        self.challenge_target_entry.delete(0, tk.END)
        self.challenge_timeframe_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Challenge created successfully!")
    
    def save_settings(self):
        """Save application settings"""
        self.settings["default_location"] = self.default_location_combo.get()
        self.settings["notifications"] = self.notifications_var.get()
        self.settings["theme"] = self.theme_combo.get()
        
        self.save_data()
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def update_workout_history(self):
        """Update the workout history treeview"""
        # Clear existing items
        for item in self.workout_history_tree.get_children():
            self.workout_history_tree.delete(item)
            
        # Add workouts (sorted by date, newest first)
        sorted_workouts = sorted(self.workouts, key=lambda x: x["date"], reverse=True)
        for workout in sorted_workouts:
            self.workout_history_tree.insert('', 'end', values=(
                workout["date"],
                workout["type"],
                workout["duration"],
                workout["calories"],
                workout["notes"][:50] + "..." if len(workout["notes"]) > 50 else workout["notes"]
            ))
    
    def update_active_challenges(self):
        """Update the active challenges treeview"""
        # Clear existing items
        for item in self.active_challenges_tree.get_children():
            self.active_challenges_tree.delete(item)
            
        # Add challenges
        for challenge in self.challenges:
            # Calculate end date (simple implementation)
            start_date = datetime.strptime(challenge["start_date"], "%Y-%m-%d")
            end_date = start_date + timedelta(days=challenge["timeframe"])
            
            self.active_challenges_tree.insert('', 'end', values=(
                challenge["name"],
                challenge["type"],
                challenge["target"],
                f"{challenge['progress']}/{challenge['target']}",
                end_date.strftime("%Y-%m-%d")
            ))
    
    def update_dashboard(self):
        """Update the dashboard with current stats"""
        # Workouts this week (simple count)
        workouts_this_week = len([w for w in self.workouts if self.is_this_week(w["date"])])
        self.workouts_count_label.config(text=f"Workouts this week: {workouts_this_week}")
        
        # Active challenges
        active_challenges = len(self.challenges)
        self.active_challenges_label.config(text=f"Active challenges: {active_challenges}")
        
        # Calories this month (simple sum)
        calories_this_month = sum(w["calories"] for w in self.workouts if self.is_this_month(w["date"]))
        self.calories_burned_label.config(text=f"Calories burned this month: {calories_this_month}")
        
        # Recent workouts (last 5)
        self.recent_workouts_tree.delete(*self.recent_workouts_tree.get_children())
        recent_workouts = sorted(self.workouts, key=lambda x: x["date"], reverse=True)[:5]
        for workout in recent_workouts:
            self.recent_workouts_tree.insert('', 'end', values=(
                workout["date"],
                workout["type"],
                workout["duration"],
                workout["calories"]
            ))
    
    def is_this_week(self, date_str):
        """Check if a date is in the current week (simplified)"""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            return date.isocalendar()[1] == today.isocalendar()[1] and date.year == today.year
        except:
            return False
    
    def is_this_month(self, date_str):
        """Check if a date is in the current month (simplified)"""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            return date.month == today.month and date.year == today.year
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTracker(root)
    root.mainloop()