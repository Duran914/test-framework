from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import SessionNotCreatedException
from time import sleep, time
import config  # Create & populate config.py 
from termcolor import colored
import sys
from datetime import date
import re
import platform
import datetime


class USI:
        def __init__(self, company, campaign_type, site_id, driver="chrome", device_type="desktop", headless=False, log_file=True, error_report=[]):
                self.company = company
                self.campaign_type = campaign_type
                self.site_id = site_id
                self.driver = driver
                self.device_type = device_type
                self.headless = headless
                self.log_file = log_file
                self.error_report = error_report


        # output campaign info and pass/fail. (will log test to a txt later)
        def initiate_test(self):
                global start_time
                start_time = time()
                self.driver = self.driver.lower()
                self.device_type = self.device_type.lower()
                available_browsers = {"chrome", "firefox", "safari"}

                if self.driver not in available_browsers:
                        USI._log_error(self, err={"value": f"{self.driver} is not valid. Please enter a valid browser"})

                if self.device_type != "desktop" and self.device_type != "mobile":
                        USI._log_error(self, err={
                                "value": f"{self.device_type} is an invalid device type. Set device type: desktop or mobile"
                                })
                global chrome_options
                chrome_options = ChromeOptions()
                firefox_options = FirefoxOptions()
 
                # Mobile execution (Chrome only)
                if self.device_type == "mobile" and self.driver == "chrome":
                        mobile_emulation = { "deviceName": "iPhone 6/7/8" } # Iphone X for now
                        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                elif self.device_type == "mobile" and self.driver == "firefox" or self.device_type == "mobile" and self.driver == "safari":
                        USI._log_error(self, err={"value": "Only chrome can run mobile execution"})

                # Broswer driver
                if self.driver == "chrome":
                        # Disables notifications on chrome 
                        chrome_options.add_argument("--disable-notifications")

                        # Runs broswer in headless mode
                        if self.headless == True:
                                chrome_options.add_argument("--headless")
                                chrome_options.add_argument("--window-size=1920x1080") # Desktop execution

                        try:
                                self.browser = webdriver.Chrome(executable_path=config.chrome_driver, options=chrome_options)
                        except SessionNotCreatedException as msg:
                                USI._terminate_script(self, name="Chrome Webdriver", message=msg)

                elif self.driver == "firefox":
                        # Disables notifications on firefox
                        firefox_options.set_preference("dom.push.enabled", False)

                        if self.headless == True:
                                firefox_options.headless = True
                                firefox_options.add_argument("--window-size=1920x1080")
                        self.browser = webdriver.Firefox(executable_path=config.firefox_driver, options=firefox_options) 

                elif self.driver == "safari":
                        if self.headless == True:
                                USI._logger(self, message=colored("Safari does not support headless mode", color="red"))
                                sys.exit()
                        self.browser = webdriver.Safari(executable_path=config.safari_driver) 

                # DOM set to poll for 15 sec 
                self.browser.implicitly_wait(15)

                # Log script info & results
                results = colored(f"{self.company} {self.campaign_type} {self.site_id}", color="cyan") + f" - {self.driver.capitalize()}|{self.device_type.capitalize()} => " + colored("Running...", color="green")
                USI._logger(self, message=results)
                
        

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


        # logger handles all prints statementsto the terminal. 
        # Also doubles as a function to log error to a log file if _terminate test is executed. 
        def _logger(self, message="", log_to_file="False"):
                if message != "":
                        print(message)
                        self.error_report.append(message)

                # self.log_file is always True unless specified differently in initiate_test()
                # log_to_file can only be True is _termiate_script results in a failed test
                if self.log_file == True and log_to_file == True:
                        # if log_to_file == True:
                        day = date.today()
                        current_date =  str(day)
                        with open( f"QA_Errors_{current_date}.txt",'w', encoding='utf-8') as log:
                                for msg in self.error_report:
                                        # if msg not in log.read():
                                        file_msg = re.sub(r"(36m|0m|32m|31m|34m|\[)", "", msg)
                                        log.write(f"{file_msg}\n")


        # terminates a test
        def _terminate_script(self, name, message="Element could not be located", element="", fail_pass=False):
                if fail_pass == True:
                        USI._logger(self, message=colored("--------------------------Test Aborted----------------------------------", color="yellow") +
                        "\n" + f"{name}: {element} => " +  colored(message, color="yellow"))
                elif element == "":
                        USI._logger(self, message=colored("--------------------------Test Failed----------------------------------", color="red") +
                        "\n" + f"{name} => " +  colored(message, color="red"), log_to_file=True)
                else:
                        USI._logger(self, message=colored("--------------------------Test Failed----------------------------------", color="red") +
                        "\n" + f"{name}: {element} => " +  colored(message, color="red"), log_to_file=True)
                USI._logger(self, message="\n")
                self.browser.quit()
                sys.exit()

      
  # Internal function to return a cookie value
        def _retrive_cookie(self, cookie):
                sleep(2)
                if self.browser.get_cookie(cookie) is None:
                        USI._logger(self, message="Could not retrieve cookie")
                else:
                        cookie_name = self.browser.get_cookie(cookie)
                        cookie_value = cookie_name["value"]
                        return cookie_value


        '''Internal function that add a 5px green or other specified color to see what div is being interacted with.
           Strictly for visuals pf what element is being interacted with, default color is green; red and None is also an acceptable values.  
        '''
        # def _border_color(self, target_element):
        #         if self.headless == True:
        #                 pass
        #         else:
        #                 if self.border_color == "" or self.border_color == None:
        #                         pass
        #                 elif self.border_color == "green":
        #                         self.browser.execute_script(f"document.querySelector('{target_element}').style.border='5px solid #009900'")
        #                 elif self.border_color == "red":
        #                         self.browser.execute_script(f"document.querySelector('{target_element}').style.border='5px solid #e60000'")
        #                 else:
        #                         USI._terminate_script(self, name="Border color", 
        #                         message=f"{self.border_color} is not a valid color. Set border_color to green, red or None")


        # Navigates to url: Accepts 1 string argmuent
        def navigate_url(self, url):
                try:
                        self.browser
                except Exception:
                        USI._terminate_script(self, name="initiate_test()", message="USI class instantiation falied")

                self.browser.get(url)
                USI._logger(self, message="Navigating to => " + colored(url, color="blue"))


        # button click: accepts a dict of button/link names & selector
                # {'Add to cart button':'#cart'}
        def click(self, buttons, locate_by="css", node_index=-1):
                        data_type = ["click", dict]
                        USI._precheck_data(self, buttons, data_type, locate_by)
                        
                        if locate_by == "css":
                                for name, button in buttons.items():
                                        try:
                                                if node_index >= 0:
                                                        sleep(5) # give webdriver time to parse nodelist
                                                        self.browser.find_elements_by_css_selector(button)[node_index].click()
                                                        USI._logger(self, message=f"{name} => " + colored("Clicked", color="green"))
                                                else:
                                                        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button))).click()
                                                        USI._logger(self, message=f"{name} => " + colored("Clicked", color="green"))
                                        except Exception:
                                                USI._terminate_script(self, name=name, element=button)

                        elif locate_by == "xpath":
                                for name, button in buttons.items():
                                        try: 
                                                self.browser.find_element_by_xpath(button).click()
                                                USI._logger(self, message=f"{name} => " + colored("Clicked", color="green"))
                                        except Exception:
                                                USI._terminate_script(self, name=name, element=button)
                

        ''' click_key will click on a keyboard key
            currently only supports tab, enter, ctrl, and command(mac)
            click_key(self, selector="body", key="tab", secondary_key="") '''
        def click_key(self, selector, key, secondary_key=""):
                os_type = platform.system()

                if key == "tab":
                        self.browser.find_element_by_css_selector(selector).send_keys(Keys.TAB)
                elif key == "enter":
                        self.browser.find_element_by_css_selector(selector).send_keys(Keys.ENTER)
                elif key == "ctrl" or key == "cmd":
                        if secondary_key == "":
                                USI._terminate_script(self, name="Missing secondary key(s)", message="secondary_ key must be passed for ctrl or cmd")
                       
                        # CHeck if device is mac 
                        if os_type == "Darwin": 
                                self.browser.find_element_by_css_selector(selector).send_keys(Keys.COMMAND, secondary_key)
                        else:
                                self.browser.find_element_by_css_selector(selector).send_keys(Keys.CONTROL, secondary_key)


        # Input text: accepts an dict of name and selector/input 
                #{"name": ["#formFirstname", "johnny"]}
        def input_text(self, input_data, locate_by="css"):
                data_type = ["input_text", dict]
                USI._precheck_data(self, input_data, data_type, locate_by)

                if locate_by == "css":
                        for name, value in input_data.items():
                                try:
                                        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value[0]))).send_keys(value[1])
                                        USI._logger(self, message=f"{value[1]} => " + colored(f"entered into {name}", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=value[0])
                elif locate_by == "xpath":
                        for name, value in input_data.items():
                                try:
                                        # self.browser.find_element_by_xpath(value[0]).send_keys(value[1])
                                        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, value[0]))).send_keys(value[1])
                                        USI._logger(self, message=f"{value[1]} => " + colored(f"entered into {name}", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=value[0])



        # Inputs email address for LC modal (USI)
                # takes email address string and optional seconds arg
        def lc_input(self, email, selector="#usi_content #usi_email_container #usi_email", sec=60):
                data_type = ["lc_input", str]
                validate_items = [selector, email]
                for item in validate_items:
                        USI._precheck_data(self, item, data_type)

                try:
                        WebDriverWait(self.browser, sec).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(email)
                        USI._logger(self, message=f"LC modal: {email} => " + colored("Entered into LC", color="green"))
                except Exception:
                        USI._terminate_script(self, name="LC input field", element=selector)


        # Hover & button click: accepts a dict of a visible element selector and non-visible selector 
                # {"checkout button": ['#menuBar', '#dropDown a'}
        def hover_and_click(self, elements, locate_by="css"):
                data_type = ["hover_and_click", dict]
                USI._precheck_data(self, elements, data_type, locate_by)

                if locate_by == "css":
                        for name, elements in elements.items():
                                try:
                                        visible_element = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, elements[0])))
                                except Exception:
                                        USI._terminate_script(self, name="visible element", element=elements[0])
                                try:
                                       hidden_element =  WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, elements[1])))

                                except Exception:
                                        USI._terminate_script(self,  name="hidden element",  element=elements[1])

                                ActionChains(self.browser).move_to_element(visible_element).click(hidden_element).perform()
                                USI._logger(self, message="Visible element => " + colored("Hovered", color="green") +
                                "\n" + f"{name} => " + colored("clicked", color="green"))


                elif locate_by == "xpath":
                        for name, elements in elements.items():
                                try:
                                        visible_element = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, elements[0])))
                                except Exception:
                                        USI._terminate_script(self, name="visible element", element=elements[0])
                                try:
                                       hidden_element =  WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, elements[1])))

                                except Exception:
                                        USI._terminate_script(self,  name="hidden element",  element=elements[1])

                                ActionChains(self.browser).move_to_element(visible_element).click(hidden_element).perform()
                                USI._logger(self, message="Visible element => " + colored("Hovered", color="green") +
                                "\n" + f"{name} => " + colored("clicked", color="green"))


        # Submit Button Click: Accepts css selector or default value will be used (USI)
        def click_cta(self, selector="#usi_content .usi_submitbutton", clicks=1):
                data_type = ["click_cta", str]
                USI._precheck_data(self, selector, data_type)
                for _ in range(clicks):
                        try:
                                WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                                USI._logger(self, message="CTA => " + colored("Clicked", color="green"))
                        except Exception:
                                USI._logger(self, message="CTA => " + colored("Not found", color="red"))
                                USI._terminate_script(self, name="CTA", element=selector)


        def mobile_cta(self):
                USI.execute_js("usi_js.submit();", "Mobile CTA clicked")


        # Select box function 
                # Accpets a dict of name and list of css selector & value or text
                #select_option({"Plug type select":["#pa_plug-type","us-plug"]}, select_by="value")
        def select_option(self, select_data, select_by="value"):
                data_type = ["checkbox", dict]
                USI._precheck_data(self, select_data, data_type)

                for name, value in select_data.items():
                        if select_by == "value":
                                select = Select(self.browser.find_element_by_css_selector(value[0]))
                                select.select_by_value(value[1])
                                USI._logger(self, message=f"Value: {value[1]} => " + colored(f"Selected from {name}", color="green"))
                        elif select_by == "text":
                                select= Select(self.browser.find_element_by_css_selector(value[0]))
                                select.select_by_visible_text(value[1])
                                USI._logger(self, message=f"Value: {value[1]} => " + colored(f"Selected from {name}", color="green"))


        # Launches Modal: No args accepted (USI)
        def launch_modal(self, proactive=False, sec=5):
                data_type = ["launch_modal", int]
                USI._precheck_data(self, sec, data_type)
                if proactive == False:
                        USI.halt_execution(self, sec=5)
                        try:
                                self.browser.execute_script("usi_js.display();")
                                USI._logger(self, message="USI modal => " + colored("Launched", color="green"))
                        except JavascriptException:
                                USI._terminate_script(self, name="USI Modal", message="Launch conditions not met; usi_js.display() is undefined", element=".usi_display")
                elif proactive == True:
                        if sec == "":
                                USI._terminate_script(self, name="Proactive Launch", message="Proactive launches must pass a proactive_wait INT argument", element="Bad Data" )
                        else: 
                                USI.halt_execution(self, sec)
                                try:
                                        self.browser.find_element_by_css_selector(".usi_display.usi_show_css")
                                        USI._logger(self, message="USI Modal => " + colored("Launched", color="green"))
                                except JavascriptException:
                                        USI._terminate_script(self, name="USI Modal", message="Proactive Launch conditions not met", element=".usi_display")

        # Executes any javascript code
        def execute_js(self, script, name="JS code"):
                data_type = ["execute_js", str]
                USI._precheck_data(self, script, data_type)

                USI.halt_execution(self, sec=5)
                try:
                        self.browser.execute_script(script)
                        USI._logger(self, message=f"{name} => " + colored("Executed", color="green"))
                except JavascriptException:
                        USI._terminate_script(self, name=name, message="Execution failed", element=script)


        # Appends string url parameters
        def append_url(self, param):
                data_type = ["append_url", str]
                USI._precheck_data(self, param, data_type)

                page_url = ""
                if '?' in self.browser.current_url:
                        page_url = self.browser.current_url + "&" + param
                else:
                        page_url = self.browser.current_url + "?" + param
                USI.navigate_url(self, page_url)


        # checks if boostbar exists
                # accepts one param if named different them the default
        def boostbar_check(self, boostbar="#usi_boost_container"):
                data_type = ["boostbar_check", str]
                USI._precheck_data(self, boostbar, data_type)

                try:
                        if WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, boostbar))):
                                USI._logger(self, message="Boostbar => " + colored("Exists", "green"))
                except Exception:
                        USI._terminate_script(self, name="Boostbar", element=boostbar)


        #  Checks if a tab (TT or LC) can toggle
                # Default params should suffice, change if needed  
        def tab_click(self, decision_selector=".usi_tab_opened", tab="#usi_tab"):
                data_type = ["tab_click", str]
                validate_items = [decision_selector, tab]
                for item in validate_items:
                        USI._precheck_data(self, item, data_type)

                try:
                        USI.click(self, buttons={"USI tab":tab})
                except Exception:
                        USI._terminate_script(self, name="tab", element="#usi_tab")
                
                try:
                        if self.browser.find_element_by_css_selector(decision_selector):
                                USI._logger(self, message="Tab => " + colored("Opened", "green"))
                except Exception:
                        USI._terminate_script(self, name="tab_opened class", element=".usi_tab_opened")
                        
                

        # Retrieves session cookie
                #accepts a str of the cookie you want ot retrieve
        def get_cookie(self, cookie):
                data_type = ["get_cookie", str]
                USI._precheck_data(self, cookie, data_type)

                USI.halt_execution(self, sec=3)
                if self.browser.get_cookie(cookie) is None:
                        USI._logger(self, message="Could not retrieve cookie")
                else:
                        cookie_name = self.browser.get_cookie(cookie)
                        cookie_value = cookie_name["value"]
                        USI._logger(self, message=f"{cookie}: " + colored(cookie_value, "blue"))
        

        #   Check for coupon validation
                ''' 
                Accpets a type of validate_by which can be an "element", "message", or
                element_message. message & element_message must pass message_text.
                EX. 
                coupon_validation(validate_by="element_message", message_text='Coupon code applied.', target_element=".messages")
                '''
                        # coupon_validation(self, validate_by="")
        def coupon_validation(self, validate_by, target_element, message_text="", locate_by="css"):
                data_type = ["coupon_validation", str]
                validate_items = [validate_by, target_element, message_text]
                [USI._precheck_data(self, item, data_type) for item in validate_items]


                if locate_by == "css":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, target_element))):
                                        USI._logger(self, message="Coupon code element => " + colored("Valid", color="green"))
                        except Exception:
                                USI._terminate_script(self, name="Coupon Element", element=target_element, message="In-valid validation element")
                       
                        if validate_by == "message" or validate_by == "element_message":                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, target_element), message_text)):
                                                USI._logger(self, message="Coupon code validation message => " + colored("Valid: " + message_text, color="green"))
                                except Exception:
                                        USI._terminate_script(self, name="Coupon Message", element=message_text, message="In-valid validation message")

                if locate_by == "xpath":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, target_element))):
                                        USI._logger(self, message="Coupon code element => " + colored("Valid", color="green"))
                        except Exception:
                                USI._terminate_script(self, name="Coupon Element", element=target_element, message="In-valid validation element")
                       
                        if validate_by == "message" or validate_by == "element_message":
                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.XPATH, target_element), message_text)):
                                                USI._logger(self, message="Coupon code validation message => " + colored("Valid: " + message_text, color="green"))
                                except Exception:
                                        USI._terminate_script(self, name="Coupon Message", element=message_text, message="In-valid validation message")
                
                
        '''
        THe discount_check check if a promo codes is applying the correct percentage or fixed amount off.
        promo_data accepts a array of subtotal, discount, and final_total
        discount_data accepts an dictionary, keys specify the element name which are subtotal, discount, and final_total and their associated values 
        are their selector. 
        locate_by allow to scrape by css selector or xpath
        company_tt_123.discount_check(
                 promo_data=["percent", .10],
                 discount_data = {
                 "Subtotal":"#selector",
                 "Discount":"#selector",
                 "Grand total": "#selector"
                 }
        )
        '''
        def discount_check(self, promo_data, discount_data, locate_by="css"):
                data_type1 = ["promo_data", list]
                data_type2 = ["discount_check", dict]
                USI._precheck_data(self, promo_data, data_type1)
                USI._precheck_data(self, discount_data, data_type2)
                
                # if discount_data != {}:
                if locate_by == "css":
                        for amount_name,element in discount_data.items():
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, element))).get_attribute("innerText"):
                                                USI._logger(
                                                        self, message=f"{amount_name} => " + colored
                                                        (WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, element))).get_attribute("innerText"), 
                                                        color="green")
                                                        )
                                except Exception:
                                        USI._terminate_script(self, name=amount_name, element=element, message=f"Could not be found")


                        prices_list = list(discount_data.values())
                        sub_total = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, prices_list[0]))).get_attribute("innerText")
                        discount = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, prices_list[1]))).get_attribute("innerText")
                        final_total = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, prices_list[2]))).get_attribute("innerText")

                if locate_by == "xpath":
                        for amount_name,element in discount_data.items():
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, element))).get_attribute("innerText"):
                                                USI._logger(
                                                        self, message=f"{amount_name} => " + colored
                                                        (WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, element))).get_attribute("innerText"), 
                                                        color="green")
                                                        )
                                except Exception:
                                        USI._terminate_script(self, name=amount_name, element=element, message=f"Could not be found")


                        prices_list = list(discount_data.values())
                        sub_total = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, prices_list[0]))).get_attribute("innerText")
                        discount = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, prices_list[1]))).get_attribute("innerText")
                        final_total = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, prices_list[2]))).get_attribute("innerText")

                prices_list = [sub_total, discount, final_total]
                totals = [int(re.sub(r"[$.-]", "", num)) for num in prices_list]
                
                
                if promo_data[0] == "percent":
                        desired_value = int(totals[0] - round(float(totals[0]) * float(promo_data[1])))
                elif promo_data[0] == "fixed":
                        desired_value = totals[0] - (promo_data[1] * 100)

                # if shipping != "":
                #        desired_value = desired_value + shipping


                # used to account for site that may round up or down 
                low_threshold = int(desired_value) - 1
                high_threshold = int(desired_value) + 2

                if int(desired_value) == int(totals[2]) or totals[2] in range(low_threshold, high_threshold):
                        USI._logger(self, message=f"Discount amount: {format(promo_data[1], '.2f')} off => " + colored("Correct", "green"))
                else:
                        USI._terminate_script(self, name="Discount: ", message=f"Correct Amount should be {totals[2]}", element=desired_value)



        # Closes usi modal (USI)
                # Accepts one string param if different from default
        def close_usi_modal(self, selector="#usi_default_close", locate_by="css"):
                data_type = ["checkbox", str]
                USI._precheck_data(self, selector, data_type, locate_by)

                if locate_by == "css":
                        try:
                                WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                                USI._logger(self, message="Modal => " + colored("Closed", "green"))
                        except Exception:
                                USI._terminate_script(self, name="Close button", element=selector)
                if locate_by == "xpath":
                        try:
                                WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, selector))).click()
                                USI._logger(self, message="Modal => " + colored("Closed", "green"))
                        except Exception:
                                USI._terminate_script(self, name="Close button", element=selector)


        ''' Checks to see if a desired element is present on the DOM and visible on page. 
            Can be used as a condition for another action. 
            Ex. wait_for_element_visibility(self, element_name="Login Modal", selector="#login-modal", locate_by="css")
        '''
        def wait_for_element_visibility(self, element_name, selector, text="", locate_by="css"):
                if locate_by == "css":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))):
                                        USI._logger(self, message=f"{element_name}: {selector} => " + colored("Element Located", "green"))
                        except Exception:
                                USI._terminate_script(self, name=element_name, element=selector)
                        
                        if text != "":                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)):
                                                USI._logger(self, message=f"{element_name}: text => " + colored("Valid: " + text, color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=f"{element_name}: text", element=text, message="In-valid element text")
                elif locate_by == "xpath":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, selector))):
                                        USI._logger(self, message=f"{element_name}: {selector} => " + colored("Element Located", "green"))
                        except Exception:
                                USI._terminate_script(self, name=element_name, element=selector)
                        
                        if text != "":                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.XPATH, selector), text)):
                                                USI._logger(self, message=f"{element_name}: text => " + colored("Valid: " + text, color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=f"{element_name}: text", element=text, message="In-valid element text")


        # Open an email in a broswer window which can be use to check email links are working 
                #Accepts two strings of session name and element xpath for the email element (xpath MUST be used here).
                        #  usi_email_link(self, 
                        #       session="usi_sess_27176_739_1567110133125", 
                        #       element_xpath="")
        def email_link_follow(self, campaign_type, element_xpath, override_session_name="", new_window=True):
                data_type = ["usi_email_link", str]
                validate_items = [campaign_type, element_xpath]
                [USI._precheck_data(self, item, data_type) for item in validate_items]
        

                if campaign_type.lower() == "lc":
                        cookie_session_name = "usi_sess"
                elif campaign_type.lower() == "pc":
                        cookie_session_name = "USI_Session"
                elif override_session_name != "":
                        cookie_session_name == override_session_name
     
                sleep(5) # Static wait for email to process
                USI.navigate_url(self, url=f"https://www.upsellit.com/email/onlineversion.jsp?{USI._retrive_cookie(self, cookie=cookie_session_name)}~1")
                
                tries = 3 # will try to refresh page 3 times to load email in broswer 
                while self.browser.find_element_by_css_selector("head > title").get_attribute("innerHTML") == "Oops, email has expired":
                        USI.refresh_page(self)
                        sleep(3)
                        tries -= 1
                        if tries == 0:
                                USI._terminate_script(self, name="Email url", element=campaign_type, message="Session not found")

                try:
                        USI.click(self, buttons={"Email hero link":element_xpath}, locate_by="xpath")
                except Exception:
                        USI._terminate_script(self, name="Hero Image", element=element_xpath, message="Email link not found")

                # In the event of an email link missing a target="_blank" attribute; set new_window argument to false
                if new_window == True:
                        self.browser.switch_to.window(self.browser.window_handles[1])

        ''' 
        switch_tab will move to a desired tab when multiple are open.
        Default value is 1 from the left.(0 is considered the first tab)
        )
        '''
        def switch_tab(self, tab=1):
                self.browser.switch_to.window(self.browser.window_handles[tab])


        # Checks a split test result, test will terminate as a no pass/fail is result is Control Group
                # split_test_check(self, dice_roll="usi_dice_roll27248")
                # naming convention is normally as such usi_dice_roll27248, double check app file. 
        def split_test_check(self, dice_roll):
                sleep(5) # Static wait for cookie creation
                data_type = ["split_test_check", str]
                USI._precheck_data(self, dice_roll, data_type)
                
                if USI._retrive_cookie(self, cookie=dice_roll) == "0" or USI._retrive_cookie(self, cookie=dice_roll) == None:
                        USI._terminate_script(self, name="Split test", element=dice_roll, message="Control group", fail_pass=True)
                else:   
                        USI._logger(self, message="Split Group: " + colored("USI" , color="green"))
                        pass


        # Interacts with to page to enable launch on mobile (usi)
        def mobile_interact(self):
                self.browser.find_element_by_tag_name("body").click()


        # Simply refeshes a page
        def refresh_page(self):
                self.browser.refresh()
                USI._logger(self, message=colored("Page refreshed", color="blue"))


        # checkbox_data is used to click a checkbox 

        def checkbox(self, checkbox_data="", locate_by="css"):
                data_type = ["checkbox", dict]
                USI._precheck_data(self, checkbox_data, data_type, locate_by)

                if locate_by == "css":
                        for name, selector in checkbox_data.items():
                                try:
                                        self.browser.find_element_by_css_selector(selector).click()
                                        USI._logger(self, message=f"{name} => {selector} " + colored("Checked", "green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=selector, message="Checkbox could not be checked")
                elif locate_by == "xpath":
                        for name, selector in checkbox_data.items():
                                try:
                                        self.browser.find_element_by_xpath(selector).click()
                                        USI._logger(self, message=f"{name} => {selector} " + colored("Checked", "green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=selector, message="Checkbox could not be checked")
        

        # checks if a campaign is under the correct sale window for launch
        # Accepts an two string arguments of a state date and an end date
        def set_date_window(self, start_date, end_date):
                data_type = ["set_date_window", str]
                validate_items = [start_date, end_date]  
                [USI._precheck_data(self, item, data_type) for item in validate_items]


                today = datetime.datetime.now()
                start_list = start_date.split("-")
                end_list = end_date.split("-")

                # Convert to INTs 
                start_list = [int(x) for x in start_list]
                end_list = [int(x) for x in end_list]

                # Date values to check against
                starting_date = datetime.datetime(start_list[0],start_list[1], start_list[2])
                ending_date = datetime.datetime(end_list[0],end_list[1], end_list[2])

                if ending_date < starting_date:
                        USI._log_error(self, err={"value":  f"End date => {end_date} cannot be eariler then specified start date {start_date}"})

                if starting_date <= today <= ending_date:
                        pass
                elif starting_date > today:
                        USI._terminate_script(self, name="Date", element=today, message="Sale window for this campaign has not yet began", fail_pass=True)
                else:
                        USI._terminate_script(self, name="Date", element=today, message="Sale window for this campaign had ended", fail_pass=True)


        # Takes screenshot
        def take_screenshot(self, screenshot_name="default.png"):
                self.browser.save_screenshot(f"{screenshot_name}.png")


        # Halts execution of script (last case scenario)
        def halt_execution(self, sec):
                sleep(sec)


        # Shuts down driver 
        def shutdown(self):
                complete_time = round((time() - start_time), 1)
                USI._logger(self, message=colored("Shutting down driver", color="yellow"))
                sleep(3) # Static wait solely for UX
                self.browser.quit()
                USI._logger(self, message=colored("---------------------------Test Complete-----------------------------", color="green") +
                "\n" + colored(self.campaign_type + " " + self.site_id, color="cyan") + " => " + 
                colored(f"All Tests Passed ({complete_time}s)", color="green") + "\n")

