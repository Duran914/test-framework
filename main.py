from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import config  # Create & populate config.py 



# output campaign info and pass/fail. (will log test to a txt later)
def initiate_test(company, campaign_type, site_id, driver="chrome", device_type="desktop", headless=False):
        driver = driver.lower()
        device_type = device_type.lower()
        available_browsers = {"chrome", "firefox", "safari"}

        if driver not in available_browsers:
                log_error({"value": f"{driver} is not valid. Please enter a valid browser"})

        if device_type != "desktop" and device_type != "mobile":
                log_error({"value": "Set device type: desktop or mobile"})

        if site_id == None:
                log_error({"value": "Enter a site id"}) #(USI)

        chrome_options = ChromeOptions()
        firefox_options = FirefoxOptions()
        global browser

        # Mobile execution (Chrome only)
        if device_type == "mobile" and driver == "chrome":
                mobile_emulation = { "deviceName": "iPhone X" } # Iphone X for now
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        elif device_type == "mobile" and driver == "firefox" or device_type == "mobile" and driver == "safari":
                log_error({"value": "Only chrome can run mobile execution"})

        # Broswer driver
        if driver == "chrome":
                # Runs broswer in headless mode
                if headless == True:
                        chrome_options.add_argument("--headless")
                        chrome_options.add_argument("--window-size=1920x1080") # Desktop execution
                browser = webdriver.Chrome(executable_path=config.chrome_driver, chrome_options=chrome_options) 

        elif driver == "firefox":
                if headless == True:
                        firefox_options.headless = True
                        firefox_options.add_argument("--window-size=1920x1080")
                browser = webdriver.Firefox(executable_path=config.firefox_driver, options=firefox_options) 

        elif driver == "safari":
                browser = webdriver.Safari(executable_path=config.safari_driver) 

        # Log script info & results
        results = f"{company} {campaign_type} {site_id}: Running..."
        print(results)


# selector validation
def check_selector(locate_by="css"):
        # Allowed locators
        allowed_locator = {"xpath", "css"}

        if locate_by not in allowed_locator:
                log_error({"value": "Enter a valid element locator"})
        else:
                pass


# Send error to console (will update to write to file)
def log_error(err):
        for err_type, message in err.items():
                if err_type == "value":
                        raise ValueError(message)
                elif err_type == "type":
                        raise TypeError(message)
                elif err_type == "name":
                        raise NameError(message)


# Navigates to url: Accepts 1 string argmuent
def navigate_url(url):
        browser.get(url)


# button click: accepts a list of css selectors
        # ['#btn', '#nextBtn']
def click_btn(buttons, locate_by="css"):
        check_selector(locate_by)
        if type(buttons) != list:
                log_error({'type':"click_btn accepts a list of selectors"})

        if locate_by == "css":
                # [browser.find_element_by_css_selector(button).click() for button in buttons]
                for button in buttons:
                       browser.find_element_by_css_selector(button).click()
                       print(f"{button} clicked!")  
        elif locate_by == "xpath":
                for button in buttons:
                        browser.find_element_by_xpath(button).click()
                        print(f"{button} clicked!")


# Input text: accepts an dict of css selector & input 
        # eg. {'#formFirstname': 'Johnny'}
def input_text(input_data, locate_by="css"):
        check_selector(locate_by)
        if type(input_data) != dict:
                log_error({'type':"input_text accepts a dictionary of selector and text"})

        if locate_by == "css":
                [browser.find_element_by_css_selector(selector).send_keys(value) for selector, value in input_data.items()]
        elif locate_by == "xpath":
                [browser.find_element_by_xpath(selector).send_keys(value) for selector, value in input_data.items()]


# Inputs email address for LC modal (USI)
        # takes email address string and optional seconds arg
def lc_input(input_email, selector="#usi_content #usi_email_container #usi_email", sec=60):
        WebDriverWait(browser, sec).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(input_email)


# Hover & button click: accepts a list of a visible element selector and non-visible selector 
        # ['#menuBar', '#dropDown a']
def hover_click_btn(visibleElement, hiddenElement, locate_by="css"):
        check_selector(locate_by)
        visibleEl = browser.find_element_by_css_selector(visibleElement)
        hiddenEl = browser.find_element_by_css_selector(hiddenElement)
        ActionChains(browser).move_to_element(visibleEl).click(hiddenEl).perform()


# Submit Button Click: Accepts css selector or default value will be used (USI)
def submit_click(selector="#usi_content .usi_submitbutton"):
        WebDriverWait(browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()


# Clicks a button when it becomes visible
def btn_click_when_visible(selector):
        WebDriverWait(browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        

# Launches Modal: No args accepted (USI)
def launch_modal():
        browser.execute_script("setTimeout( () => { usi_js.display(); }, 5000);")

# Executes any javascript code
def execute_js(script):
        browser.execute_script(script)


# Appends string url parameters
def append_url(param):
        page_url = ""
        if '?' in browser.current_url:
                page_url = browser.current_url + "&" + param
        else:
                page_url = browser.current_url + "?" + param
        navigate_url(page_url)
        print(f"Navigated to {page_url}")


# Retrieves session cookie
        #accepts a str of the cookie you want ot retrieve
def get_cookie(cookie_name):
        if browser.get_cookie(cookie_name) is None:
                print("Could not retrieve session cookie")
        else:
                cookie = browser.get_cookie(cookie_name)
                session_name = cookie["value"]
                print(f"USI session: {session_name}")


# Shuts down driver 
def shutdown():
        sleep(5)
        browser.quit()
        print("Test complete")


# Halts execution of script (last case scenario)
def halt_execution(sec):
        sleep(sec)


def take_screenshot(screenshot_name="default.png"):
        browser.save_screenshot(f"{screenshot_name}.png")


initiate_test("Office-Furniture-to-go", "TT", "24586", driver="firefox", device_type="desktop", headless=False)
navigate_url('https://www.officefurniture2go.com/')
get_cookie('shopperID')
click_btn(['#ctl00_mainPlaceHolder_hlHeroSecond', '#clearFilters a'], locate_by="css")
append_url('usi_enable=1')
input_text({"#ctl00_ucHeader_tbSearchQuery": "Testing"}, locate_by="css")
shutdown()

# initiate_test("Plp jewles", "TT", "24586", driver="chrome", device_type="desktop", headless=False)
# navigate_url("https://www.peoplesjewellers.com/wedding/engagement-rings/c/3216973")
# lc_input("testing")

