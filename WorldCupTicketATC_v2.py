from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import winsound
import ctypes


def option_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    # options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--incognito")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    options.add_experimental_option("prefs",{'credentials_enable_service': False, 'profile': {'password_manager_enabled': False}})
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return options

def OpenWeb(url, driver):
    select = None
    try:
        driver.get(url)
        sleep(0.5)
        button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Select"]')))

        if button:
            duration = 5000
            freq = 700
            winsound.Beep(freq, duration)
            ctypes.windll.user32.MessageBoxW(0, "TICKET AVAILABLE!!!!", "WARNING", 0)

            return ''
        else:
            OpenWeb(url, driver)

    except Exception as e:
        OpenWeb(url, driver)
        
        

if __name__ == '__main__':
    url = input("\nInput the URL the ticket page: ")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option_driver())
    print("Opening web page")
    driver.get(url)
    
    k = input("\nPress enter if you already login and enter the page...")

    OpenWeb(url, driver)

    k = input("\nTicket detected, please process it, and press Enter to close the browser...")