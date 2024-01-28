import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
import time

with open('Ersteller.txt', 'w') as file:
    file.write('Made by Nikoheld')


keyboard = Controller()

filename = 'Ersteller.txt'
content = 'Made by Nikoheld'
main_file = "TypeHack.py"

if not os.path.exists(filename):
    with open(filename, 'w') as file:
        file.write(content)

    main_file = 'TypeHack.py'
    if os.path.exists(main_file):
        os.remove(main_file)

service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)

driver.get("https://at4.typewriter.at/index.php?r=typewriter/runLevel")

input_element = driver.find_element(By.ID, "LoginForm_username")
input_element.send_keys("E-Mail")

input_element = driver.find_element(By.ID, "LoginForm_pw")
input_element.clear()
input_element.send_keys("Passwort" + Keys.ENTER)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-buttonset"))
)

keyboard.press('A')
keyboard.release('A')

while 5 < 10:
    language_element = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[3]/div[2]/div[2]/span[1]")
    language_text = language_element.text

    for buchstabe in language_text:
        keyboard.press(buchstabe)
        keyboard.release(buchstabe)
        time.sleep(0.0005)

driver.quit()
