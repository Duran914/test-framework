# Test Automation Library 
### Library for generating automated UI tests for Campaigns. 

## Requirements

* Python 3 (3.6 or higher)
  * https://www.python.org/downloads/
* Selenium WebDriver 
  * https://www.seleniumhq.org/download/ or use pip install selenium
* Termcolor
  * pip install termcolor
* Download browser drivers
    * https://www.seleniumhq.org/download/ (Library currently supports Chrome, Firefox, and Safari)
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
    

### Running a test script
Create a new test script.
Open a terminal and run test as follows. 
```Python
python3 my_first_test.py
```

#### Sample TT test
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

#### Running multiple tests
If two or more tests need to be ran in the same file; each
test must be wrapped in a try/execpt block.
```Python

# Test Name 1 
try:
        teleStream_tt_25502 = main.USI("Telestream", "TT", "25502", driver="chrome")
        teleStream_tt_25502.initiate_test()
        teleStream_tt_25502.navigate_url("http://www.telestream.net/wirecast/store.asp")
        teleStream_tt_25502.click({"Add to cart button":"#OneMac"})
        teleStream_tt_25502.launch_modal()
        teleStream_tt_25502.click_cta()
        teleStream_tt_25502.shutdown()
except BaseException:
        pass

# Test Name 2 
try:
        ...
        ...
except BaseException:
        pass
```

#### Succesful Test Output
A succesful test script will display a green Test Complete message.
![Succesful Demo](https://raw.githubusercontent.com/Duran914/images/master/demo_tt.png)


#### Failed Test Output
A test script will terminate if an error is thrown.
Possible Errors Include:
  * Elements that could not be located. 
  * Passing incorrect data types.
  * Missing Arguments.
  * Incorrect driver instantiation.
  * Campaign launch rules not being met.
  * Selenium errors. 

![Failed demo](https://raw.githubusercontent.com/Duran914/images/master/demo_failed.png)

## Test API 

Before writing a test script you must create an instance of the USI class for EVERY campaign.
```Python
ace_TT_12345 = main.USI("Ace", "TT", "12345", driver="chrome", device_type="desktop", headless=False)
```
* Requires company name, campaign type, site id.
* driver can accept "chrome", "firefox", "safari"; default is set to "chrome".
* device_type accepts "desktop" or "mobile";  default is "desktop". Mobile execution only works on chrome. 
* headless accepts a boolean of "True" or "False"; default is False. Only chrome and firefox support headless.

### initiate_test()
The initiate_test function must come immediately after creating a new instance of the USI class. This function creates all
necessary configurations for webdriver. Script will fail without this function.  

#### *Example:*<br> 
```Python
initiate_test()
```
* No arguments required, all nessasary data will be passed after creating a new instance of the USI class.

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
The click function clicks on any specifed link, button etc.

#### *Example:*<br> 
```Python
click({"Add to Cart Button":"#addBtn"})
```
* Accepts a dictionary (object) of a element name as a key and a selector as its value. Mulitple objects can be passed if clicking thorugh numerous elements. 

#

### click_cta()
The click_cta function will click a CTA button.

#### *Example:*<br> 
```Python
click_cta(selector="#usi_content .usi_submitbutton", clicks=1)
```
* Accepts two argument of a selector and click 
  * selector accepts a string of a css selector; has a default selector of "#usi_content .usi_submitbutton".
  * clicks accepts a number argument of a desired amount of times to click a CTA.  Has a default value of 1, a different value is only necessary when a cta needs to be clicked more then once and shares the same selector value.

#

### input_text()
The input_text function inserts text into any input field.

#### *Example:*<br> 
```Python
input_text({"Email-address": ["#formFirstname", "Johnny"]})
```
* Accepts an dictionary (object) of a element name as a key and an array of selector & text as values. Mulitple objects can be passed if needed, such as filling out numerous input fields.

#

### lc_input()
The lc_input function inserts an email address into an LC modal.

#### *Example:*<br> 
```Python
lc_input("jdran@mail.com", selector="#usi_content #usi_email_container #usi_email")
```
* Accepts a string argument of an email address, default is "#usi_content #usi_email_container #usi_email".

#

### launch_modal()
The launch_modal function launches a usi TT or LC modal. 

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
* Accepts a dictionary (object) of an element name as a key and a selector as a value.

#

### select_option()
The select_option function selects an option from a select menu. Will only work for HTML select elements.
 
 
#### *Example:*<br> 
```Python
select_option({"Size select":[".select-size", "large"]}, select_by="text")
```
* Accepts two arguments of the following
  * name of the select field as a key and an array of selector and option as values. 
  * select_by accepts a argument of text or value and will scrape the dom based that option; "value" is the default. 

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
    * validate_by="element" checks for validation by an element selector.
    * validate_by="text" checks for validation by a string of text.
    * validate_by="element_text" checks for validation by an element selector and string of text.
  * target_element accepts a string argument of a selector.
  * message_text accepts a string of text to check validation.  An argument must be passed when validating by "text" or "element_text".

*Listing arguments name is not necessary, displayed for visualization.

#

### split_test_check()
The split_test_check function determines if a split test campaign is "USI" or "CONTROL". Script will abort if split test is control group,

#### *Example:*<br> 
```Python
split_test_check(dice_roll="usi_dice_roll27248")
```
* Accepts on string argument of the dice_roll cookie name. Naming convention for dice roll is as follows; usi_dice_roll{site id}

#

### email_link_follow()
The email_link_check function opens a LC or PC email and clicks on a specified element by XPATH.
```Python
usi_email_link(session="usi_sess", element_xpath="/html/body/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/a")
```
* Accepts two string arguments.
  * session accepts a string argument of the cookie name of the desired session.
  * element_path accpets a string argument of the desired element to click on and follow back to site. Must use an xpath selector as
our mjml email templetes do not have classnames or ids.

#

### get_cookie()
The get_cookie function will retrieve a cookie. 

#### *Example:*<br> 
```Python
get_cookie("USI_session")
```
* Accepts a single string argument of a cookie name.

#

### execute_js()
The execute_js function will execute javascript. 

#### *Example:*<br> 
```Python
execute_js('alert("Hello World");', "Alert box for hello world")
```
* Accepts a string of JS code.
* An optional string argument of name can be passed to specify what the javascript's code intended action is. Default will be "JS code"

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
The close_usi_modal function closes a usi modal 

#### *Example:*<br> 
```Python
close_usi_modal(selector="#usi_default_close")
```
* Accepts a string argument of selector,  default is "#usi_default_close".

#

### tab_click()
The tab_click function toggles a usi TT or LC tab

#### *Example:*<br> 
```Python
tab_click(decision_selector=".usi_tab_opened", tab="#usi_tab")
```
* Accepts two default arguements
  * decision_selector checks for an exepected classname/id after a tab is clicked. Default ".usi_tab_opened", but can accept a different argument.
  * tab has a default seletor of "#usi_tab" for a usi modal tab but can accept a different selector if needed.

#

### boostbar_check()
The boostbar_check function checks if a boost bar has loaded.

#### *Example:*<br> 
```Python
boostbar_check(selector="#usi_boost_container")
```
* Accepts a string argument of selector, default is "#usi_boost_container".

#

### mobile_interact()
The mobile_interact function interacts with a mobile page to enable our backtrap to function properly

#### *Example:*<br> 
```Python
mobile_interact()
```
* No arguments accepted

#

### halt_execution()
The halt_execution function stops execution for a predefined amount of time.<br>
*WARNING: Use with caution, a thread.sleep can be unreliable and slow down tests. All functions have a predefined 15s wait time to poll the DOM. Use only as a last case scenario.

#### *Example:*<br> 
```Python
halt_execution(5)
```
* Accepts an INT argument for an amount of seconds to sleep webdriver. 

#

### shutdown()
The shutdown function gracefully shuts down the selenium webdriver. Must be added to the end of EVERY test script.

#### *Example:*<br> 
```Python
shutdown()
```
* No arguments are accepted
