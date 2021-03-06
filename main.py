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
                global test_count
                test_count = 0
                self.driver = self.driver.lower()
                self.device_type = self.device_type.lower()
                available_browsers = {"chrome", "firefox", "safari"}

                if self.driver not in available_browsers:
                        USI._terminate_script(self, name=f"{self.driver}: ", message="In-valid driver. Please enter a valid browser")

                if self.device_type != "desktop" and self.device_type != "mobile":
                        USI._terminate_script(self, name=f"{self.device_type}: ", message="Invalid device type. Set device type: desktop or mobile")
                global chrome_options
                chrome_options = ChromeOptions()
                firefox_options = FirefoxOptions()
 
                # Mobile execution (Chrome only)
                if self.device_type == "mobile" and self.driver == "chrome":
                        mobile_emulation = { "deviceName": "iPhone 6/7/8" } # Iphone X for now
                        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                elif self.device_type == "mobile" and self.driver == "firefox" or self.device_type == "mobile" and self.driver == "safari":
                        USI._terminate_script(self, name=f"{self.driver}-{self.device_type}: ", message="Only chrome can run mobile execution")

                # Broswer driver
                if self.driver == "chrome":
                        # Disables notifications on chrome 
                        chrome_options.add_argument("--disable-notifications")
                        chrome_options.add_argument("--window-size=1920x1080")

                        # Runs broswer in headless mode
                        if self.headless == True:
                                chrome_options.add_argument("--headless")
                                chrome_options.add_argument("--window-size=1920x1080") # Desktop execution

                        try:
                                self.browser = webdriver.Chrome(executable_path=config.chrome_driver, options=chrome_options)
                        except SessionNotCreatedException as msg:
                                USI._terminate_script(self, name="Chrome Webdriver", message=f"{msg}. Download new Chrome driver at https://chromedriver.chromium.org/" )

                elif self.driver == "firefox":
                        # Disables notifications on firefox
                        firefox_options.set_preference("dom.push.enabled", False)

                        if self.headless == True:
                                firefox_options.headless = True
                                firefox_options.add_argument("--window-size=1920x1080")
                        self.browser = webdriver.Firefox(executable_path=config.firefox_driver, options=firefox_options) 

                elif self.driver == "safari":
                        if self.headless == True:
                                USI._logger(self, message=USI._pr_color(self, " Safari does not support headless mode", color="red"))
                                sys.exit()
                        self.browser = webdriver.Safari(executable_path=config.safari_driver) 

                # DOM set to poll for 15 sec 
                self.browser.implicitly_wait(15)

                # Log script info & results
                results = USI._pr_color(self, f"{self.company} {self.campaign_type} {self.site_id}", color="cyan") + f" - {self.driver.capitalize()}|{self.device_type.capitalize()} " + USI._pr_color(self, " Running...", color="green")
                USI._logger(self, message=results)
                
        

        def _precheck_data(self, elements, data_type, locate_by="css"):
                allowed_locator = {"xpath", "css"}
                if locate_by not in allowed_locator:
                        USI._terminate_script(self, name="Invalid Selector", message=f"{locate_by} is not a valid locator. Valid locators are {allowed_locator}")
                elif data_type[1] != type(elements):
                        USI._terminate_script(self, name="Wrong data type", message=f"{data_type[0]} accpets a {data_type[1]}")
                else:
                        pass

        def _pr_color(self, text, color):
                if color == "green":
                        return f"\033[32m{text}\033[00m"
                elif color == "red":
                        return f"\033[31m{text}\033[00m"
                elif color == "cyan":
                        return f"\033[96m{text}\033[00m"
                elif color == "yellow":
                        return f"\033[93m{text}\033[00m"
                elif color == "blue":
                        return f"\033[34m{text}\033[00m"
                else:
                        return f"\033[97m{text}\033[00m"



        # logger handles all prints statementsto the terminal. 
        # Also doubles as a function to log error to a log file if _terminate test is executed. 
        def _logger(self, message="", log_to_file="False"):
                if message != "":
                        print(message)
                        self.error_report.append(message)
                        global test_count
                        test_count += 1
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
                        USI._logger(self, message=USI._pr_color(self, "Test Aborted - Results", color="yellow") +
                        "\n  " +  f"⚠️  {name}: {element} " +  USI._pr_color(self, message, color="yellow"))
                elif element == "":
                        USI._logger(self, message=USI._pr_color(self, "Test Failed - Results", color="red") +
                        "\n  " + USI._pr_color(self, "✘ ", color="red") + f"{name} " + USI._pr_color(self, message, color="red"), log_to_file=True)
                else:
                        USI._logger(self, message=USI._pr_color(self, "Test Failed - Results", color="red") +
                        "\n  " + USI._pr_color(self, "✘ ", color="red") + f"{name}: {element} - "+ USI._pr_color(self, message, color="red"), log_to_file=True)
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


        # Navigates to url: Accepts 1 string argmuent
        def navigate_url(self, url):
                try:
                        self.browser.get(url)
                        USI._logger(self, message="Navigating to ".ljust(40, '.') + USI._pr_color(self, f" {url} ✓", color="blue"))
                except Exception:
                        USI._terminate_script(self, name="initiate_test()", message="USI class instantiation falied")


        # button click: accepts a dict of button/link names & selector
                # {'Add to cart button':'#cart'}
        def click(self, element_data, locate_by="css", node_index=-1):
                        data_type = ["click(): element_data", dict]
                        USI._precheck_data(self, element_data, data_type, locate_by)
                        
                        if locate_by == "css":
                                for name, button in element_data.items():
                                        try:
                                                if node_index >= 0:
                                                        sleep(5) # give webdriver time to parse nodelist
                                                        self.browser.find_elements_by_css_selector(button)[node_index].click()
                                                        USI._logger(self, message=f"{name} ".ljust(40, '.') + USI._pr_color(self, " Clicked ✓", color="green"))
                                                else:
                                                        WebDriverWait(self.browser, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button))).click()
                                                        USI._logger(self, message=f"{name} ".ljust(40, '.') + USI._pr_color(self, " Clicked ✓", color="green"))
                                        except Exception as msg:
                                                        messg = str(msg)
                                                        messg = messg.replace(' ', '')
                                                        messg = ''.join(messg.split())
                                                        if(messg == "Message:"):
                                                                msg="Element could not be located"
                                                        USI._terminate_script(self, name=name, element=button, message=msg)

                        elif locate_by == "xpath":   
                                for name, button in element_data.items():
                                        try:
                                                        WebDriverWait(self.browser, 40).until(EC.element_to_be_clickable((By.XPATH, button))).click()
                                                        USI._logger(self, message=f"{name} ".ljust(40, '.') + USI._pr_color(self, " Clicked ✓", color="green"))
                                        except Exception as msg:
                                                        messg = str(msg)
                                                        messg = messg.replace(' ', '')
                                                        messg = ''.join(messg.split())
                                                        if(messg == "Message:"):
                                                                msg="Element could not be located"
                                                        USI._terminate_script(self, name=name, element=button, message=msg)
                

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
                data_type = ["input_text(): input_date", dict]
                USI._precheck_data(self, input_data, data_type, locate_by)

                if locate_by == "css":
                        for name, value in input_data.items():
                                try:
                                        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value[0]))).send_keys(value[1])
                                        USI._logger(self, message=f"{value[1]} ".ljust(40, '.') + USI._pr_color(self, f" Entered into {name} ✓", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=value[0])
                elif locate_by == "xpath":
                        for name, value in input_data.items():
                                try:
                                        # self.browser.find_element_by_xpath(value[0]).send_keys(value[1])
                                        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, value[0]))).send_keys(value[1])
                                        USI._logger(self, message=f"{value[1]} ".ljust(40, '.') + USI._pr_color(self, f" Entered into {name} ✓", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=value[0])



        # Inputs email address for LC modal (USI)
                # takes email address string and optional seconds arg
        def lc_input(self, email, selector="#usi_content #usi_email_container #usi_email", sec=60):
                data_type = ["lc_input(): email", str]
                data_type2 = ["lc_input(): sec", int]
                validate_items = [selector, email]
                [USI._precheck_data(self, item, data_type) for item in validate_items]
                USI._precheck_data(self, sec, data_type2)
                        

                try:
                        WebDriverWait(self.browser, sec).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).send_keys(email)
                        USI._logger(self, message=f"LC modal: {email} ".ljust(40, '.') + USI._pr_color(self, " Entered into LC ✓", color="green"))
                except Exception:
                        USI._terminate_script(self, name="LC input field", element=selector)


        # Hover & button click: accepts a dict of a visible element selector and non-visible selector 
                # {"checkout button": ['#menuBar', '#dropDown a'}
        def hover_and_click(self, elements, locate_by="css"):
                data_type = ["hover_and_click(): elements", dict]
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
                                USI._logger(self, message="Visible element ".ljust(40, '.') + USI._pr_color(self, " Hovered ✓", color="green") +
                                "\n" + f"{name} ".ljust(40, '.') + USI._pr_color(self, " Clicked ✓", color="green"))


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
                                USI._logger(self, message="Visible element ".ljust(40, '.') + USI._pr_color(self, " Hovered ✓", color="green") +
                                "\n" + f"{name} ".ljust(40, '.') + USI._pr_color(self, " Clicked ✓", color="green"))


        # Submit Button Click: Accepts css selector or default value will be used (USI)
        def click_cta(self, selector="#usi_content .usi_submitbutton", clicks=1):
                data_type = ["click_cta(): selector", str]
                data_type2 = ["click_cta(): clicks", int]
                USI._precheck_data(self, selector, data_type)
                USI._precheck_data(self, clicks, data_type2)
                
                for _ in range(clicks):
                        try:
                                WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                                USI._logger(self, message="CTA ".ljust(40, '.') + USI._pr_color(self, " Clicked ✓", color="green"))
                        except Exception:
                                USI._logger(self, message="CTA ".ljust(40, '.') + USI._pr_color(self, " Not found", color="red"))
                                USI._terminate_script(self, name="CTA", element=selector)


        def mobile_cta(self):
                USI.execute_js("usi_js.submit();", "Mobile CTA clicked")


        # Select box function 
                # Accpets a dict of name and list of css selector & value or text
                #select_option({"Plug type select":["#pa_plug-type","us-plug"]}, select_by="value")
        def select_option(self, select_data, select_by="value"):
                data_type = ["checkbox(): select_data", dict]
                USI._precheck_data(self, select_data, data_type)

                for name, value in select_data.items():
                        if select_by == "value":
                                select = Select(self.browser.find_element_by_css_selector(value[0]))
                                select.select_by_value(value[1])
                                USI._logger(self, message=f"Value: {value[1]} ".ljust(40, '.') + USI._pr_color(self, f" Selected from {name} ✓", color="green"))
                        elif select_by == "text":
                                select= Select(self.browser.find_element_by_css_selector(value[0]))
                                select.select_by_visible_text(value[1])
                                USI._logger(self, message=f"Value: {value[1]} ".ljust(40, '.') + USI._pr_color(self, f" Selected from {name} ✓", color="green"))


        # Launches Modal: No args accepted (USI)
        def launch_modal(self, proactive=False, sec=5):
                data_type = ["launch_modal(): sec", int]
                USI._precheck_data(self, sec, data_type)
                if proactive == False:
                        try:
                                tries = 3 # loop for .usi_display 3 times at 3 second intervals
                                while self.browser.find_element_by_css_selector(".usi_display"):
                                        try:
                                                self.browser.execute_script("usi_js.display();")
                                                USI._logger(self, message="USI modal ".ljust(40, '.') + USI._pr_color(self, " Launched ✓", color="green"))
                                                break
                                        except Exception:
                                                pass
                                        sleep(3)
                                        tries -= 1
                                        print(f"Searching for modal..{tries} attempts left")
                                        if tries == 0:
                                                USI._terminate_script(self, name="USI Modal", message="Launch conditions not met; usi_js.display() is undefined", element=".usi_display")
                        except Exception:
                                USI._terminate_script(self, name="USI Modal", message="No View.jsp loaded on this page", element=".usi_display")
                elif proactive == True:
                        if sec == "":
                                USI._terminate_script(self, name="Proactive Launch", message="Proactive launches must pass a proactive_wait INT argument", element="Bad Data" )
                        else: 
                                USI.halt_execution(self, sec)
                                try:
                                        self.browser.find_element_by_css_selector(".usi_display.usi_show_css")
                                        USI._logger(self, message="USI Modal ".ljust(40, '.') + USI._pr_color(self, " Launched ✓", color="green"))
                                except JavascriptException:
                                        USI._terminate_script(self, name="USI Modal", message="Proactive Launch conditions not met", element=".usi_display")

        # Executes any javascript code
        def execute_js(self, script, name="JS code"):
                data_type = ["execute_js() script", str]
                USI._precheck_data(self, script, data_type)

                USI.halt_execution(self, sec=5)
                try:
                        self.browser.execute_script(script)
                        USI._logger(self, message=f"{name} ".ljust(40, '.') + USI._pr_color(self, " Executed ✓", color="green"))
                except JavascriptException:
                        USI._terminate_script(self, name=name, message="Execution failed", element=script)


        # Appends string url parameters
        def append_url(self, param, wait_param_exist=False, overide=False, url=""):
                #  Check url data type
                data_type = ["append_url(): param", str]
                USI._precheck_data(self, param, data_type)

                page_url = ""
                if wait_param_exist == True:
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.url_contains(url)):                
                                        url_found = True
                                        USI._logger(self, message=f"URL Param: {url}".ljust(40, '. ') + USI._pr_color(self, "  Exists", "green"))
                        except Exception:
                                url_found = False
                                USI._terminate_script(self, name="URL Param", element=url, message="URL Parameter Not Found")
                
                if wait_param_exist == False or wait_param_exist == True and url_found == True:
                        if overide == True:
                                page_url = self.browser.current_url + param
                        elif '?' in self.browser.current_url:
                                page_url = self.browser.current_url + "&" + param
                        else:
                                page_url = self.browser.current_url + "?" + param
                        USI.navigate_url(self, page_url)




        # checks if boostbar exists
                # accepts one param if named different them the default
        def boostbar_check(self, boostbar="#usi_boost_container", bb_close_selector=""):
                data_type = ["boostbar_check(): boostbar", str]
                USI._precheck_data(self, boostbar, data_type)

                try:
                        if WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, boostbar))):
                                USI._logger(self, message="Boostbar ".ljust(40, '.') + USI._pr_color(self, " Exists ✓", "green"))
                                if bb_close_selector != "":
                                        USI.click(self, element_data={"Close boost bar":bb_close_selector})
                except Exception:
                        USI._terminate_script(self, name="Boostbar", element=boostbar)


        #  Checks if a tab (TT or LC) can toggle
                # Default params should suffice, change if needed  
        def tab_click(self, decision_selector=".usi_tab_opened", tab="#usi_tab"):
                data_type = ["tab_click()", str]
                validate_items = [decision_selector, tab]
                [USI._precheck_data(self, item, data_type) for item in validate_items]

                try:
                        USI.click(self, element_data={"USI tab":tab})
                except Exception:
                        USI._terminate_script(self, name="tab", element="#usi_tab")
                
                try:
                        if self.browser.find_element_by_css_selector(decision_selector):
                                USI._logger(self, message="Tab ".ljust(40, '.') + USI._pr_color(self, " Opened", "green"))
                except Exception:
                        USI._terminate_script(self, name="tab_opened class", element=".usi_tab_opened")
                        
                

        # Retrieves session cookie
                #accepts a str of the cookie you want ot retrieve
        def get_cookie(self, cookie):
                data_type = ["get_cookie()", str]
                USI._precheck_data(self, cookie, data_type)

                USI.halt_execution(self, sec=3)
                if self.browser.get_cookie(cookie) is None:
                        USI._logger(self, message="Could not retrieve cookie")
                else:
                        cookie_name = self.browser.get_cookie(cookie)
                        cookie_value = cookie_name["value"]
                        USI._logger(self, message=f"{cookie}: " + USI._pr_color(self, cookie_value, "blue"))
        

        #   Check for coupon validation
                ''' 
                Accpets a type of validate_by which can be an "element", "message", or
                element_message. message & element_message must pass message_text.
                EX. 
                coupon_validation(validate_by="element_message", message_text='Coupon code applied.', target_element=".messages")
                '''
                        # coupon_validation(self, validate_by="")
        def coupon_validation(self, validate_by, target_element, message_text="", locate_by="css"):
                data_type = ["coupon_validation()", str]
                validate_items = [validate_by, target_element, message_text, locate_by]
                [USI._precheck_data(self, item, data_type) for item in validate_items]


                if locate_by == "css":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, target_element))):
                                        USI._logger(self, message="Coupon code element ".ljust(40, '.') + USI._pr_color(self, " Valid ✓", color="green"))
                        except Exception:
                                USI._terminate_script(self, name="Coupon Element", element=target_element, message="In-valid validation element")
                       
                        if validate_by == "message" or validate_by == "element_message":                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, target_element), message_text)):
                                                USI._logger(self, message="Coupon code validation message ".ljust(40, '.') + USI._pr_color(self, f" Valid: {message_text} ✓", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name="Coupon Message", element=message_text, message="In-valid validation message")

                if locate_by == "xpath":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, target_element))):
                                        USI._logger(self, message="Coupon code element ".ljust(40, '.') + USI._pr_color(self, " Valid ✓", color="green"))
                        except Exception:
                                USI._terminate_script(self, name="Coupon Element", element=target_element, message="In-valid validation element")
                       
                        if validate_by == "message" or validate_by == "element_message":
                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.XPATH, target_element), message_text)):
                                                USI._logger(self, message="Coupon code validation message ".ljust(40, '.') + USI._pr_color(self, f" Valid: {message_text} ✓", color="green"))
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
                data_type1 = ["promo_data(): promo_data", list]
                data_type2 = ["discount_check(): discount_data", dict]
                USI._precheck_data(self, promo_data, data_type1)
                USI._precheck_data(self, discount_data, data_type2)
                
                # if discount_data != {}:
                if locate_by == "css":
                        for amount_name,element in discount_data.items():
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, element))).get_attribute("innerText"):
                                                USI._logger(
                                                        self, message=f"{amount_name} ".ljust(40, '.') + USI._pr_color(self, " Correct ✓", color="green")
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
                                                        self, message=f"{amount_name} ".ljust(40, '.') + USI._pr_color(self, " Correct ✓", color="green")
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
                        USI._logger(self, message=f"Discount amount: {format(promo_data[1], '.2f')} off ".ljust(40, '.') + USI._pr_color(self, " Correct", "green"))
                else:
                        USI._terminate_script(self, name="Discount: ", message=f"Correct Amount should be {totals[2]}", element=desired_value)



        # Closes usi modal (USI)
                # Accepts one string param if different from default
        def close_usi_modal(self, selector="#usi_default_close", locate_by="css"):
                data_type = ["checkbox()", str]
                USI._precheck_data(self, selector, data_type, locate_by)

                if locate_by == "css":
                        try:
                                WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
                                USI._logger(self, message="Modal ".ljust(40, '.') + USI._pr_color(self, " Closed", "green"))
                        except Exception:
                                USI._terminate_script(self, name="Close button", element=selector)
                if locate_by == "xpath":
                        try:
                                WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, selector))).click()
                                USI._logger(self, message="Modal ".ljust(40, '.') + USI._pr_color(self, " Closed", "green"))
                        except Exception:
                                USI._terminate_script(self, name="Close button", element=selector)


        ''' Checks to see if a desired element is present on the DOM and visible on page. 
            Can be used as a condition for another action. 
            Ex. check_element_visibility(self, element_name="Login Modal", selector="#login-modal", locate_by="css")
        '''
        def check_element_visibility(self, element_name, selector, text="", locate_by="css", client_modal=False):
                data_type = ["check_element_visibility()", str]
                validate_items = [element_name, selector, text, locate_by]
                [USI._precheck_data(self, item, data_type) for item in validate_items]

                if locate_by == "css":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))):
                                        USI._logger(self, message=f"{element_name}".ljust(40, '.') + USI._pr_color(self, " Exists ✓", "green"))
                                if client_modal == True:
                                        USI.click(self, {"Client modal X button":selector})
                        except Exception:
                                if client_modal == True:
                                        USI._logger(self, message=f"{element_name}".ljust(40, '.') + USI._pr_color(self, " Bypass Client Modal ✓", "yellow"))
                                else:
                                        USI._terminate_script(self, name=element_name, element=selector)
                        
                        if text != "":                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)):
                                                USI._logger(self, message=f"{element_name}: text ".ljust(40, '.') + USI._pr_color(self, f" Valid: {text} ✓", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=f"{element_name}: text", element=text, message="In-valid element text")
                elif locate_by == "xpath":
                        try:
                                if WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, selector))):
                                        USI._logger(self, message=f"{element_name}: {selector} ".ljust(40, '.') + USI._pr_color(self, " Element Located", "green"))
                        except Exception:
                                if client_modal == True:
                                        USI._logger(self, message=f"{element_name}".ljust(40, '.') + USI._pr_color(self, " Bypass Client Modal ✓", "yellow"))
                                else:
                                        USI._terminate_script(self, name=element_name, element=selector)
                        
                        if text != "":                                
                                try:
                                        if WebDriverWait(self.browser, 20).until(EC.text_to_be_present_in_element((By.XPATH, selector), text)):
                                                USI._logger(self, message=f"{element_name}: text ".ljust(40, '.') + USI._pr_color(self, f" Valid: {text} ✓", color="green"))
                                except Exception:
                                        USI._terminate_script(self, name=f"{element_name}: text", element=text, message="In-valid element text")
        

        # Checks if the desired monitor.js has loaded in the network.
        def siteID_load(self):
                tries = 3 # will try to refresh page 3 times to load email in broswer 
                while tries != 0:
                        try:
                                if self.campaign_type.lower() == "pc":
                                        self.browser.execute_script('usi_js_monitor["USI_siteID"]')
                                        self.site_id = self.browser.execute_script('return usi_js_monitor["USI_siteID"]')
                                else:
                                        self.browser.execute_script('usi_js.campaign.site_id')
                                        self.site_id = self.browser.execute_script('return usi_js.campaign.site_id')
                                USI._logger(self, message=f"Site id: {self.campaign_type} {self.site_id}".ljust(40, '.') + USI._pr_color(self, " Ready ✓", "green"))
                                break
                        except Exception:
                                sleep(5)
                                tries -= 1
                                USI._logger(self, message=f"Waiting for correct Site Id ".ljust(40, '.') + USI._pr_color(self, f" {tries} attempts left", "yellow"))
                        if tries == 0:
                                USI._terminate_script(self, name=f"Site ID {self.site_id}", message="Failed to load", element=".usi_display")

        
        # Open an email in a broswer window which can be use to check email links are working 
                #Accepts two strings of session name and element xpath for the email element (xpath MUST be used here).
                        #  usi_email_link(self, 
                        #       session="usi_sess_27176_739_1567110133125", 
                        #       element_xpath="")
        def email_link_follow(self, campaign_type, element_xpath, override_session_name="", new_window=True):
                data_type = ["usi_email_link()", str]
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
                        sleep(5)
                        tries -= 1
                        if tries == 0:
                                USI._terminate_script(self, name="Email url", element=campaign_type, message="Session not found")

                try:
                        USI.click(self, element_data={"Email hero link": element_xpath}, locate_by="xpath")
                except Exception:
                        USI._terminate_script(self, name="Hero Image", element=element_xpath, message="Email link not found")

                # In the event of an email link missing a target="_blank" attribute; set new_window argument to false
                if new_window == True:
                        self.browser.switch_to.window(self.browser.window_handles[1])


        ''' The check_product_rec function  checking if a our USI product rec's item name/price matches up 
        with the onsite name/price after CTA and redirect to product page. 
                check_product_rec(site_product_selectors=[".onsite_redirect_name", ".onsite_redirect_price"], 
                        usi_product_selectors=[".usi_product_name", ".usi_product_price"],
                        cta_selector=".usi_product_cta1" )        
                '''

        def check_product_rec(self, usi_product_selectors, site_product_selectors, new_window=True, cta_selector="#usi_content .usi_submitbutton"):
                data_type = ["check_product_rec()", list]
                validate_items = [usi_product_selectors, site_product_selectors]
                [USI._precheck_data(self, item, data_type) for item in validate_items]

                # specifies whether to test both name and price or just name
                test_type = "both"
                if usi_product_selectors[0] != None and usi_product_selectors[1] != None:
                        product_rec_name = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, usi_product_selectors[0]))).get_attribute("innerText")
                        product_rec_price = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, usi_product_selectors[1]))).get_attribute("innerText")
                elif usi_product_selectors[1] == None:
                        product_rec_name = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, usi_product_selectors[0]))).get_attribute("innerText")
                        test_type = "name_only"

                USI.click_cta(self, selector=cta_selector)

                if new_window == True:
                        self.browser.switch_to.window(self.browser.window_handles[1])

                if test_type == "name_only":
                        onsite_product_name = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, site_product_selectors[0]))).get_attribute("innerText")
                        
                        if product_rec_name == onsite_product_name:
                                USI._logger(self, message=f"Product Rec name => Onsite product name: \"{onsite_product_name}\" " + USI._pr_color(self, "  Correct", "green"))
                        else:
                                USI._terminate_script(self, name="Product Rec USI product name ".ljust(40, '.'), message="Not matching onsite product name")
                else:
                        onsite_product_name = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, site_product_selectors[0]))).get_attribute("innerText")
                        onsite_product_price = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, site_product_selectors[1]))).get_attribute("innerText")

                        if product_rec_name == onsite_product_name and product_rec_price == onsite_product_price:
                                USI._logger(self, message=f"Product Rec name & price ".ljust(40, '.') + USI._pr_color(self, " Correct", "green"))
                        elif product_rec_name == onsite_product_name and product_rec_price != onsite_product_price:
                                USI._terminate_script(self, name="Product Rec price ".ljust(40, '.'), message="Not matching onsite product price")
                        elif product_rec_name != onsite_product_name and product_rec_price == onsite_product_price:
                                USI._terminate_script(self, name="Product Rec name ".ljust(40, '.'), message="Not matching onsite product name")
                        elif product_rec_name != onsite_product_name and product_rec_price != onsite_product_price:
                                USI._terminate_script(self, name="Product Rec name & price ".ljust(40, '.'), message="Not matching onsite name/price")

        
        ''' 
        switch_tab will move to a desired tab when multiple are open.
        Default value is 1 from the left.(0 is considered the first tab)
        )
        '''
        def switch_tab(self, tab=1):
                data_type = ["switch_tab()", int]
                USI._precheck_data(self, tab, data_type)
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
                        USI._logger(self, message="Split Group: " + USI._pr_color(self, " USI ✓" , color="green"))
                        pass


        # Interacts with to page to enable launch on mobile (usi)
        def mobile_interact(self):
                self.browser.find_element_by_tag_name("body").click()


        # Simply refeshes a page
        def refresh_page(self, sec=0 ):
                self.browser.refresh()
                if sec > 0:
                        sleep(sec)
                USI._logger(self, message=USI._pr_color(self, " Page refreshed", color="blue"))


        # checkbox_data is used to click a checkbox 

        def checkbox(self, checkbox_data="", locate_by="css"):
                data_type = ["checkbox()", dict]
                USI._precheck_data(self, checkbox_data, data_type, locate_by)

                if locate_by == "css":
                        for name, selector in checkbox_data.items():
                                try:
                                        self.browser.find_element_by_css_selector(selector).click()
                                        USI._logger(self, message=f"{name}: {selector} ".ljust(40, '. ') + USI._pr_color(self, " Checked", "green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=selector, message="Checkbox could not be checked")
                elif locate_by == "xpath":
                        for name, selector in checkbox_data.items():
                                try:
                                        self.browser.find_element_by_xpath(selector).click()
                                        USI._logger(self, message=f"{name}: {selector} ".ljust(40, '. ') + USI._pr_color(self, " Checked", "green"))
                                except Exception:
                                        USI._terminate_script(self, name=name, element=selector, message="Checkbox could not be checked")
        

        # checks if a campaign is under the correct sale window for launch
        # Accepts an two string arguments of a state date and an end date
        def set_date_window(self, start_date, end_date):
                data_type = ["set_date_window()", str]
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
                        USI._terminate_script(self, name="Date Error", message=f"End date => {end_date} cannot be eariler then specified start date {start_date}", fail_pass=True)
                        

                if starting_date <= today <= ending_date:
                        pass
                elif starting_date > today:
                        USI._terminate_script(self, name="Campaign start Date", element=starting_date, message="Sale window for this campaign has not yet began", fail_pass=True)
                else:
                        USI._terminate_script(self, name="Campaign end date", element=ending_date, message="Sale window for this campaign had ended", fail_pass=True)


        # Takes screenshot
        def take_screenshot(self, screenshot_name="default.png"):
                self.browser.save_screenshot(f"{screenshot_name}.png")


        # Halts execution of script (last case scenario)
        def halt_execution(self, sec):
                sleep(sec)


        # Shuts down driver 
        def shutdown(self):
                complete_time = round((time() - start_time), 1)
                USI._logger(self, message=USI._pr_color(self, "Shutting down driver ".ljust(40, '.') + " Complete ✓", color="yellow"))
                sleep(3) # Static wait solely for UX
                self.browser.quit()
                USI._logger(self, message=USI._pr_color(self, "Test Complete - Results", color="green") +
                "\n  " + USI._pr_color(self, f"✓ {self.company} {self.campaign_type} {self.site_id} ", color="cyan") + 
                USI._pr_color(self, f"- {test_count - 1}/{test_count - 1} Tests PASSED ({complete_time}s)", color="green") + "\n")

