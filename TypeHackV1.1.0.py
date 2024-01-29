import json
import sys
import threading
import tkinter as tk
from tkinter import ttk
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Controller
from colorama import init, Fore, Style

init(autoreset=True)
init()


class TypeHackApp:
    def __init__(self):
        self.root = None
        self.stop_flag = threading.Event()
        self.driver = None
        self.keyboard = Controller()
        self.start_button = None
        self.quit_button = None
        self.panic_button = None
        self.speed_scale = None
        self.speed_label = None
        self.min_speed = 0.0000001  # Mindestgeschwindigkeit
        self.max_speed = 4.0  # Maximale Geschwindigkeitsstufe
        self.num_speeds = 10  # Anzahl der Geschwindigkeitsstufen

    def create_widgets(self):
        self.root = tk.Tk()
        self.root.title("TypeHack")

        self.start_animation_label = tk.Label(self.root, text="", font=("Arial", 20), fg="white", bg="black")
        self.start_animation_label.pack()

        self.start_button = tk.Button(self.root, text="Start Typing", command=self.start_typing_callback)
        self.start_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_callback)  # Quit-Button immer verfügbar
        self.quit_button.pack()

        self.panic_button = tk.Button(self.root, text="Panic!", command=self.panic_button_callback, state="disabled")
        self.panic_button.pack()

        self.language_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.language_label.pack()

        # Schieberegler für die Geschwindigkeit
        self.speed_label = tk.Label(self.root, text="Geschwindigkeit:")
        self.speed_label.pack()

        self.speed_scale = ttk.Scale(self.root, from_=self.min_speed, to=self.max_speed, length=200, orient="horizontal", command=self.update_speed_label)
        self.speed_scale.set(self.min_speed)  # Startwert für Geschwindigkeitsstufe 1
        self.speed_scale.pack()

        self.speed_label_display = tk.Label(self.root, text="")
        self.speed_label_display.pack()

        self.ad_label = tk.Label(self.root, text="Made by Nikoheld", font=("Arial", 8), foreground="gray")
        self.ad_label.pack(side=tk.BOTTOM)

        self.root.protocol("WM_DELETE_WINDOW", self.quit_callback)

    def update_speed_label(self, value):
        speed_level = int((float(value) - self.min_speed) / ((self.max_speed - self.min_speed) / (self.num_speeds - 1)) + 1)
        self.speed_label_display.config(text=f"Geschwindigkeitsstufe: {speed_level}")

    def start_typing_callback(self):
        if not self.stop_flag.is_set():
            self.stop_flag.set()
            self.start_button["text"] = "Start Typing"
            self.quit_button["state"] = "normal"
            self.panic_button["state"] = "normal"
        else:
            self.stop_flag.clear()
            self.start_button["text"] = "Stop Typing"
            self.quit_button["state"] = "disabled"
            self.panic_button["state"] = "normal"
            threading.Thread(target=self.start_typing, daemon=True).start()
            self.root.focus_set()  # Das Tkinter-Fenster in den Vordergrund bringen

    def quit_callback(self):
        self.stop_flag.set()
        if self.driver:
            self.driver.quit()
        self.root.destroy()
        sys.exit(0)

    def panic_button_callback(self):
        self.stop_flag.set()
        sys.exit(0)

    def initialize_webdriver(self):
        service = Service(executable_path="msedgedriver.exe")
        driver = webdriver.Edge(service=service)
        return driver

    def login(self, email, password):
        self.driver.get("https://at4.typewriter.at/index.php?r=typewriter/runLevel")

        input_element = self.driver.find_element(By.ID, "LoginForm_username")
        input_element.send_keys(email)

        input_element = self.driver.find_element(By.ID, "LoginForm_pw")
        input_element.clear()
        input_element.send_keys(password + Keys.ENTER)

        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-buttonset"))
        )

    def start_typing(self):
        try:
            while not self.stop_flag.is_set():
                language_element = WebDriverWait(self.driver, 1000).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div[3]/div[2]/div[2]/span[1]"))
                )
                language_text = language_element.text

                # Führe UI-Aktionen im Hauptthread aus
                self.root.after(0, lambda: self.language_label.config(text=language_text))
                self.root.after(0, lambda: self.root.attributes('-topmost', True))
                self.root.after(0, lambda: self.root.update_idletasks())
                self.root.after(0, lambda: self.root.attributes('-topmost', False))
                self.root.focus_set()  # Das Tkinter-Fenster in den Vordergrund bringen

                self.keyboard.type(language_text)

                # Dynamische Wartezeit basierend auf der Geschwindigkeit
                speed = self.speed_scale.get()  # Geschwindigkeit aus dem Schieberegler

                if speed > self.min_speed:
                    time.sleep(speed)
                else:
                    # Markiere die Linie rot, wenn die langsamste Geschwindigkeitsstufe erreicht ist
                    self.root.after(0, lambda: self.language_label.config(fg="red"))

            # Nachdem das Schreiben abgeschlossen ist, aktiviere den "Start Typing" Button
            self.root.after(0, lambda: self.start_button.invoke())
        except (TimeoutError, KeyboardInterrupt) as e:
            print(f"An error occurred: {e}")
            raise

    def start_animation(self, text, index=0):
        if index < len(text):
            current_text = self.start_animation_label["text"]
            self.start_animation_label.config(text=current_text + text[index])
            self.root.after(100, lambda: self.start_animation(text, index + 1))
        else:
            # Nach der Animation aktiviere den "Start Typing" Button
            self.root.after(500, lambda: self.start_button.invoke())


def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            data = json.load(file)
            email = data.get("email")
            password = data.get("password")
            return email, password
    except FileNotFoundError:
        return None, None


def get_user_credentials():
    email = input("Bitte geben Sie Ihre E-Mail-Adresse ein: ")
    password = input("Bitte geben Sie Ihr Passwort ein: ")
    return email, password


def save_credentials(email, password):
    credentials = {"email": email, "password": password}
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)


def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "TypeHack")
    print(Fore.MAGENTA + Style.BRIGHT + "Made by Nikoheld" + Style.RESET_ALL)


def main():
    print_banner()
    choice = input("Möchten Sie gespeicherte Anmeldedaten verwenden? (j/n): ")

    app = TypeHackApp()

    if choice.lower() == 'j':
        email, password = load_credentials()
        if email is None or password is None:
            print("Keine gespeicherten Anmeldedaten gefunden.")
            return
    elif choice.lower() == 'n':
        email, password = get_user_credentials()
        save_credentials(email, password)
    else:
        print("Ungültige Eingabe. Programm wird beendet.")
        return

    print("Initialisiere WebDriver...")
    app.driver = app.initialize_webdriver()
    print("Login...")
    app.login(email, password)
    print("Erstelle Tkinter-Fenster...")
    app.create_widgets()
    print("Starte Startanimation...")
    app.start_animation("TypeHack")

    app.root.attributes('-topmost', True)

    print("Starte Tkinter Mainloop...")
    app.root.mainloop()


if __name__ == "__main__":
    main()
