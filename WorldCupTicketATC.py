from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import winsound
from selenium.webdriver.common.action_chains import ActionChains


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

def OpenWeb(url, driver, page=1, error=0):
    select = None
    try:
        driver.get(url + '&page=' + str(page))

        #https://resale-intl.fwc22.tickets.fifa.com/secured/selection/resale/item?performanceId=101437163883&productId=101397570845&lang=en
        
        try:
            if page == 1:
                pass
            else:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'page.next')))
        except Exception as e:
            OpenWeb(url, driver, page=1, error=0)

        sleep(2)
        driver.implicitly_wait(10)

        select = driver.find_elements(By.CSS_SELECTOR, 'a[title="Select"]')
        if error >= len(select):
            driver.execute_script("arguments[0].click();", select[0])
            # ActionChains(driver).move_to_element(select[0]).click(select[0]).perform()
        else:
            driver.execute_script("arguments[0].click();", select[error])
            # ActionChains(driver).move_to_element(select[error]).click(select[error]).perform()

        driver.implicitly_wait(0)
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="book"]')))
        ActionChains(driver).move_to_element(button).double_click(button).perform()
        sleep(2)

        buttonError = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="restart"]')))
        if buttonError.is_dispayed():
            if error >= len(select):
                OpenWeb(url, driver, page=page+1, error=0)
            else:
                OpenWeb(url, driver, page=page, error=error+1)
        else:
            button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="book"]')))
            if button:
                duration = 5000
                freq = 700
                winsound.Beep(freq, duration)

            return ''            

    except Exception as e:
        # print("ERROR HAPPEN" + str(e))
        if error >= len(select):
            OpenWeb(url, driver, page=page+1, error=0)
        else:
            OpenWeb(url, driver, page=page, error=error+1)
        

if __name__ == '__main__':
    url = input("\nInput the URL the ticket page: ")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option_driver())
    print("Opening web page")
    driver.get(url)
    
    k = input("\nPress enter if you already login and enter the page...")

    OpenWeb(url, driver)

    k = input("\nTicket added to cart, pleaes process the ticket and then press enter to exit...")