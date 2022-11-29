#!/usr/bin/python3
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def skribblConnection():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument(f"--user-data-dir=C:\\Users\\bezie\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://skribbl.io/")
    driver.set_page_load_timeout(30)
    driver.maximize_window()
    return (driver)

def TryWord(driver, word):
    #select by placeholder
    try:
        inputElement = driver.find_element(By.XPATH, "//input[@placeholder='Type your guess here...']")
        inputElement.send_keys(word)
        inputElement.send_keys(Keys.ENTER)
    except:
        return
    with open("AllReadyTest.txt", "a") as f:
        f.write(word + "\n")
    return (0)

def CheckPossibilityOfWord(driver, HintWord):
    with open("WordList_EN.txt", "r") as f:
        WordList = f.read().splitlines()
    with open("AllReadyTest.txt", "r") as f:
        AlreadyList = f.read().splitlines()
    for word in WordList:
        if (len(word) == len(HintWord) and word not in AlreadyList):
            for i in range(len(word)):
                if (HintWord[i] != "_"):
                    if (word[i] != HintWord[i]):
                        break
            else:
                TryWord(driver, word)
                return
    return (0)

def CheckEnd(driver):
    Waiting = driver.find_element(By.XPATH, "//div[@class='description waiting']")
    if (Waiting.text == "WAITING"):
        with open("AllReadyTest.txt", "w") as f:
            f.write("")

def PlayGame(driver):
    print("Waiting for game to start")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button-play']"))).click()
    print("Game Started")
    while (1):
        try:
            HintWord = driver.find_elements(By.XPATH, "//div[@class='container']")
            HintWord = HintWord[1].text
            #HintWord[-1] = ""
            temp = ""
            for i in range(len(HintWord)-1):
                if (HintWord[i] == "\n"):
                    continue
                temp += HintWord[i]
            CheckPossibilityOfWord(driver, temp)
            CheckEnd(driver)
            sleep(1)
        except:
            sleep(1)
    return (driver)

def main():
    driver = skribblConnection()
    driver = PlayGame(driver)

if __name__ == "__main__":
    main()