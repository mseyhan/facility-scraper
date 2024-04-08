# login2site.PY

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import date, datetime, timedelta
import read_config1 as read_config
from time import sleep
import pickle
import datetime
import runpy

# Function to initialize the driver
def init_driver():
    chrome_options = uc.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--headless")
    driver = uc.Chrome(options=chrome_options)
    return driver

# Function to perform login
def login(driver, tc, password, link):
    driver.get(link)
    print("siteye girdi.")
    driver.find_element(By.XPATH, "//*[@id='txtTCPasaport']").send_keys(tc)
    driver.find_element(By.XPATH, "//*[@id='txtSifre']").send_keys(password)
    driver.find_element(By.XPATH, "//*[@id='cboxBeniHatirla']").click()
    driver.find_element(By.XPATH, "//*[@id='btnGirisYap']").click()
    print("credential'lar girildi.")

# Main function to run SCRAPER1
def run_scraper1():
    start = datetime.datetime.now()
    print(start)

    # Read configuration
    config_file_path = 'data/config.json'
    tc, password, link, timeslot, plus, timer_hms, bransadi, tesisadi, salonadi = read_config.read_config(config_file_path)
    
    today_plus = date.today() + timedelta(days=plus)
    today_plus_str = today_plus.strftime("%d.%m.%Y")

    if tc and password:
        print(f"TC: {tc}")
        print(f"Password: {password}")
        print(f"Link: {link}")
        print(f"Timeslot: {timeslot}")
        print(f"For date: {today_plus_str}")

    driver = init_driver()
    login(driver, tc, password, link)

    # Add any additional steps you want to perform in SCRAPER1 here
    sleep(3)
    #CLICK ANYWHERE
    # JavaScript to calculate the middle of the viewport and click
    js_script = """
    // Calculate middle of the viewport
    const x = window.innerWidth / 2;
    const y = window.innerHeight / 2;

    // Create a mouse click event
    const clickEvent = new MouseEvent('click', {
        'view': window,
        'bubbles': true,
        'cancelable': true,
        'clientX': x,
        'clientY': y
    });

    // Dispatch the event on the element at the calculated position
    document.elementFromPoint(x, y).dispatchEvent(clickEvent);
    """

    # Execute the JavaScript
    driver.execute_script(js_script)

    sleep(3)

    # kiralama hizmetleri kısmına tıklar
    kiralamahizm = '//*[@id="form1"]/div[3]/div[2]/div/div/ul/li[3]/a'
    driver.find_element(By.XPATH, kiralamahizm).click()
    print("kiralama tıkladı")

    wait = WebDriverWait(driver, 10)

    # BRANS
    brans_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlBransFiltre")))
    Select(brans_dropdown).select_by_visible_text(bransadi)
    print("Branş seçildi.")
    sleep(1)

    #TESİS
    tesis_dropdown = wait.until(
        EC.visibility_of_element_located((
            By.XPATH, f"//option[contains(text(), '{tesisadi}')]")))
    tesis_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ddlTesisFiltre")))
    Select(tesis_dropdown).select_by_visible_text(tesisadi)
    print("tesis secildi")

    # Return the driver for further use in SCRAPER2
    end = datetime.datetime.now()
    duration = end - start
    print(f"login2site.py completed in {duration}.")
    return driver

# If this script is run directly, execute run_scraper1
if __name__ == "__main__":
    driver = run_scraper1()
    # You might want to close the driver or pass it to another script here
