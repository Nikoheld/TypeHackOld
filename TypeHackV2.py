import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Controller
import tkinter as tk
from colorama import init, Fore, Style

init(autoreset=True)
init()

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "TypeHack")
    print(Fore.MAGENTA + Style.BRIGHT + "Made by Nikoheld" + Style.RESET_ALL)

def get_user_credentials():
    email = input("Bitte geben Sie Ihre E-Mail-Adresse ein: ")
    password = input("Bitte geben Sie Ihr Passwort ein: ")
    return email, password

def save_credentials(email, password):
    credentials = {"email": email, "password": password}
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file)

def load_credentials():
    try:
        with open('credentials.json', 'r') as file:
            credentials = json.load(file)
            return credentials['email'], credentials['password']
    except FileNotFoundError:
        return None, None

def initialize_webdriver():
    service = Service(executable_path="msedgedriver.exe")
    driver = webdriver.Edge(service=service)
    return driver

def login(driver, email, password):
    driver.get("https://at4.typewriter.at/index.php?r=typewriter/runLevel")

    input_element = driver.find_element(By.ID, "LoginForm_username")
    input_element.send_keys(email)

    input_element = driver.find_element(By.ID, "LoginForm_pw")
    input_element.clear()
    input_element.send_keys(password + Keys.ENTER)

    # Verkürze die Wartezeit auf 10 Sekunden
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-buttonset"))
    )

def start_typing(driver, keyboard):
    try:
        while True:
            # Verkürze die Wartezeit auf 5 Sekunden
            language_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div[3]/div[2]/div[2]/span[1]"))
            )
            language_text = language_element.text
            keyboard.type(language_text)
    except:
        pass

def main():
    print_banner()
    choice = input("Möchten Sie gespeicherte Anmeldedaten verwenden? (j/n): ")
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
    driver = initialize_webdriver()
    login(driver, email, password)
    root = tk.Tk()
    root.title("Start Typing")
    def start_typing_callback():
        start_button["state"] = "disabled"
        start_typing(driver, keyboard)
        start_button["state"] = "normal"
    keyboard = Controller()
    start_button = tk.Button(root, text="Start Typing", command=start_typing_callback)
    start_button.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
