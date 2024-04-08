# scraper dependencies
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from time import sleep
import pickle
from datetime import date
from datetime import datetime
import datetime
import runpy
import read_config

start = datetime.datetime.now()
print(start)

today_plus = date.today() + datetime.timedelta(days=read_config.plus)
today_plus = today_plus.strftime("%d.%m.%Y")

if read_config.tc and read_config.password:
    print(f"TC: {read_config.tc}")
    print(f"Password: {read_config.password}")
    print(f"Link: {read_config.link}")
    print(f"Timeslot: {read_config.timeslot}")
    print(f"For date: {today_plus}")

# driver execution and rules for better performance
chromeOptions = uc.ChromeOptions()
chromeOptions.add_argument('--blink-settings=imagesEnabled=false')
#chromeOptions.add_argument("--headless")  # Enable headless mode
chromeOptions.add_argument("--disable-gpu")  # Recommended when running headless
chromeOptions.add_argument("--window-size=1920,1080")  # Specify window size

driver = uc.Chrome(options=chromeOptions)

wait = WebDriverWait(driver, 10)  # Adjust the timeout according to your needs

driver.get(read_config.link) # siteye giriş
print("siteye girdi.")

# credential'ları gir
tcelem = driver.find_element(By.XPATH, "//*[@id='txtTCPasaport']").send_keys(read_config.tc)
passelem = driver.find_element(By.XPATH, "//*[@id='txtSifre']").send_keys(read_config.password)
benihatir = driver.find_element(By.XPATH, "//*[@id='cboxBeniHatirla']").click()
loginbutt = driver.find_element(By.XPATH, "//*[@id='btnGirisYap']").click()

print("credential'lar girildi.")
sleep(.2)
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


# kiralama hizmetleri kısmına tıklar
kiralamahizm = '//*[@id="form1"]/div[3]/div[2]/div/div/ul/li[3]/a'
driver.find_element(By.XPATH, kiralamahizm).click()
print("kiralama tıkladı")

##########################
# BRANŞ seç
bransdropdown = driver.find_element(By.ID, "ddlBransFiltre")
selectbrans = Select(bransdropdown)
selectbrans.select_by_visible_text("TENİS")
print("branş seçildi")
sleep(.5)

# Select "MALTEPE SAHİL SPOR TESİSİ" from the tesis dropdown
tesisdropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlTesisFiltre")))
Select(tesisdropdown).select_by_visible_text("MALTEPE SAHİL SPOR TESİSİ")
print("tesis seçildi")
sleep(.5)
# salon seç
salondd = wait.until(EC.element_to_be_clickable((By.ID, "ddlSalonFiltre")))
#salondd = driver.find_element(By.ID, "ddlSalonFiltre")
#selectsalon = Select(salondd)
#selectsalon.select_by_visible_text("KAPALI TENIS KORTU 3")
#selectsalon.select_by_visible_text("AÇIK TENIS KORTU")
Select(salondd).select_by_visible_text("AÇIK TENIS KORTU")

print("salon seçildi")



#sleep(1.5)
# en aşağı scroll'la, bulsun diye
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("aşağı scrollke")


print(today_plus)
# 3 gün sonrayı bulsun
date_xpath = f"//*[contains(@class, 'panel-heading') and contains(text(), '{today_plus}')]"
print(date_xpath)

#target_date_container = wait.until(EC.visibility_of_element_located((By.XPATH, date_xpath + "/..")))

date_containers = driver.find_elements(By.CLASS_NAME, 'panel-heading')
target_date_container = None
for container in date_containers:
    if today_plus in container.text:
        target_date_container = container.find_element(By.XPATH, './..')  # Navigate to parent container
        break

# Check if the target date container was found
if target_date_container:
    print("Found the target date container.")
    # Find the specific time slot within this container
    time_slot_xpath = f".//*[contains(@class, 'lblStyle') and contains(text(), '{read_config.timeslot}')]"
    try:
        target_time_slot = target_date_container.find_element(By.XPATH, time_slot_xpath + "/..")
        print("Found the target time slot container.")
        # Click the 'Rezervasyon' button within this slot
        rezervasyon_button = target_time_slot.find_element(By.XPATH, ".//a[contains(text(), 'Rezervasyon')]")
        rezervasyon_button.click()
        print("Clicked the 'Rezervasyon' button.")
    except Exception as e:
        print(f"Could not find or click the 'Rezervasyon' button: {e}")
else:
    print(f"Date '{today_plus}' not found.")

# Handle the alert if it appears
try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    print("Alert found and accepted.")
except Exception as e:
    print(f"No JavaScript alert found: {e}")

# Click other elements like 'Kort Kirala', 'Kiralık Sözleşmesi', and 'Sepete Ekle'
try:
    kortkirala_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='rblKiralikTenisSatisTuru']/tbody/tr[3]/td/label")))
    kortkirala_button.click()
    kiraliksoz_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent_dvSepet']/p[2]/span/label")))
    kiraliksoz_checkbox.click()
    sepete_ekle_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent_lbtnSepeteEkle']")))
    sepete_ekle_button.click()
    print("Successfully clicked 'Kort Kirala', 'Kiralık Sözleşmesi', and 'Sepete Ekle'.")
except Exception as e:
    print(f"Error interacting with one of the final buttons: {e}")

# Calculate and print the duration
end = datetime.datetime.now()
print(f"it took {end-start} seconds")