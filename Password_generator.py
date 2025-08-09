import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import secrets
import json
from datetime import datetime

class ProfessionalPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Password Generator")
        self.root.geometry("600x500")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles for strength meter
        style.configure("Red.Horizontal.TProgressbar", background='red')
        style.configure("Yellow.Horizontal.TProgressbar", background='orange')
        style.configure("Green.Horizontal.TProgressbar", background='green')
        
        self.create_notebook()
        
    def create_notebook(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_single_tab()
        self.create_bulk_tab()
        self.create_passphrase_tab()
        self.create_settings_tab()
        
    def create_single_tab(self):
        # Single Password Generation Tab
        single_frame = ttk.Frame(self.notebook)
        self.notebook.add(single_frame, text="Single Password")
        
        # Main frame with padding
        main_frame = ttk.Frame(single_frame, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Password length
        ttk.Label(main_frame, text="Password Length:").grid(row=0, column=0, sticky='w', pady=5)
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(main_frame, from_=4, to=128, textvariable=self.length_var, width=10)
        length_spinbox.grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Character Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.use_uppercase_var = tk.BooleanVar(value=True)
        self.use_lowercase_var = tk.BooleanVar(value=True)
        self.use_numbers_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=True)
        self.avoid_ambiguous_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.use_uppercase_var).grid(row=0, column=0, sticky='w')
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.use_lowercase_var).grid(row=1, column=0, sticky='w')
        ttk.Checkbutton(options_frame, text="Numbers (0-9)", variable=self.use_numbers_var).grid(row=0, column=1, sticky='w', padx=(20, 0))
        ttk.Checkbutton(options_frame, text="Special Characters", variable=self.use_special_var).grid(row=1, column=1, sticky='w', padx=(20, 0))
        ttk.Checkbutton(options_frame, text="Avoid Ambiguous (0, O, l, I)", variable=self.avoid_ambiguous_var).grid(row=2, column=0, columnspan=2, sticky='w')
        
        # Generate button
        ttk.Button(main_frame, text="Generate Password", command=self.generate_single_password).grid(row=2, column=0, columnspan=2, pady=15)
        
        # Password display
        ttk.Label(main_frame, text="Generated Password:").grid(row=3, column=0, sticky='w', pady=5)
        self.password_var = tk.StringVar()
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)
        
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, width=50, font=('Courier', 10))
        self.password_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(password_frame, text="Copy", command=self.copy_password).pack(side='right', padx=(10, 0))
        
        # Strength meter
        strength_frame = ttk.Frame(main_frame)
        strength_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)
        
        ttk.Label(strength_frame, text="Strength:").pack(side='left')
        self.strength_meter = ttk.Progressbar(strength_frame, length=200, mode='determinate')
        self.strength_meter.pack(side='left', padx=(10, 0))
        
        self.strength_label = ttk.Label(strength_frame, text="")
        self.strength_label.pack(side='left', padx=(10, 0))
        
    def create_bulk_tab(self):
        # Bulk Password Generation Tab
        bulk_frame = ttk.Frame(self.notebook)
        self.notebook.add(bulk_frame, text="Bulk Generate")
        
        main_frame = ttk.Frame(bulk_frame, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Number of passwords
        ttk.Label(main_frame, text="Number of Passwords:").grid(row=0, column=0, sticky='w', pady=5)
        self.bulk_count_var = tk.IntVar(value=10)
        ttk.Spinbox(main_frame, from_=1, to=100, textvariable=self.bulk_count_var, width=10).grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        # Password length for bulk
        ttk.Label(main_frame, text="Password Length:").grid(row=1, column=0, sticky='w', pady=5)
        self.bulk_length_var = tk.IntVar(value=12)
        ttk.Spinbox(main_frame, from_=4, to=128, textvariable=self.bulk_length_var, width=10).grid(row=1, column=1, sticky='w', padx=(10, 0))
        
        # Generate bulk button
        ttk.Button(main_frame, text="Generate Bulk Passwords", command=self.generate_bulk_passwords).grid(row=2, column=0, columnspan=2, pady=15)
        
        # Text area for bulk passwords
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=10)
        
        self.bulk_text = tk.Text(text_frame, height=15, width=60, font=('Courier', 9))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.bulk_text.yview)
        self.bulk_text.configure(yscrollcommand=scrollbar.set)
        
        self.bulk_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons for bulk operations
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Copy All", command=self.copy_bulk_passwords).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="Save to File", command=self.save_bulk_passwords).pack(side='left')
        
        # Configure grid weights
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
    def create_passphrase_tab(self):
        # Passphrase Generation Tab
        passphrase_frame = ttk.Frame(self.notebook)
        self.notebook.add(passphrase_frame, text="Passphrase")
        
        main_frame = ttk.Frame(passphrase_frame, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Number of words
        ttk.Label(main_frame, text="Number of Words:").grid(row=0, column=0, sticky='w', pady=5)
        self.words_count_var = tk.IntVar(value=4)
        ttk.Spinbox(main_frame, from_=3, to=8, textvariable=self.words_count_var, width=10).grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        # Separator
        ttk.Label(main_frame, text="Word Separator:").grid(row=1, column=0, sticky='w', pady=5)
        self.separator_var = tk.StringVar(value="-")
        separator_combo = ttk.Combobox(main_frame, textvariable=self.separator_var, values=["-", "_", ".", " ", ""], width=10)
        separator_combo.grid(row=1, column=1, sticky='w', padx=(10, 0))
        
        # Capitalize option
        self.capitalize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Capitalize Words", variable=self.capitalize_var).grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        # Generate passphrase button
        ttk.Button(main_frame, text="Generate Passphrase", command=self.generate_passphrase).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Passphrase display
        ttk.Label(main_frame, text="Generated Passphrase:").grid(row=4, column=0, sticky='w', pady=5)
        self.passphrase_var = tk.StringVar()
        passphrase_frame_display = ttk.Frame(main_frame)
        passphrase_frame_display.grid(row=5, column=0, columnspan=2, sticky='ew', pady=5)
        
        self.passphrase_entry = ttk.Entry(passphrase_frame_display, textvariable=self.passphrase_var, width=50, font=('Courier', 10))
        self.passphrase_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(passphrase_frame_display, text="Copy", command=self.copy_passphrase).pack(side='right', padx=(10, 0))
        
    def create_settings_tab(self):
        # Settings Tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        main_frame = ttk.Frame(settings_frame, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Custom character set
        ttk.Label(main_frame, text="Custom Special Characters:").grid(row=0, column=0, sticky='w', pady=5)
        self.custom_special_var = tk.StringVar(value="!@#$%^&*()_+-=[]{}|;:,.<>?")
        ttk.Entry(main_frame, textvariable=self.custom_special_var, width=40).grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        # Save/Load settings
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save Settings", command=self.save_settings).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="Load Settings", command=self.load_settings).pack(side='left')
        
    def generate_single_password(self):
        try:
            length = self.length_var.get()
            if length < 4:
                messagebox.showerror("Error", "Password length must be at least 4")
                return
            
            characters = ""
            if self.use_lowercase_var.get():
                chars = string.ascii_lowercase
                if self.avoid_ambiguous_var.get():
                    chars = chars.replace('l', '').replace('o', '')
                characters += chars
                
            if self.use_uppercase_var.get():
                chars = string.ascii_uppercase
                if self.avoid_ambiguous_var.get():
                    chars = chars.replace('I', '').replace('O', '')
                characters += chars
                
            if self.use_numbers_var.get():
                chars = string.digits
                if self.avoid_ambiguous_var.get():
                    chars = chars.replace('0', '').replace('1', '')
                characters += chars
                
            if self.use_special_var.get():
                characters += self.custom_special_var.get()
            
            if not characters:
                messagebox.showerror("Error", "Please select at least one character type")
                return
            
            password = ''.join(secrets.choice(characters) for _ in range(length))
            self.password_var.set(password)
            self.update_strength_meter(password)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_bulk_passwords(self):
        try:
            count = self.bulk_count_var.get()
            length = self.bulk_length_var.get()
            
            self.bulk_text.delete(1.0, tk.END)
            
            for i in range(count):
                # Use same settings as single password
                characters = ""
                if self.use_lowercase_var.get():
                    characters += string.ascii_lowercase
                if self.use_uppercase_var.get():
                    characters += string.ascii_uppercase
                if self.use_numbers_var.get():
                    characters += string.digits
                if self.use_special_var.get():
                    characters += self.custom_special_var.get()
                
                if not characters:
                    messagebox.showerror("Error", "Please select at least one character type in the Single Password tab")
                    return
                
                password = ''.join(secrets.choice(characters) for _ in range(length))
                self.bulk_text.insert(tk.END, f"{i+1:3d}: {password}\n")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_passphrase(self):
        # Simple word list for demonstration
        words = ["apple", "banana", "cherry", "dragon", "elephant", "forest", "guitar", "harmony", 
                "island", "jungle", "kingdom", "lemon", "mountain", "ocean", "planet", "quartz", 
                "rainbow", "sunset", "thunder", "universe", "valley", "wonder", "xenon", "yellow", "zebra"]
        
        try:
            word_count = self.words_count_var.get()
            separator = self.separator_var.get()
            capitalize = self.capitalize_var.get()
            
            selected_words = random.sample(words, word_count)
            
            if capitalize:
                selected_words = [word.capitalize() for word in selected_words]
            
            passphrase = separator.join(selected_words)
            
            # Add some numbers for extra security
            passphrase += str(random.randint(10, 99))
            
            self.passphrase_var.set(passphrase)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_strength_meter(self, password):
        score = 0
        
        # Length scoring
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        elif len(password) >= 6:
            score += 1
        
        # Character variety
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 2
        
        # Update meter
        strength_percentage = min(100, (score / 8) * 100)
        self.strength_meter['value'] = strength_percentage
        
        if score < 3:
            self.strength_label.config(text="Weak", foreground="red")
        elif score < 6:
            self.strength_label.config(text="Moderate", foreground="orange")
        else:
            self.strength_label.config(text="Strong", foreground="green")
    
    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_var.get())
        messagebox.showinfo("Success", "Password copied to clipboard!")
    
    def copy_passphrase(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.passphrase_var.get())
        messagebox.showinfo("Success", "Passphrase copied to clipboard!")
    
    def copy_bulk_passwords(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.bulk_text.get(1.0, tk.END))
        messagebox.showinfo("Success", "All passwords copied to clipboard!")
    
    def save_bulk_passwords(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n")
                    f.write(self.bulk_text.get(1.0, tk.END))
                
                messagebox.showinfo("Success", f"Passwords saved to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def save_settings(self):
        settings = {
            'length': self.length_var.get(),
            'use_uppercase': self.use_uppercase_var.get(),
            'use_lowercase': self.use_lowercase_var.get(),
            'use_numbers': self.use_numbers_var.get(),
            'use_special': self.use_special_var.get(),
            'avoid_ambiguous': self.avoid_ambiguous_var.get(),
            'custom_special': self.custom_special_var.get()
        }
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(settings, f, indent=2)
                
                messagebox.showinfo("Success", f"Settings saved to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r') as f:
                    settings = json.load(f)
                
                # Apply settings
                self.length_var.set(settings.get('length', 12))
                self.use_uppercase_var.set(settings.get('use_uppercase', True))
                self.use_lowercase_var.set(settings.get('use_lowercase', True))
                self.use_numbers_var.set(settings.get('use_numbers', True))
                self.use_special_var.set(settings.get('use_special', True))
                self.avoid_ambiguous_var.set(settings.get('avoid_ambiguous', False))
                self.custom_special_var.set(settings.get('custom_special', "!@#$%^&*()_+-=[]{}|;:,.<>?"))
                
                messagebox.showinfo("Success", "Settings loaded successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalPasswordGenerator(root)
    root.mainloop()