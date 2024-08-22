import time
from random import Random

import undetected_chromedriver as uc
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


def gen_driver():
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
        chrome_options = uc.ChromeOptions()
        # chrome_options.add_argument('--headless=new')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent={}".format(user_agent))
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
        driver = uc.Chrome(options=chrome_options, driver_executable_path=ChromeDriverManager().install())
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
                )
        return driver
    except Exception as e:
        print("Error in Driver: ", e)


time.sleep(Random().randint(1, 4))
