import os
import tkinter as tk
from tkinter import ttk, messagebox
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator - MIPS Assembly Backend")
        self.root.geometry("500x650")
        self.root.configure(bg='#2C3E50')
        
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.operation = None
        self.previous_value = 0
        self.radians_mode = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(main_frame, text="MIPS SCIENTIFIC CALCULATOR", 
                              font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#ECF0F1')
        title_label.pack(pady=(0, 10))
        
        # Display
        display_frame = tk.Frame(main_frame, bg='#34495E', relief='sunken', bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.display = tk.Entry(display_frame, textvariable=self.result_var, 
                               font=('Arial', 24), justify='right', 
                               bg='#1A252F', fg='#ECF0F1', bd=0, insertbackground='white')
        self.display.pack(fill=tk.X, padx=10, pady=15, ipady=8)
        
        # Mode selector
        mode_frame = tk.Frame(main_frame, bg='#2C3E50')
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        mode_label = tk.Label(mode_frame, text="Angle Mode:", 
                             bg='#2C3E50', fg='#ECF0F1', font=('Arial', 10))
        mode_label.pack(side=tk.LEFT)
        
        self.mode_var = tk.StringVar(value="DEG")
        deg_btn = tk.Radiobutton(mode_frame, text="DEG", variable=self.mode_var, 
                                value="DEG", command=self.toggle_mode, 
                                bg='#2C3E50', fg='#ECF0F1', selectcolor='#34495E',
                                font=('Arial', 10))
        deg_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        rad_btn = tk.Radiobutton(mode_frame, text="RAD", variable=self.mode_var, 
                                value="RAD", command=self.toggle_mode,
                                bg='#2C3E50', fg='#ECF0F1', selectcolor='#34495E',
                                font=('Arial', 10))
        rad_btn.pack(side=tk.LEFT, padx=(5, 10))
        
        # Status label
        self.status_label = tk.Label(mode_frame, text="Backend: Python (MIPS Ready)", 
                                   bg='#2C3E50', fg='#27AE60', font=('Arial', 9))
        self.status_label.pack(side=tk.RIGHT)
        
        # Button frames
        button_frame = tk.Frame(main_frame, bg='#2C3E50')
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scientific functions frame
        sci_frame = tk.LabelFrame(button_frame, text="Scientific Functions", 
                                 bg='#2C3E50', fg='#ECF0F1', font=('Arial', 10, 'bold'))
        sci_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        sci_buttons = [
            ['sin', 'cos', 'tan', 'log₁₀'],
            ['x²', 'x³', '√x', 'x!'],
            ['π', 'e', 'x^y', '10^x'],
            ['(', ')', 'C', 'AC']
        ]
        
        for i, row in enumerate(sci_buttons):
            for j, text in enumerate(row):
                btn = self.create_button(sci_frame, text, self.sci_button_click, i, j)
        
        # Number pad frame
        num_frame = tk.Frame(button_frame, bg='#2C3E50')
        num_frame.pack(fill=tk.BOTH, expand=True)
        
        num_buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        
        for i, row in enumerate(num_buttons):
            for j, text in enumerate(row):
                btn = self.create_button(num_frame, text, self.button_click, i, j)
    
    def create_button(self, parent, text, command, row, col):
        colors = {
            'numbers': ('#34495E', '#ECF0F1'),
            'operations': ('#E67E22', '#FFFFFF'),
            'scientific': ('#2980B9', '#FFFFFF'),
            'clear': ('#E74C3C', '#FFFFFF'),
            'equals': ('#27AE60', '#FFFFFF')
        }
        
        if text in ['C', 'AC']:
            bg, fg = colors['clear']
        elif text == '=':
            bg, fg = colors['equals']
        elif text in ['+', '-', '*', '/', 'x^y']:
            bg, fg = colors['operations']
        elif text.isdigit() or text == '.':
            bg, fg = colors['numbers']
        else:
            bg, fg = colors['scientific']
            
        btn = tk.Button(parent, text=text, font=('Arial', 12), 
                       bg=bg, fg=fg, bd=0, relief='raised',
                       command=lambda: command(text),
                       activebackground='#16A085')
        btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        return btn
    
    def toggle_mode(self):
        self.radians_mode = (self.mode_var.get() == "RAD")
        mode_text = "RADIANS" if self.radians_mode else "DEGREES"
        self.status_label.config(text=f"Mode: {mode_text} | Backend: Python (MIPS Ready)")
    
    def button_click(self, value):
        if value.isdigit() or value == '.':
            if self.current_input == "0" and value != '.':
                self.current_input = value
            else:
                self.current_input += value
            self.result_var.set(self.current_input)
        elif value in ['+', '-', '*', '/']:
            if self.current_input:
                self.previous_value = float(self.current_input)
                self.operation = value
                self.current_input = ""
                self.result_var.set(value)
        elif value == '=':
            if self.operation and self.current_input:
                current_value = float(self.current_input)
                result = self.calculate(self.previous_value, current_value, self.operation)
                self.result_var.set(str(result))
                self.current_input = str(result)
                self.operation = None
    
    def sci_button_click(self, function):
        try:
            if function in ['C', 'AC']:
                self.handle_clear(function)
            elif function in ['(', ')']:
                self.handle_parenthesis(function)
            else:
                if self.current_input:
                    value = float(self.current_input)
                    result = self.scientific_function(function, value)
                    self.result_var.set(str(result))
                    self.current_input = str(result)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.current_input = ""
            self.result_var.set("0")
    
    def handle_clear(self, function):
        if function == 'C':
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input if self.current_input else "0")
        elif function == 'AC':
            self.current_input = ""
            self.result_var.set("0")
            self.operation = None
    
    def handle_parenthesis(self, parenthesis):
        self.current_input += parenthesis
        self.result_var.set(self.current_input)
    
    def scientific_function(self, function, value):
        if function == 'sin':
            angle = math.radians(value) if not self.radians_mode else value
            return round(math.sin(angle), 10)
        elif function == 'cos':
            angle = math.radians(value) if not self.radians_mode else value
            return round(math.cos(angle), 10)
        elif function == 'tan':
            angle = math.radians(value) if not self.radians_mode else value
            return round(math.tan(angle), 10)
        elif function == 'log₁₀':
            return round(math.log10(value), 10)
        elif function == 'x²':
            return value ** 2
        elif function == 'x³':
            return value ** 3
        elif function == '√x':
            return round(math.sqrt(value), 10)
        elif function == 'x!':
            return math.factorial(int(value))
        elif function == 'π':
            return round(math.pi, 10)
        elif function == 'e':
            return round(math.e, 10)
        elif function == 'x^y':
            self.previous_value = value
            self.operation = '^'
            self.current_input = ""
            return value
        elif function == '10^x':
            return 10 ** value
        
        return value
    
    def calculate(self, a, b, operation):
        if operation == '+':
            return a + b
        elif operation == '-':
            return a - b
        elif operation == '*':
            return a * b
        elif operation == '/':
            if b == 0:
                messagebox.showerror("Error", "Division by zero!")
                return 0
            return a / b
        elif operation == '^':
            return a ** b

def main():
    print("Starting MIPS Scientific Calculator...")
    print("Backend: Python (MIPS Assembly integration ready)")
    print("To integrate MIPS backend, ensure QtSpim is installed at:")
    print(r"C:\Program Files (x86)\QtSpim\QtSpim.exe")
    print()
    
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()