from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
                        USI._log_error(self, err={"value": f"{self.driver} is not valid. Please enter a valid browser"})

                if self.device_type != "desktop" and self.device_type != "mobile":
                        USI._log_error(self, err={
                                "value": f"{self.device_type} is an invalid device type. Set device type: desktop or mobile"
                                })

                chrome_options = ChromeOptions()
                firefox_options = FirefoxOptions()

                # Mobile execution (Chrome only)
                if self.device_type == "mobile" and self.driver == "chrome":
                        mobile_emulation = { "deviceName": "iPhone X" } # Iphone X for now
                        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                elif self.device_type == "mobile" and self.driver == "firefox" or self.device_type == "mobile" and self.driver == "safari":
                        USI._log_error(self, err={"value": "Only chrome can run mobile execution"})

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
                results = colored(self.company + " " + self.campaign_type + " " + 
                self.site_id, color="cyan") + " => " + colored("Running...", color="green")
                print(results)


        def _precheck_data(self, elements, data_type, locate_by="css"):
                allowed_locator = {"xpath", "css"}
                if locate_by not in allowed_locator:
                        USI._log_error(self, err={"value": f"{locate_by} is not a valid locator. Valid locators are {allowed_locator}"})
                elif data_type[1] != type(elements):
                        USI._log_error(self, err={"type": f"{data_type[0]} accpets a {data_type[1]}"})
                else:
                        pass



        # Send error to console (will update to write to file)
        def _log_error(self, err):
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
        def _element_not_located(self, name, element=""):
                print(colored("--------------------------Test Failed----------------------------------", color="red"))
                print(f"{name}: {element} => " +  colored("Element could not be located", color="red"))
                sys.exit()


        # Navigates to url: Accepts 1 string argmuent
        def navigate_url(self, url):
                self.browser.get(url)
                print("Navigating to => " + colored(url, color="blue"))


        # button click: accepts a dict of button/link names & selector
                # {'Add to cart button':'#cart'}
        def click(self, buttons, locate_by="css"):
                data_type = ["click", dict]
                USI._precheck_data(self, buttons, data_type, locate_by)

                if locate_by == "css":
                        for name, button in buttons.items():
                                try: 
                                        self.browser.find_element_by_css_selector(button).click()
                                        print(f"{name} => " + colored("clicked", color="green"))
                                except Exception:
                                        USI._element_not_located(name, button)

                elif locate_by == "xpath":
                        for name, button in buttons.items():
                                try: 
                                        self.browser.find_element_by_xpath(button).click()
                                        print(f"{name} => " + colored("clicked", color="green"))
                                except Exception:
                                        USI._element_not_located(name, button)


        # Input text: accepts an dict of name and selector/input 
                #{"name": ["#formFirstname", "johnny"]}
        def input_text(self, input_data, locate_by="css"):
                data_type = ["input_text", dict]
                USI._precheck_data(self, input_data, data_type, locate_by)

                if locate_by == "css":
                        for name, value in input_data.items():
                                try:
                                        self.browser.find_element_by_css_selector(value[0]).send_keys(value[1])
                                        print(f'"{value[1]}" entered into {name} ')
                                except Exception:
                                        USI._element_not_located(name,value[0])
                elif locate_by == "xpath":
                        for name, value in input_data.items():
                                try:
                                        self.browser.find_element_by_xpath(value[0]).send_keys(value[1])
                                        print(f'"{value[1]}" entered into {name} ')
                                except Exception:
                                        USI._element_not_located(name,value[0])



        # Inputs email address for LC modal (USI)
                # takes email address string and optional seconds arg
        def lc_input(self, input_email, selector="#usi_content #usi_email_container #usi_email", sec=60):
                try:
                        WebDriverWait(self.browser, sec).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(input_email)
                        print(f"{input_email} => " + colored("entered into LC", color="green"))
                except Exception:
                        print(colored("LC input falied", color="red"))


        # Hover & button click: accepts a dict of a visible element selector and non-visible selector 
                # {"checkout button": ['#menuBar', '#dropDown a'}
        def hover_and_click(self, elements, locate_by="css"):
                data_type = ["hover_and_click", dict]
                USI._precheck_data(self, elements, data_type, locate_by)

                if locate_by == "css":
                        for name, elements in elements.items():
                                try:
                                        visible_element = self.browser.find_element_by_css_selector(elements[0])
                                except Exception:
                                        USI._element_not_located(self, name="visible element", element=elements[0])
                                try:
                                        hidden_element = self.browser.find_element_by_css_selector(elements[1])
                                except Exception:
                                        USI._element_not_located(self,  name="hidden element",  element=elements[1])

                                ActionChains(self.browser).move_to_element(visible_element).click(hidden_element).perform()
                                print("Visible element => " + colored("Hovered", color="green"))
                                print(f"{name} => " + colored("clicked", color="green"))


                elif locate_by == "xpath":
                        for name, elements in elements.items():
                                try:
                                        visible_element = self.browser.find_element_by_xpath(elements[0])
                                except Exception:
                                        USI._element_not_located(self, name="visible element", element=elements[0])
                                try:
                                        hidden_element = self.browser.find_element_by_xpath(elements[1])
                                except Exception:
                                        USI._element_not_located(self,  name="hidden element",  element=elements[1])

                                ActionChains(self.browser).move_to_element(visible_element).click(hidden_element).perform()
                                print("Visible element => " + colored("Hovered", color="green"))
                                print(f"{name} => " + colored("clicked", color="green"))


        # Submit Button Click: Accepts css selector or default value will be used (USI)
        def click_cta(self, selector="#usi_content .usi_submitbutton"):
                try:
                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                        print("CTA => " + colored("Clicked", color="green"))
                except Exception:
                        print("CTA => " + colored("Not found", color="red"))
                        USI._element_not_located(self, name="CTA", element=selector)


        # Clicks a button when it becomes visible

        def click_when_visible(self, elements, locate_by="css"):
                data_type = ["click_when_visible", dict]
                USI._precheck_data(self, elements, data_type, locate_by)

                if locate_by == "css":
                        for name, value in elements.items():
                                try:
                                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, value))).click()
                                        print(f"{name} => ", colored("clicked", color="green"))
                                except Exception:
                                        USI._element_not_located(self, name=name, element=value)
                elif locate_by == "xpath":
                        for name, value in elements.items():
                                try:
                                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.XPATH, value))).click()
                                        print(f"{name} => ", colored("clicked", color="green"))
                                except Exception:
                                        USI._element_not_located(self, name=name, element=value)


        # Select box function 
                # Accpets a dict of name and list of css selector & value or text
        def select_option(self, select_data, select_by="value"):
                for name, value in select_data.items():
                        if select_by == "value":
                                select = Select(self.browser.find_element_by_css_selector(value[0]))
                                select.select_by_value(value[1])
                                print(f"Value: {value[1]} => " + colored(f"Selected from {name}", color="green"))
                        elif select_by == "text":
                                select= Select(self.browser.find_element_by_css_selector(value[0]))
                                select.select_by_visible_text(value[1])
                                print(f"Value: {value[1]} => " + colored(f"Selected from {name}", color="green"))


        # Launches Modal: No args accepted (USI)
        def launch_modal(self):
                USI.halt_execution(self, sec=3)
                self.browser.execute_script("usi_js.display();")
                print("USI Modal => " + colored("Launched", color="green"))


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


        # Retrieves session cookie
                #accepts a str of the cookie you want ot retrieve
        def get_cookie(self, cookie_name):
                if self.browser.get_cookie(cookie_name) is None:
                        print("Could not retrieve session cookie")
                else:
                        cookie = self.browser.get_cookie(cookie_name)
                        session_name = cookie["value"]
                        print(f"USI session: " + colored(session_name, "blue"))


        #   Check for coupon validation
                ''' 
                Accpets a type of validate_by which can be an "element", "message", or
                element_message. message & element_message must pass message_text.
                EX. 
                coupon_validation(validate_by="element_message", message_text='Coupon code applied.', target_element=".messages")
                '''
                        # coupon_validation(self, validate_by="")
        def coupon_validation(self, validate_by, target_element, message_text=""):
                if validate_by == "element":
                        if self.browser.find_element_by_css_selector(target_element):
                                print("Coupon code element => " + colored("Valid", color="green"))
                        else:
                                print("Coupon code element => " + colored("In-Valid", color="red"))
                elif validate_by == "message":
                        valididation_message = self.browser.find_element_by_css_selector(target_element).get_attribute("innerHTML")
                        if message_text == valididation_message:
                                print("Validation message => " + colored("Valid", color="green"))
                        else:
                                print("Validation message => " + colored("In-Valid", color="red"))
                elif validate_by == "element_message":
                        valididation_message = self.browser.find_element_by_css_selector(target_element).get_attribute("innerHTML")
                        if self.browser.find_element_by_css_selector(target_element):
                                if message_text == valididation_message:
                                       print("Coupon code element and validation message => " + colored("Valid", color="green"))
                                else:
                                        print("Validation message => " + colored("In-Valid", color="red"))
                        else:
                                print("Coupon code element => " + colored("In-Valid", color="red"))

        # Closes usi modal (USI)
                # Accepts one string param if different from default
        def close_usi_modal(self, selector="#usi_default_close"):
                try:
                        WebDriverWait(self.browser, 90).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                        print("Modal => " + colored("Closed", "green"))
                except Exception:
                       USI._element_not_located(self, name="Close button", element=selector)


        # Interacts with to page to enable launch on mobile (usi)
        def mobile_interact(self):
                self.browser.find_element_by_tag_name("body").click()
                

        # Shuts down driver 
        def shutdown(self):
                print(colored("Shutting down driver", color="yellow"))
                sleep(5)
                self.browser.quit()
                print(colored("---------------------------Test Complete-----------------------------", color="green"))
                print(colored(self.campaign_type + " " + self.site_id, color="cyan") + " => " + colored("All Tests Passed ", color="green"))


        # Halts execution of script (last case scenario)
        def halt_execution(self, sec):
                sleep(sec)


        def take_screenshot(self, screenshot_name="default.png"):
                self.browser.save_screenshot(f"{screenshot_name}.png")


