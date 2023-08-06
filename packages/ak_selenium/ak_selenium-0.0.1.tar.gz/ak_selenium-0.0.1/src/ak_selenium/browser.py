from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path
import sys

class Chrome:
    USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/83.0.4103.53 Safari/537.36'
    IMPLICITLY_WAIT_TIME = 3
    MAX_WAIT_TIME = 5

    def __init__(
            self, headless:bool = False, 
            Chrome_userdata_path:str=None, 
            half_screen:bool=True):
        self.headless = headless
        
        if not Chrome_userdata_path and sys.platform=="win32":
            Chrome_userdata_path = Path.home() / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data'
            if not Chrome_userdata_path.exists():
                Chrome_userdata_path = None
            else:
                Chrome_userdata_path = str(Chrome_userdata_path)
        self.Chrome_userdata_path = Chrome_userdata_path
        self.half_screen = half_screen
        self.s = None
        return None

    def init_chrome(self) -> webdriver.Chrome:
        """
        Initializes a Chrome web driver with specific options and configurations.
        
        Returns:
            webdriver.Chrome: The initialized Chrome driver object.
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        if self.headless:
            options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if self.Chrome_userdata_path:
            options.add_argument('--user-data-dir=' + self.Chrome_userdata_path)
        options.add_experimental_option('useAutomationExtension', False)
    
        options = _ram_optimization_browser_options(options)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=options)
        driver = self.driver

        driver.implicitly_wait(self.IMPLICITLY_WAIT_TIME) 

        driver.execute_script('window.focus()')
        driver.execute_cdp_cmd('Network.setUserAgentOverride',
                               {"userAgent": self.USERAGENT})

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
                """})

        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders",
                               {"headers": {"User-Agent": "browser1"}})

        if self.half_screen:
            size = driver.get_window_size()
            driver.set_window_size(size['width']/2, size['height'])
            driver.set_window_position(size['width']/2-13, 0)
        self.driver = driver
        return driver

    def __str__(self) -> str:
        return f"""
        Chrome.Object
        UserAgent:{self.USERAGENT}
        Implicit Wait Time: {self.IMPLICITLY_WAIT_TIME:.2f}s
        Max Wait Time: {self.MAX_WAIT_TIME:.2f}s
        Headless: {self.headless}
        Chrome Userdata Path: {self.Chrome_userdata_path}
        Half Screen View: {self.half_screen}
        """
    
    def __repr__(self) -> str:
        return f"Chrome(headless={self.headless},\
                Chrome_userdata_path={self.Chrome_userdata_path},\
                half_screen={self.half_screen})"
    
    def __del__(self) -> None:
        driver = self.driver
        try:
            driver.quit()
        except Exception as e:
            print(str(e))
        
        return None

    def Wait_for_locator(self,locator: tuple) -> None:
        (
            WebDriverWait(self.driver, self.MAX_WAIT_TIME, 0.5)
            .until(EC.presence_of_element_located(locator))
        )
        return None

    @staticmethod
    def fill_userinput_form(element, text, clear_existing=True) -> None:
        if clear_existing:
            element.clear()
        element.send_keys(text)
        
    def get_By_and_Keys(self):
        return By, Keys
    
    def init_requests(self):
        import requests
        self.s = requests.Session()
        return self.s
    
    def update_req_headers_cookies(self):
        driver = self.driver
        if not self.s:
            s = self.init_requests()
        s.cookies.update({c['name']: c['value'] for c in driver.get_cookies()})
        s.headers.update({
            "Accept-Language": driver.execute_script("return window.navigator.language;"),
            "X-Forwarded-For": driver.execute_script("return window.navigator.ip;"),
            "X-Timezone": driver.execute_script("return window.navigator.timezone;"),
            "User-Agent": driver.execute_script("return window.navigator.userAgent;"),
            "Connection": "keep-alive"
        })
        self.s = s
        return s
    
    @staticmethod
    def find_element_by_text(elements, text):
        for element in elements:
            if element.text.strip() == text:
                return element
        return None
    

def _ram_optimization_browser_options(options: Options) -> Options:
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", 
                                    ['enable-automation', "enable-logging"])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=en-US")
    return options