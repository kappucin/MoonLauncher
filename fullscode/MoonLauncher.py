import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import subprocess
import threading
import os
import webbrowser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('icon.ico')
        self.title("Moon Launcher")
        self.geometry("600x350")
        
        # Запрет изменения размера окна
        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.play_frame = ttk.Frame(self.notebook)
        self.console_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.play_frame, text=" Играть ")
        self.notebook.add(self.console_frame, text=" Консоль ")
        self.notebook.add(self.settings_frame, text=" Настройки ")

        self.setup_play_frame()
        self.setup_console_frame()
        self.setup_settings_frame()

        self.process = None

    def setup_play_frame(self):
        self.image_label = ttk.Label(self.play_frame)
        self.image_label.pack(pady=10)

        self.load_image()

        # Загрузка и уменьшение изображений кнопок
        self.button_image = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images/button.png")).resize((214, 63), Image.LANCZOS))
        self.button_pressed_image = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "images/button_pressed.png")).resize((214, 63), Image.LANCZOS))

        self.play_button = tk.Label(self.play_frame, image=self.button_image)
        self.play_button.pack(pady=10)
        self.play_button.bind("<Button-1>", self.on_button_press)
        self.play_button.bind("<ButtonRelease-1>", self.on_button_release)

    def load_image(self):
        try:
            image_path = os.path.join(os.getcwd(), ".\\images\\image.png")  # Замените на ваш путь к изображению
            image = Image.open(image_path)
            image = image.resize((160, 160), Image.LANCZOS)  # Изменение размера до 256x256 пикселей
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
        except Exception as e:
            self.image_label.config(text=f"Не удалось загрузить изображение: {e}")

    def on_button_press(self, event):
        self.play_button.config(image=self.button_pressed_image)

    def on_button_release(self, event):
        self.run_script()

    def setup_console_frame(self):
        self.console_text = ScrolledText(self.console_frame, state='disabled', bg='black', fg='white', font=('Monospace', 10))
        self.console_text.pack(fill='both', expand=True)

    def setup_settings_frame(self):
        ttk.Label(self.settings_frame, text="Ник:").pack(pady=10)
        self.username_entry = ttk.Entry(self.settings_frame, width=50)
        self.username_entry.pack(pady=10)
        self.username_button = ttk.Button(self.settings_frame, text="Сохранить", command=self.save_username)
        self.username_button.pack(pady=10)

        self.open_folder_button = ttk.Button(self.settings_frame, text="Открыть папку игры", command=self.open_game_folder)
        self.open_folder_button.pack(pady=10)

        self.open_website_button = ttk.Button(self.settings_frame, text="Открыть сайт лаунчера", command=self.open_launcher_website)
        self.open_website_button.pack(pady=10)

        self.load_username()

    def run_script(self):
        self.console_text.config(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state='disabled')

        script_path = os.path.join(os.getcwd(), "bin", "helper.bat")
        if not os.path.exists(script_path):
            self.console_text.config(state='normal')
            self.console_text.insert(tk.END, f"Файл {script_path} не найден.\n")
            self.console_text.config(state='disabled')
            self.play_button.config(image=self.button_image)  # Reset button image
            return

        # Use CREATE_NO_WINDOW flag to prevent new console window
        creationflags = subprocess.CREATE_NO_WINDOW

        self.process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=creationflags)
        threading.Thread(target=self.read_process_output, daemon=True).start()

    def read_process_output(self):
        for line in self.process.stdout:
            self.console_text.config(state='normal')
            self.console_text.insert(tk.END, line)
            self.console_text.see(tk.END)
            self.console_text.config(state='disabled')

        for line in self.process.stderr:
            self.console_text.config(state='normal')
            self.console_text.insert(tk.END, line)
            self.console_text.see(tk.END)
            self.console_text.config(state='disabled')

        self.process.wait()
        self.play_button.config(image=self.button_image)  # Reset button image

    def load_username(self):
        username_file = os.path.join(os.getcwd(), "./settings/username.txt")
        if os.path.exists(username_file):
            with open(username_file, 'r', encoding='utf-8') as file:
                username = file.read().strip()
                self.username_entry.insert(0, username)

    def save_username(self):
        username = self.username_entry.get().strip()
        username_file = os.path.join(os.getcwd(), "./settings/username.txt")
        with open(username_file, 'w', encoding='utf-8') as file:
            file.write(username)
        self.console_text.config(state='normal')
        self.console_text.insert(tk.END, "Имя пользователя сохранено.\n")
        self.console_text.config(state='disabled')

    def open_game_folder(self):
        game_folder_path = os.path.join(os.getcwd(), "game")
        try:
            os.startfile(game_folder_path)
        except Exception as e:
            self.console_text.config(state='normal')
            self.console_text.insert(tk.END, f"Не удалось открыть папку игры: {e}\n")
            self.console_text.config(state='disabled')

    def open_launcher_website(self):
        webbrowser.open("https://kappucino.is-a.dev/moon")

if __name__ == "__main__":
    app = App()
    app.mainloop()
