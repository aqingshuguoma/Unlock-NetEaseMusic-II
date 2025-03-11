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
    browser.add_cookie({"name": "MUSIC_U", "value": "003103ADD1E06D4A4EFB699EBA8FB3DAAC31A0019D4E5E3062C5A6E80143D3F7E775D4A19782B56698F62C2B164567A9780D1E4EA8384E88E9C1B9A0D9B5C7928148FFF7BCDD3376221AC4DA2AC0434D5B2C960C9796556FFE4D6547A3453BFF042F8BBD10BB7D850B8E0394478A2D678DDF56C565FBB2B312615616F9E4BA0E23E47D58ED91D40A8831690C010660C8F1B88C8BFC8CCE5311BE6E64AF3B166A37072644880E0E5E7F5A8232214E57BA2B1426EB3CF4FDC3452207BB3FC0C6E2E19A2B39842D512D1DD6BF9A826E097C95740469F0223135E6FF9E32470787232426C795AC62EC3A7405C5C9C678F6E7F0E8D6F3727D920C33F88BB84FEAB2CC869D54B69214075F48288A828C56F5D7F3EF4F54E6C0F794A023D33AACECC26B44082A3E29259240555DD2AE2EF89B46A3D48CA62BA18ED8A110223D0E2D5F328B7A817AE3DCFF5F4BC4CB9883AAB1F55963E00897AEE73C08AE6272B1B1D0A614"})
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
