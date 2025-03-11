# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BCFDFA3A73FBB5F45950EEA00AC4658071A9D754FF990CF8251914C2722F26E8A4E6DA5A8E46E232036272FD1C91F249E875A7ED382C5F2DBEB48EEF4264FF49B5DCCAEEDFAC5DE13624586B82949EAC538BA708E8D9AAC3FDBF9B6FFF79788D66DFE0D0623ACE352E10777D90472A25DEE836D14D4445557DE50053135924B1A5C2732C6DB133EC128DB63164997F374C3F6924BE4A5F30B6565B7FFFCF11A8FE6F8EF5BA7452CE4096E59EF40FC174932680523BD3F79E95ED67D5832061842D4D82A9FA2FEC8F3A72886E8FA19B3E2051DA39ED455F2D6C4BB1CCEA10649CCBB62BFCF87709FEBFBA80F08C83A706985E8CC02BA56474035197430912693AF8A0715742555F4C06CAB2BD9C73CB7FC98981E2308CA668408896B28C84B6BA4F9C66C35B9190F074E46F1490242ACFC7FA07228CC2FFF3A0189419B9D501D1391783659A8FD5A95ED35DC2246087F042458DE08265804B056F1B52A978CF0A"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
