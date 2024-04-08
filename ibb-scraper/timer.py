import datetime
import time
import runpy
import read_config1 as read_config
from login2site import run_scraper1  # login2site.py'den fonksiyonu içe aktar
from book import run_scraper2  # book.py'den fonksiyonu içe aktar

# Example usage
config_file_path = 'data/config.json'
tc, password, link, timeslot, plus, timer_hms = read_config.read_config(config_file_path)
target_hour, target_minute, target_second = timer_hms #hedef zamanı tnanımla
print(timer_hms)

driver = run_scraper1()

while True:
    # Şu anki zamanı al
    now = datetime.datetime.now()
    print("now:", now)
    # Hedef zamana ulaşıp ulaşmadığını kontrol et
    if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_minute and now.second >= target_second):
        # Fonksiyonu çalıştır
        print("run book.py")
        run_scraper2(driver)
        # Bir sonraki tam saniyeye kadar bekle
        break
    else:
        # Hedef zamana henüz ulaşılmadıysa, bir sonraki tam saniyeye kadar bekle
        time.sleep(1 - (time.time() % 1))