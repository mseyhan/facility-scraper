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
    date_containers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'panel-heading')))
    #print()
    print('date_container bulundu, uzunluğu:', len(date_containers))
    #sleep(.1)
    target_date_container = None
    for container in date_containers:
        print("today plus:",today_plus_str)
        print("containerınkendisi:",container.text)
        if today_plus_str in container.text:
            target_date_container = container.find_element(By.XPATH, './..')  # Navigate to parent container
            break
    print("parent'a gidildi")



    if target_date_container:
        #sleep(.2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Within this container, find the specified time slot
        time_slots = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lblStyle')))
        print(timeslot, "timeslot'a bakılıyor.")
        for slot_element in time_slots:
            slot_text = slot_element.text.strip()  # strip() removes any extra whitespace
            if timeslot == slot_text:
                print("Found the slot:", slot_text)
                
                
                # Navigate to parent container of the slot, which should also contain the reservation button
                target_time_slot_container = slot_element.find_element(By.XPATH, './ancestor::div[contains(@class, "well")]')#.find_element(By.XPATH,rezButtonXpath)
                print("target time slot container:",target_time_slot_container.get_attribute('innerHTML'))

                # Find the 'Rezervasyon' button for this time slot
                rezButtonXpath = ".//a[contains(text(), 'Rezervasyon') and contains(@class, 'btn-danger')]"
                #rezervasyon_button = target_time_slot_container.find_element(By.XPATH, ".//a[contains(text(), 'Rezervasyon') and contains(@class, 'btn-danger')]")
                sleep(1)
                element = WebDriverWait(target_time_slot_container, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, rezButtonXpath)))
                print("element found:", element.get_attribute('innerHTML'))
                try:
                    # Attempt to click the reservation button
                    element.click()
                    print("Rezervasyon button clicked.")
                    
                    # Wait for the alert to be present and then accept it
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    print(f"Alert found with text: {alert_text}")
                    alert.accept()
                    print("Alert accepted")
                except TimeoutException:
                    print("No alert appeared after clicking the reservation button.")
                except UnexpectedAlertPresentException as e:
                    # Handle the unexpected alert
                    alert = driver.switch_to.alert
                    alert.accept()
                    print(f"Unexpected alert handled: {e.alert_text}")

                break
        else:

            print(f"Time slot {timeslot} not found.")
    else:
        print(f"Date {today_plus_str} not found.")




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
