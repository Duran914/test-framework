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
from termcolor import colored
import sys


class USI:
        def __init__(self, company, campaign_type, site_id, driver="chrome", device_type="desktop", headless=False):
                self.company = company
                self.campaign_type = campaign_type
                self.site_id = site_id
                self.driver = driver
                self.device_type = device_type
                self.headless = headless
                
        # output campaign info and pass/fail. (will log test to a txt later)
        def initiate_test(self):
                self.driver = self.driver.lower()
                self.device_type = self.device_type.lower()
                available_browsers = {"chrome", "firefox", "safari"}

                if self.driver not in available_browsers:
                        USI.__log_error(self, err={"value": f"{self.driver} is not valid. Please enter a valid browser"})

                if self.device_type != "desktop" and self.device_type != "mobile":
                        USI.__log_error(self, err={"value": "Set device type: desktop or mobile"})

                if self.site_id == None:
                        USI.__log_error(self, err={"value": "Enter a site id"}) #(USI)

                chrome_options = ChromeOptions()
                firefox_options = FirefoxOptions()
                # global browser

                # Mobile execution (Chrome only)
                if self.device_type == "mobile" and self.driver == "chrome":
                        mobile_emulation = { "deviceName": "iPhone X" } # Iphone X for now
                        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                elif self.device_type == "mobile" and self.driver == "firefox" or self.device_type == "mobile" and self.driver == "safari":
                        USI.__log_error(self, err={"value": "Only chrome can run mobile execution"})

                # Broswer driver
                if self.driver == "chrome":
                        # Runs broswer in headless mode
                        if self.headless == True:
                                chrome_options.add_argument("--headless")
                                chrome_options.add_argument("--window-size=1920x1080") # Desktop execution
                        self.browser = webdriver.Chrome(executable_path=config.chrome_driver, options=chrome_options) 

                elif self.driver == "firefox":
                        if self.headless == True:
                                firefox_options.headless = True
                                firefox_options.add_argument("--window-size=1920x1080")
                        self.browser = webdriver.Firefox(executable_path=config.firefox_driver, options=firefox_options) 

                elif self.driver == "safari":
                        self.browser = webdriver.Safari(executable_path=config.safari_driver) 

                # Log script info & results
                results = f"{self.company} {self.campaign_type} {self.site_id}: Running..."
                print(results)


        # selector validation
        # def check_selector(locate_by="css"):
        #         # Allowed locators
        #         allowed_locator = {"xpath", "css"}

        #         if locate_by not in allowed_locator:
        #                 __log_error({"value": "Enter a valid element locator"})
        #         else:
        #                 pass

        def __precheck_data(self, elements, data_type, locate_by="css"):
                allowed_locator = {"xpath", "css"}
                if locate_by not in allowed_locator:
                        USI.__log_error(self, err={"value": f"{locate_by} is not a valid locator. Valid locators are {allowed_locator}"})
                elif data_type[1] != type(elements):
                        USI.__log_error(self, err={"type": f"{data_type[0]} accpets a {data_type[1]}"})
                else:
                        pass



        # Send error to console (will update to write to file)
        def __log_error(self, err):
                for err_type, message in err.items():
                        if err_type == "value":
                                raise ValueError(message)
                        elif err_type == "type":
                                raise TypeError(message)
                        elif err_type == "name":
                                raise NameError(message)
                        elif err_type == "exeception":
                                print(message)


        # terminate test 
        def __element_not_located(self, name, element=""):
                print(colored("--------------------------Test Failed----------------------------------", color="red"))
                print(f"{name}: {element}  => " +  colored("Element could not be located", color="red"))
                sys.exit()


        # Navigates to url: Accepts 1 string argmuent
        def navigate_url(self, url):
                self.browser.get(url)
                print(colored(f"Navigating to {url}", color="green"))


        # button click: accepts a dict of button/link names & selector
                # {'Add to cart button':'#cart'}
        def click_btn(self, buttons, locate_by="css"):
                data_type = ["click_btn", dict]
                USI.__precheck_data(self, buttons, data_type, locate_by)
                # check_selector(locate_by)
                # if type(buttons) != dict:
                #         __log_error({'type':"click_btn accepts a list of selectors"})

                if locate_by == "css":
                        for name, button in buttons.items():
                                try: 
                                        self.browser.find_element_by_css_selector(button).click()
                                        print(f"{name} => " + colored("clicked", color="green"))
                                except Exception:
                                        USI.__element_not_located(name, button)

                elif locate_by == "xpath":
                        for name, button in buttons.items():
                                try: 
                                        self.browser.find_element_by_xpath(button).click()
                                        print(f"{name} => " + colored("clicked", color="green"))
                                except Exception:
                                        USI.__element_not_located(name, button)


        # Input text: accepts an dict of css selector & input 
                # eg. {'#formFirstname': 'Johnny'}
                #{"name": ["#formFirstname", "johnny"]}
        def input_text(self, input_data, locate_by="css"):
                # check_selector(locate_by)
                if type(input_data) != dict:
                        USI.__log_error(self, err={'type':"input_text accepts a dictionary of selector and text"})

                if locate_by == "css":
                        for name, value in input_data.items():
                                try:
                                        self.browser.find_element_by_css_selector(value[0]).send_keys(value[1])
                                        print(f'"{value[1]}" entered into {name} ')
                                except Exception:
                                        USI.__element_not_located(name,value[0])
                elif locate_by == "xpath":
                        for name, value in input_data.items():
                                try:
                                        self.browser.find_element_by_xpath(value[0]).send_keys(value[1])
                                        print(f'"{value[1]}" entered into {name} ')
                                except Exception:
                                        USI.__element_not_located(name,value[0])



        # Inputs email address for LC modal (USI)
                # takes email address string and optional seconds arg
        def lc_input(self, input_email, selector="#usi_content #usi_email_container #usi_email", sec=60):
                try:
                        WebDriverWait(self.browser, sec).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(input_email)
                        print(f"{input_email} => " + colored("entered into LC", color="green"))
                except Exception:
                        print(colored("LC input falied", color="red"))


        # Hover & button click: accepts a dict of a visible element selector and non-visible selector 
                # {'#menuBar', '#dropDown a'}
        def hover_click_btn(self, elements, locate_by="css"):
                # check_selector(locate_by)
                if type(elements) != dict:
                        USI.__log_error(self, err={'type':"hover_click_btn accepts a dictionary of visiable and hidden elements"})

                if locate_by == "css":
                        for v_el, h_el in elements.items():
                                visible_element = self.browser.find_element_by_css_selector(v_el)
                                hidden_element = self.browser.find_element_by_css_selector(h_el)
                                ActionChains(self.browser).move_to_element(visible_element).click(hidden_element).perform()
                                print(f" Hovered over {hidden_element}  \n {visible_element} clicked ")
                elif locate_by == "xpath":
                        for v_el, h_el in elements.items():
                                visible_element = self.browser.find_element_by_xpath(v_el)
                                hidden_element = self.browser.find_element_by_xpath(h_el)
                                ActionChains(self.browser).move_to_element(visible_element).click(hidden_element).perform()


        # Submit Button Click: Accepts css selector or default value will be used (USI)
        def click_cta(self, selector="#usi_content .usi_submitbutton"):
                try:
                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                        print("CTA submit clicked ")
                except Exception:
                        print(colored("CTA not found", color="red"))


        # Clicks a button when it becomes visible
        def btn_click_when_visible(self, button, locate_by="css"):
                # check_selector(locate_by)
                
                if locate_by == "css":
                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button))).click()
                        print(f"{button} clicked ")
                elif locate_by == "xpath":
                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.XPATH, button))).click()
                        print(f"{button} clicked ")
                

        # Launches Modal: No args accepted (USI)
        def launch_modal(self):
                self.browser.execute_script("setTimeout( () => { usi_js.display(); }, 5000);")

        # Executes any javascript code
        def execute_js(self, script):
                self.browser.execute_script(script)


        # Appends string url parameters
        def append_url(self, param):
                page_url = ""
                if '?' in self.browser.current_url:
                        page_url = self.browser.current_url + "&" + param
                else:
                        page_url = self.browser.current_url + "?" + param
                USI.navigate_url(self, page_url)
                print(f"Navigated to {page_url}")


        # Retrieves session cookie
                #accepts a str of the cookie you want ot retrieve
        def get_cookie(self, cookie_name):
                if self.browser.get_cookie(cookie_name) is None:
                        print("Could not retrieve session cookie")
                else:
                        cookie = self.browser.get_cookie(cookie_name)
                        session_name = cookie["value"]
                        print(f"USI session: {session_name}")


        # Shuts down driver 
        def shut_down(self):
                print("Shutting down driver")
                sleep(5)
                self.browser.quit()
                print(colored("---------------------------Test Complete-----------------------------", color="green"))
                # print(colored("Test Complete", color="green"))


        # Halts execution of script (last case scenario)
        def halt_execution(self, sec):
                sleep(sec)


        def take_screenshot(self, screenshot_name="default.png"):
                self.browser.save_screenshot(f"{screenshot_name}.png")

usi = USI("Office-Furniture-to-go", "TT", "24586", driver="chrome", device_type="desktop")
usi.initiate_test()
usi.navigate_url('https://www.officefurniture2go.com/')
usi.click_btn({"Shop conference tables button":'#ctl00_mainPlaceHolder_hlHeroSecond'})
usi.shut_down()