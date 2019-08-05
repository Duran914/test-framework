# Test Automation Library 
### Library for generating automating UI tests for Campaigns. 

## Requirements

* Python 3 (3.6 or higher)
  * https://www.python.org/downloads/
* Selenium WebDriver 
  * https://www.seleniumhq.org/download/ or use pjp install selenium
* Termcolor
  * pip install termcolor
* Download browsers Drivers
    * https://www.seleniumhq.org/download/ (Currently only supports Chrome, Firefox, and Safari)
    * Safari driver can be found at /usr/bin/safaridriver
    
  
## Getting Started 
* Download or git clone main.py
* Create config.py file in same directory as main.py
  * Populate config.py as
    ```Python
      chrome_driver = "/path/to/driver/chromedriver" #replace with your local paths
      firefox_driver = "/path/to/driver/geckodriver" #replace with your local paths
      safari_driver = "/usr/bin/safaridriver"
    ```
    

### Running a Test 
Create a new test script.
Open a terminal and run test as follows. 
```Python
python3 my_first_test.py
```
### Example of a simple TT test
```Python
#### Alwyas import main ####
import main

teleStream = main.USI("telestream", "TT", "25502", driver="chrome", device_type="desktop", headless=False)
teleStream.initiate_test()
teleStream.navigate_url("http://www.telestream.net/wirecast/store.asp")
teleStream.click({"Mac add button":"#OneMac"})
teleStream.launch_modal()
teleStream.click_cta()
teleStream.shutdown()
```
 
## Test API

Before writting script you must create an instance of the USI class
```Python
ace_TT_12345 = main.USI("Ace", "TT", "12345", driver="chrome", device_type="desktop", headless=False)
```

### initiate_test()
The initiate_test function must come immediately after creating a new instance of the USI class. This function creates all
necessary configuration for the webdriver. 

#### *Example:*<br> initiate_test("Ace", "TT", "12345", driver="chrome", device_type="desktop", headless=False)
* Requires company name, campaign type, site id
* driver can accept "chrome", "firefox", "safari"; default is set to "chrome"
* device_type accepts "desktop" or "mobile";  default is "desktop". Mobile execution only work on chrome. 
* headless accepts a boolean of "True" or "False".

#

### navigate_url()
The navigate_url function navigates to a specified url. 

#### *Example:*<br> navigate_url("http://www.ace.com")
* Requires a string url to be pass

#

### click()
The click function clicks an any specifed link, button etc.

#### *Example:*<br> click({"Add to Cart Button":"#addBtn"})
* Accepts a dictionary(object) of name of the target element & a selector

#

### click_cta()
The click_cta function will click a CTA button.

#### *Example:*<br> click_cta(selector)
* Accepts a single argument of a selector, the default selector "#usi_content .usi_submitbutton" should work in most cases.

#

### input_text()
The input_text function inserts text into any input field.

#### *Example:*<br> input_text({"Email-address": ["#formFirstname", "Johnny"]})
* Accepts an dictionary of a "name" as a key and list of "selector" and "text" as values.

#

### lc_input()
The lc_input() function inserts an email address into an LC modal

#### *Example:*<br> lc_input("jdran@mail.com", selector)
* Accepts a string argument of an email address, selector can also be passed if default #usi_content #usi_email_container #usi_email is not sufficient

#

### launch_modal()
The launch_modal() function launches a usi modal whether being a TT or LC

#### *Example:*<br> launch_modal()
* No arguments accepted

#

### click_when_visible()
The click_when_visible function will click on a specifed link, button, etc when it is visible in the DOM. Such as a modal launching.

#### *Example:*<br> click_when_visible({"Modal checkout button":".checkout.modal-button"})
* Accepts a dictionary(object) of name of the target element & selector

#

### select_option()
The select_option function selects a option from a select menu. Will only work for HTML select elements.
 
 
#### *Example:*<br> select_option({"Size select":[".select-size", "large"]}, select_by="text")
* Accepts a dictionary of name of select field as a key and a list of select and option. select_by accepts a arg of text or value and will search for that option; value is the default. 

#

### append_url()
The append_url function simply appeands a parameter to the current url and navigates to the new url;  "?" and "&" do not need to be passed.

#### *Example:*<br> append_url("usi_enable=1")
* Accepts a single string.

#

### coupon_validation()
The coupon_validation function check if a coupon code is valid, by classname or string of text.

#### *Example:*<br> coupon_validation(validate_by="element_text", target_element=".coupon-valid", message_text="Promo code is valid!")
* Accepts three arguments of the following
  * validate_by
    * validate_by="element" => check for validation by an element class/id
    * validate_by="text" => check for validation by a string of text
    * validate_by="element_text" => check for validation by an element and string of text
  * target_element accepts a string argument of a classname or id
  * message_text accepts a string of text to check against. Argument must be passed for validate_by text/element_text
    

#

### get_cookie()
The get_cookie function will retrieve a cookie. 

#### *Example:*<br> get_cookie("USI_session")
* Accepts a string of a cookie name.

#

### execute_js()
The execute_js function will execute javascript. 

#### *Example:*<br> execute_js('alert("Hello World");')
* Accepts a string of JS code.

#

### take_screenshot()
The take_screenshot() function takes a screenshot of the screen, .png file type. 

#### *Example:*<br> take_screenshot("screenshot")
* Accepts a name of screenshot

#

### close_usi_modal()
The close_usi_modal() function click on an X button that closes an usi modal 

#### *Example:*<br> close_usi_modal(selector)
* Accepts a selector if the default #usi_default_close is not sufficient

#

### tab_click()
The tab_click function toggles a usi TT or LC tab

#### *Example:*<br> tab_click(decision_class=".usi_tab_opened", tab="#usi_tab")
* Accepts two default arguements
  * decision_class checks for an exepected class after tab is clicked
  * tab is is the default seletor for a usi modal tab but can be changed if needed.

#

### boostbar_check()
The boostbar_check function checks that a boost bar had loaded.

#### *Example:*<br> boostbar_check(selector)
* Accepts a selector if the default #usi_boost_container is not sufficient

#

### mobile_interact()
The mobile_interact() function interacts with mobile page to enable our backtrap to function properly

#### *Example:*<br> mobile_interact()
* No arguments accepted

#

### halt_execution()
The halt_execution function stop execution for a predefined amount of sleep.<br>
*WARNING: Use with caution, a thread.sleep can be unreliable and can slow down tests. Use only as a last case scenario.

#### *Example:*<br> halt_execution(sec=5)
* Accepts an INT argument for amount of seconds to sleep webdriver. 

### shutdown()
The shutdown() function gracefully shuts down the selenium webdriver. Must be added to the end of EVERY test script.

#### *Example:*<br> shutdown()
* No arguments are accepted
