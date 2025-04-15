import tkinter as tk
from tkinter import messagebox

quiz_data = [
    {
        "question": "What is a growth mindset?",
        "choices": ["Believing abilities are fixed", "Believing skills can improve with effort", "Avoiding challenges", "Only focusing on natural talent"],
        "answer": "Believing skills can improve with effort"
    },
    {
        "question": "What should you do when you fail at something?",
        "choices": ["Give up", "Blame others", "Hide your failure", "Learn from failure and try again"],
        "answer": "Learn from failure and try again"
    },
    {
        "question": "Why is setting goals important?",
        "choices": ["It limits your potential", "It makes failure", "It gives direction and motivation", "It's only useful for athletes"],
        "answer": "It gives direction and motivation"
    },
    {
        "question": "Intelligence is fixed and cannot change.",
        "choices": ["True", "False"],
        "answer": "False"
    },
    {
        "question": "Revisiting your progress weekly helps stay on track.",
        "choices": ["True", "False"],
        "answer": "True"
    },
    {
        "question": "Breaking tasks into smaller steps makes them easier.",
        "choices": ["True", "False"],
        "answer": "True"
    },
    {
        "question": "How can you improve self-confidence?",
        "choices": ["Celebrating small wins", "Comparing yourself to others", "Avoiding challenges", "Focusing only on weaknesses"],
        "answer": "Celebrating small wins"
    },
    {
        "question": "Why is sleep important for learning?",
        "choices": ["It wastes time", "It helps to memorize", "It reduces focus", "It makes you lazy"],
        "answer": "It helps to memorize"
    },
    {
        "question": "Deep breathing reduces anxiety.",
        "choices": ["True", "False"],
        "answer": "True"
    },
    {
        "question": "Failure means you should give up.",
        "choices": ["True", "False"],
        "answer": "False"
    }
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Growth Mindset Quiz")
        self.current_question = 0
        self.score = 0
        
        self.question_label = tk.Label(root, text="", wraplength=400, font=("Arial", 12))
        self.question_label.pack(pady=20)
        
        self.radio_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.radio_var, value="", 
                               font=("Arial", 10), anchor='w')
            rb.pack(anchor='w', padx=20)
            self.radio_buttons.append(rb)
            
        self.feedback_label = tk.Label(root, text="", fg="red", font=("Arial", 10))
        self.feedback_label.pack(pady=10)
        
        self.next_button = tk.Button(root, text="Submit", command=self.check_answer, 
                                   font=("Arial", 10), bg="#4CAF50", fg="white")
        self.next_button.pack(pady=20)
        
        self.show_question()
    
    def show_question(self):
        self.feedback_label.config(text="")
        if self.current_question < len(quiz_data):
            question_data = quiz_data[self.current_question]
            self.question_label.config(text=f"Q{self.current_question+1}: {question_data['question']}")
            
            # Hide extra radio buttons for True/False questions
            for i in range(4):
                if i < len(question_data["choices"]):
                    self.radio_buttons[i].config(text=question_data["choices"][i], 
                                               value=question_data["choices"][i])
                    self.radio_buttons[i].pack(anchor='w', padx=20)
                else:
                    self.radio_buttons[i].pack_forget()
            
            self.radio_var.set("")
        else:
            messagebox.showinfo("Quiz Complete", 
                              f"Your score: {self.score}/{len(quiz_data)}")
            self.root.destroy()
    
    def check_answer(self):
        if not self.radio_var.get():
            self.feedback_label.config(text="Please select an answer!")
            return
            
        if self.radio_var.get() == quiz_data[self.current_question]["answer"]:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
            self.next_button.config(text="Next", command=self.next_question)
        else:
            self.feedback_label.config(text="Try again! " + quiz_data[self.current_question]["answer"], fg="red")
            self.next_button.config(text="Next", command=self.next_question)
    
    def next_question(self):
        self.current_question += 1
        self.next_button.config(text="Submit", command=self.check_answer)
        self.show_question()

root = tk.Tk()
root.geometry("500x400")
app = QuizApp(root)
root.mainloop()

