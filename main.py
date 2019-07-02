from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from config import browser # populate config.py 


# selector validation
def check_selector(locate_by="css"):
        # Allowed locators
        allowed_locator = {"xpath", "css"}

        if locate_by == "" or locate_by not in allowed_locator:
                return False
        else:
                return True

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
        if check_selector(locate_by):
                # if locate_by == "" or locate_by not in allowed_locator:
                #         raise ValueError("Enter a valid element locator")
                # else:
                if locate_by == "css":
                        [browser.find_element_by_css_selector(button).click() for button in buttons]
                elif locate_by == "xpath":
                        [browser.find_element_by_xpath(button).click() for button in buttons]
        elif check_selector(locate_by) == False:
                log_error({"value": "Enter a valid element locator"})
        

# Input text: accepts an dict of css selector & input 
        # eg. {'#formFirstname': 'Johnny'}
def input_text(inputData, locate_by="css"):
        # if locate_by == "" or locate_by not in allowed_locator:
        #         raise ValueError("Enter a valid element locator")
        # else:
        if check_selector(locate_by):
                if locate_by == "css":
                        [browser.find_element_by_css_selector(selector).send_keys(value) for selector, value in inputData.items()]
                elif locate_by == "xpath":
                        [browser.find_element_by_xpath(selector).send_keys(value) for selector, value in inputData.items()]
        elif check_selector(locate_by) == False:
                log_error({"value": "Enter a valid element locator"})
        # [browser.find_element_by_css_selector(selector).send_keys(value) for selector, value in inputData.items()]


# Hover & button click: accepts a list of a visible element selector and non-visible selector 
        # ['#menuBar', '#dropDown a']
def hover_click_btn(visibleElement, hiddenElement, locate_by="css"):
        visibleEl = browser.find_element_by_css_selector(visibleElement)
        hiddenEl = browser.find_element_by_css_selector(hiddenElement)
        ActionChains(browser).move_to_element(visibleEl).click(hiddenEl).perform()

# Submit Button Click: Accepts css selector or default value will be used
def submit_click(selector="#usi_content .usi_submitbutton"):
        WebDriverWait(browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        
# Launches Modal: No args accepted 
def launch_modal():
        browser.execute_script("setTimeout( () => { usi_js.display(); }, 5000);")

# Appends string url parameters
def enable_url(param):
        page_url = ""
        if '?' in browser.current_url:
                page_url = browser.current_url + "&" + param
        else:
                page_url = browser.current_url + "?" + param
        navigate_url(page_url)
        print(page_url)

# Retrieves session cookie
def get_session_cookie():
        if browser.get_cookie('usi_sess') is None:
                print("Could not retrieve session cookie")
        return "USI session :" + browser.get_cookie('usi_sess')

# Shuts down driver 
def shutdown():
        browser.quit()

# Halts execution of script (last case scenario)
def halt_execution(sec):
        sleep(sec)

navigate_url('https://www.officefurniture2go.com/')
click_btn(['#ctl00_mainPlaceHolder_hlHeroSecond', '#clearFilters a'], locate_by="css")
input_text({'#ctl00_ucHeader_tbSearchQuery': "Testing"}, locate_by="csdfs")


