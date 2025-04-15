import tkinter as tk
from tkinter import ttk, font

class MultiAppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-App Tool")
        self.root.geometry("500x500")
        
        # Create container frame
        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Initialize frames
        self.frames = {}
        for F in (MainMenu, CalculatorApp, TranslatorApp):
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
        
        label = ttk.Label(self, text="Multi-App Tool", font=('Arial', 16))
        label.pack(pady=20)
        
        btn1 = ttk.Button(self, text="Calculator",
                         command=lambda: controller.show_frame(CalculatorApp))
        btn1.pack(fill="x", padx=100, pady=10)
        
        btn2 = ttk.Button(self, text="Myanmar-English Translator",
                         command=lambda: controller.show_frame(TranslatorApp))
        btn2.pack(fill="x", padx=100, pady=10)
        
        quit_btn = ttk.Button(self, text="Exit", command=root.destroy)
        quit_btn.pack(fill="x", padx=100, pady=30)

class CalculatorApp(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=5)
        
        back_btn = ttk.Button(nav_frame, text="← Back to Menu",
                             command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(side="left", padx=5)
        
        title_label = ttk.Label(nav_frame, text="Calculator", font=('Arial', 12))
        title_label.pack(side="left", expand=True)
        
        # Create display font
        display_font = font.Font(size=24)
        
        # Create display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = tk.Entry(
            self, 
            textvariable=self.display_var, 
            font=display_font, 
            justify="right", 
            bd=10, 
            insertwidth=2, 
            width=14, 
            borderwidth=4
        )
        self.display.pack(fill="x", padx=10, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('C', 3, 1), ('=', 3, 2), ('+', 3, 3)
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            button = tk.Button(
                button_frame, 
                text=text, 
                padx=20, 
                pady=20, 
                font=display_font,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew")
            
            # Configure button grid weights
            button_frame.grid_rowconfigure(row, weight=1)
            button_frame.grid_columnconfigure(col, weight=1)
            
        # Initialize calculator state
        self.current_input = "0"
        self.operation = None
        self.previous_value = None
        self.reset_input = False
    
    def on_button_click(self, button_text):
        if button_text.isdigit():
            self.handle_digit(button_text)
        elif button_text == 'C':
            self.handle_clear()
        elif button_text == '=':
            self.handle_equals()
        else:
            self.handle_operation(button_text)
            
        self.update_display()
    
    def handle_digit(self, digit):
        if self.current_input == "0" or self.reset_input:
            self.current_input = digit
            self.reset_input = False
        else:
            self.current_input += digit
    
    def handle_clear(self):
        self.current_input = "0"
        self.operation = None
        self.previous_value = None
    
    def handle_operation(self, op):
        if self.operation and not self.reset_input:
            self.calculate()
        self.previous_value = float(self.current_input)
        self.operation = op
        self.reset_input = True
    
    def handle_equals(self):
        if self.operation:
            self.calculate()
            self.operation = None
    
    def calculate(self):
        try:
            current_value = float(self.current_input)
            if self.operation == '+':
                result = self.previous_value + current_value
            elif self.operation == '-':
                result = self.previous_value - current_value
            elif self.operation == '*':
                result = self.previous_value * current_value
            elif self.operation == '/':
                result = self.previous_value / current_value
            
            self.current_input = str(result)
            if self.current_input.endswith('.0'):
                self.current_input = self.current_input[:-2]
        except ZeroDivisionError:
            self.current_input = "Error"
        self.reset_input = True
    
    def update_display(self):
        self.display_var.set(self.current_input)

class TranslatorApp(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=5)
        
        back_btn = ttk.Button(nav_frame, text="← Back to Menu",
                             command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(side="left", padx=5)
        
        title_label = ttk.Label(nav_frame, text="Myanmar-English Translator", font=('Arial', 12))
        title_label.pack(side="left", expand=True)
        
        # Main content frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Language selection
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill="x", pady=5)
        
        ttk.Label(lang_frame, text="From:").pack(side="left", padx=5)
        self.from_lang = ttk.Combobox(lang_frame, values=["English", "Myanmar"], state="readonly")
        self.from_lang.pack(side="left", padx=5)
        self.from_lang.current(0)
        
        ttk.Label(lang_frame, text="To:").pack(side="left", padx=5)
        self.to_lang = ttk.Combobox(lang_frame, values=["Myanmar", "English"], state="readonly")
        self.to_lang.pack(side="left", padx=5)
        self.to_lang.current(0)
        
        # Text input
        ttk.Label(main_frame, text="Input Text:").pack(anchor="w", pady=(10, 0))
        self.input_text = tk.Text(main_frame, height=5, wrap="word")
        self.input_text.pack(fill="x", pady=5)
        
        # Translate button
        translate_btn = ttk.Button(main_frame, text="Translate", command=self.translate)
        translate_btn.pack(pady=5)
        
        # Output
        ttk.Label(main_frame, text="Translation:").pack(anchor="w", pady=(10, 0))
        self.output_text = tk.Text(main_frame, height=5, wrap="word", state="disabled")
        self.output_text.pack(fill="x", pady=5)
        
        # Sample dictionary (very basic)
        self.translation_dict = {
            "english": {
                "hello": "မင်္ဂလာပါ",
                "goodbye": "ဘိုင်ဘိုင်",
                "thank you": "ကျေးဇူးတင်ပါတယ်",
                "yes": "ဟုတ်ကဲ့",
                "no": "မဟုတ်ပါ"
            },
            "myanmar": {
                "မင်္ဂလာပါ": "hello",
                "ဘိုင်ဘိုင်": "goodbye",
                "ကျေးဇူးတင်ပါတယ်": "thank you",
                "ဟုတ်ကဲ့": "yes",
                "မဟုတ်ပါ": "no"
            }
        }
    
    def translate(self):
        # Get input text
        input_txt = self.input_text.get("1.0", "end-1c").strip().lower()
        if not input_txt:
            return
        
        # Get language direction
        from_lang = self.from_lang.get().lower()
        to_lang = self.to_lang.get().lower()
        
        # Simple word-by-word translation
        translated_words = []
        for word in input_txt.split():
            if from_lang == "english":
                translated = self.translation_dict["english"].get(word, word)
            else:
                translated = self.translation_dict["myanmar"].get(word, word)
            translated_words.append(translated)
        
        # Update output
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", " ".join(translated_words))
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiAppLauncher(root)
    root.mainloop()