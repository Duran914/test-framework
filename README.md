# Test Automation Library 
### Library for generating automating UI tests for Campaigns. 

## Requirements

* Python 3 (3.6 or higher)
  * https://www.python.org/downloads/
* Selenium WebDriver 
  * https://www.seleniumhq.org/download/ or use pip install selenium
* Termcolor
  * pip install termcolor
* Download browsers Drivers
    * https://www.seleniumhq.org/download/ (Library only supports Chrome, Firefox, and Safari)
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

Before writing webdriver actions you must create an instance of the USI class.
```Python
ace_TT_12345 = main.USI("Ace", "TT", "12345", driver="chrome", device_type="desktop", headless=False)
```
* Requires company name, campaign type, site id.
* driver can accept "chrome", "firefox", "safari"; default is set to "chrome".
* device_type accepts "desktop" or "mobile";  default is "desktop". Mobile execution only works on chrome. 
* headless accepts a boolean of "True" or "False". False is default. Only chrome and firefox support headless.

### initiate_test()
The initiate_test function must come immediately after creating a new instance of the USI class. This function creates all
necessary configurations for webdriver. Script will fail without this function  

#### *Example:*<br> 
```Python
initiate_test()
```
* No arguments required, all nessasary data should be passed after creating a new instance of the USI class.

#

### navigate_url()
The navigate_url function navigates to a specified url. 

#### *Example:*<br> 
```Python
navigate_url("http://www.ace.com")
```
* Requires a string url argument.

#

### click()
The click function clicks an any specifed link, button etc.

#### *Example:*<br> 
```Python
click({"Add to Cart Button":"#addBtn"})
```
* Accepts an dictionary(Object) of a element name as a key and a selector value. Mulitple objects can be passed if clicking thorugh numerous elements. 

#

### click_cta()
The click_cta function will click a CTA button.

#### *Example:*<br> 
```Python
click_cta(selector="#usi_content .usi_submitbutton")
```
* Accepts a single argument of a selector, the default selector "#usi_content .usi_submitbutton" should work in most cases.

#

### input_text()
The input_text function inserts text into any input field.

#### *Example:*<br> 
```Python
input_text({"Email-address": ["#formFirstname", "Johnny"]})
```
* Accepts an dictionary of a element name as a key and a list of selector & text as values. Mulitple objects can be passed if needed. Such as filling out numerous input fields.

#

### lc_input()
The lc_input() function inserts an email address into an LC modal.

#### *Example:*<br> 
```Python
lc_input("jdran@mail.com", selector="#usi_content #usi_email_container #usi_email")
```
* Accepts a string argument of an email address, selector can be passed if default "#usi_content #usi_email_container #usi_email" is not sufficient.

#

### launch_modal()
The launch_modal() function launches a usi modal whether being a TT or LC.

#### *Example:*<br> 
```Python
launch_modal()
```
* No arguments accepted.

#

### click_when_visible()
The click_when_visible function will click on a specifed link, button, etc.., when it is visible in the DOM.

#### *Example:*<br> 
```Python
click_when_visible({"Modal checkout button":".checkout.modal-button"})
```
* Accepts a dictionary(object) element name as a key and a selector as a value.

#

### select_option()
The select_option function selects a option from a select menu. Will only work for HTML select elements.
 
 
#### *Example:*<br> 
```Python
select_option({"Size select":[".select-size", "large"]}, select_by="text")
```
* Accepts two arguments of the following
  * name of the select field as a key and a list of selector and option as values. 
  * select_by accepts a argument of text or value and will search for that option; value is the default. 

#

### append_url()
The append_url function appeands a parameter to the current url and navigates to the new url. Query components "?" and "&" do not need to be passed in argument.

#### *Example:*<br>
```Python
append_url("usi_enable=1")
```
* Accepts a single string argument.

#

### coupon_validation()
The coupon_validation function checks if a coupon code is valid by classname or string of text.

#### *Example:*<br> 
```Python
coupon_validation(validate_by="element_text", target_element=".coupon-valid", message_text="Promo code is valid!")
```

* Accepts three arguments of the following
  * validate_by
    * validate_by="element" => checks for validation by an element classname/id
    * validate_by="text" => checks for validation by a string of text
    * validate_by="element_text" => checks for validation by an element and string of text
  * target_element accepts a string argument of a classname or id
  * message_text accepts a string of text to check against for validation. A message_text argument must be passed for validate_by text & element_text

*Listing arguments name is not necessary, displayed for visualization.

#

### get_cookie()
The get_cookie function will retrieve a cookie. 

#### *Example:*<br> 
```Python
get_cookie("USI_session")
```
* Accepts a string of a cookie name.

#

### execute_js()
The execute_js function will execute javascript. 

#### *Example:*<br> 
```Python
execute_js('alert("Hello World");')
```
* Accepts a string of JS code.

#

### take_screenshot()
The take_screenshot function takes a screenshot of the screen, .png file type. 

#### *Example:*<br> 
```Python
take_screenshot("screenshot_name")
```
* Accepts a string of the screenshot name

#

### close_usi_modal()
The close_usi_modal function clics on an X button that closes an usi modal 

#### *Example:*<br> 
```Python
close_usi_modal(selector="#usi_default_close")
```
* Accepts a selector if the default "#usi_default_close" is not sufficient

#

### tab_click()
The tab_click function toggles a usi TT or LC tab

#### *Example:*<br> 
```Python
tab_click(decision_class=".usi_tab_opened", tab="#usi_tab")
```
* Accepts two default arguements
  * decision_class checks for an exepected classname after tab is clicked. Default ".usi_tab_opened", but can accept a different argument.
  * tab has a default seletor of "#usi_tab" for a usi modal tab but can accept a different selector if needed.

#

### boostbar_check()
The boostbar_check function checks that a boost bar had loaded.

#### *Example:*<br> 
```Python
boostbar_check(selector="#usi_boost_container")
```
* Accepts a selector if the default #usi_boost_container is not sufficient

#

### mobile_interact()
The mobile_interact() function interacts with mobile page to enable our backtrap to function properly

#### *Example:*<br> 
```Python
mobile_interact()
```
* No arguments accepted

#

### halt_execution()
The halt_execution function stop execution for a predefined amount of time.<br>
*WARNING: Use with caution, a thread.sleep can be unreliable and slow down tests. All functions have a predefined 15s wait time to poll the DOM. Use only as a last case scenario.

#### *Example:*<br> 
```Python
halt_execution(5)
```
* Accepts an INT argument for an amount of seconds to sleep webdriver. 

### shutdown()
The shutdown function gracefully shuts down the selenium webdriver. Must be added to the end of EVERY test script.

#### *Example:*<br> 
```Python
shutdown()
```
* No arguments are accepted
