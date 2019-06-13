from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


browser = webdriver.Chrome('//Users/johnnyduran/Python/Selenium/chromedriver') 
browser.implicitly_wait(30)
browser.get('https://www.bcbg.com/en/draped-chiffon-maxi-dress/EPK6206201-809.html?dwvar_EPK6206201-809_color=809&cgid=dresses#start=2&dwvar_EPK6206201-809_color=809&cgid=dresses?usi_enable=1')


def click_btn(buttons):
    for button in buttons:
        browser.find_element_by_css_selector(button).click()

def input_text(checkoutData):
    for selector, value in checkoutData.items():
        browser.find_element_by_css_selector(selector).send_keys(value)

def hover_click_btn(visibleElement, hiddenElement):
        visibleEl = browser.find_element_by_css_selector(visibleElement)
        hiddenEl = browser.find_element_by_css_selector(hiddenElement)
        ActionChains(browser).move_to_element(visibleEl).click(hiddenEl).perform()

def usi_submit_click():
        WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#usi_content .usi_submitbutton"))).click()

def lanuch_usi_modal():
        browser.execute_script("usi_js.display()")


# browser.implicitly_wait(30)
# browser.execute_script("usi_js.display()")

# hover_click_btn('#usi_content', 'button.usi_submitbutton')
# click_btn(['#usi_close']) # Worked 
# click_btn(['#usi_content button'])

# WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#usi_content .usi_submitbutton"))).click()


# usiSubmitClick()

lanuch_usi_modal()
usi_submit_click()