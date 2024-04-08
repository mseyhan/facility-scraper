# SCRAPER2.PY

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
from datetime import datetime, timedelta
import read_config1 as read_config
from time import sleep

# Assuming read_config.py is correctly set up to return configuration values
config_file_path = 'data/config.json'
tc, password, link, timeslot, plus, timer_hms, bransadi, tesisadi, salonadi = read_config.read_config(config_file_path)

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# Function to select options and navigate in the web application
def continue_scraping(driver):
    start = datetime.now()
    #print(start)
    today_plus = datetime.today() + timedelta(days=plus)
    today_plus_str = today_plus.strftime("%d.%m.%Y")
    #print(f"Looking for date: {today_plus_str}")
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.visibility_of_element_located((
            By.XPATH, f"//option[contains(text(), '{salonadi}')]")))
    salon_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlSalonFiltre")))
    Select(salon_dropdown).select_by_visible_text(salonadi)
    print("Salon seçildi.")
    #sleep(.3)
    # en aşağı scroll'la, bulsun diye
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 3 gün sonrayı bulsun
    #print()
    target_date_container = None
    try:
        target_date_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h3[contains(., '{today_plus_str}')]/ancestor::div[@class='panel panel-info']"))
        )
        print("Date container found.")
    except TimeoutException:
        print(f"Date container for {today_plus_str} not found.")
        return  # Exit the function if the date container is not found
    
    driver.execute_script("arguments[0].scrollIntoView(true);", target_date_container)

    # Trying to find the time slot
    try:
        time_slot_xpath = f".//span[contains(@class, 'lblStyle') and contains(text(), '{timeslot}')]"
        time_slot_element = WebDriverWait(target_date_container, 10).until(
            EC.visibility_of_element_located((By.XPATH, time_slot_xpath))
        )
        print(f"Time slot {timeslot} found.")

        # Scroll to the time slot
        driver.execute_script("arguments[0].scrollIntoView(true);", time_slot_element)

        # Find and click the reservation button
        rezButtonXpath = ".//a[contains(text(), 'Rezervasyon') and contains(@class, 'btn-danger')]"
        reservation_button = WebDriverWait(time_slot_element, 10).until(
            EC.element_to_be_clickable((By.XPATH, rezButtonXpath))
        )
        reservation_button.click()
        print("Reservation button clicked.")

    except TimeoutException:
        print(f"Time slot {timeslot} or reservation button not found.")
        return  # Exit the function if the time slot or reservation button is not found

    # Handle alert
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert accepted.")
    except TimeoutException:
        print("No alert appeared after reservation button click.")



    #print("skrollandı baby.")
    #print("tıklamalara geçiliyor")
    #sleep(.2)
    try:
        kortkirala = '''//*[@id="rblKiralikTenisSatisTuru"]/tbody/tr[3]/td/label'''
        wait.until(EC.element_to_be_clickable((By.XPATH, kortkirala))).click()
        print("kort kiralama seçildi")
        #sleep(.3)
        kiraliksoz = '''//*[@id="pageContent_dvSepet"]/p[2]/span/label'''
        wait.until(EC.element_to_be_clickable((By.XPATH, kiraliksoz))).click()
        print("sözleşme kabul edildi")
        #sleep(.3)
        sepete_ekle = '''//*[@id="pageContent_lbtnSepeteEkle"]'''
        wait.until(EC.element_to_be_clickable((By.XPATH, sepete_ekle))).click()
        print("sepete eklendi.")
    except Exception as e:
        print("Bir elementin görünür olmasını beklerken zaman aşımına uğradı.",e)

    print("cycle done.")
    # Calculate and print the duration
    end = datetime.now()
    duration = end - start
    print(f"book.py completed in {duration}.")

# This function would be called from the notebook or another script, passing the driver from SCRAPER1
def run_scraper2(driver):
    continue_scraping(driver)

# If you need to test SCRAPER2 directly, you might temporarily include code to initialize the driver here
# and then call run_scraper2(driver). Remember to remove or comment out this test code when integrating with SCRAPER1.
