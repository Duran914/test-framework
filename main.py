from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome('insert dir to driver') 
browser.implicitly_wait(30)

# Navigates to url: Accepts 1 string argmuent
def navigate_url(url):
        browser.get(url)

# button click: accepts a list of css selectors
        # ['#btn', '#nextBtn']
def click_btn(buttons):
    for button in buttons:
        browser.find_element_by_css_selector(button).click()

# Input text: accepts an dict of css selector & input 
        # eg. {'#formFirstname': 'Johnny'}
def input_text(inputData):
    for selector, value in inputData.items():
        browser.find_element_by_css_selector(selector).send_keys(value)

# Hover & button click: accepts a list of a visible element selector and non-visible selector 
        # ['#menuBar', '#dropDown a']
def hover_click_btn(visibleElement, hiddenElement):
        visibleEl = browser.find_element_by_css_selector(visibleElement)
        hiddenEl = browser.find_element_by_css_selector(hiddenElement)
        ActionChains(browser).move_to_element(visibleEl).click(hiddenEl).perform()

# Submit Button Click: Accepts css selector or default value will be used
def submit_click(selector="#usi_content .usi_submitbutton"):
        WebDriverWait(browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        
# Launches Modal: No args accepted 
def launch_modal():
        browser.execute_script("setTimeout( () => { usi_js.display(); }, 5000);")

def shutdown():
        browser.quit()

def halt_execution(sec):
        time.sleep(sec)





