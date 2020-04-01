# Test Framework
### Framework for generating automated UI tests for Campaigns. 

## Requirements

* Python 3 (3.6 or higher)
  * https://www.python.org/downloads/
* Selenium WebDriver 
  * https://www.seleniumhq.org/download/ or use pip install selenium
* Termcolor
  * pip install termcolor
* Download browser drivers
    * https://www.seleniumhq.org/download/ (Framework currently supports Chrome, Firefox, and Safari)
    * Safari driver can be found at /usr/bin/safaridriver
* Text Editor or IDE of your choice


## Prerequisites   

* Knowledge of HTML, CSS and Javascript.
* Python 3 knowledge is helpful but NOT necessary, any programming language with basic knowledge such as arrays, objects, arguemnts and parameters will do. 
* Strong knowledge of traversing the DOM, CSS selectors, and XPATH.
* Knowledge of navigating a browser console.
* Comfortable working in a terminal or windows cmd enviroment. 

  
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


#### Sample Lead Capture Test
```Python
#### Alwyas import main ####
import main

try:
        inkjets_lc_26632 = main.USI("123Inkjets", "LC", "26632", headless=False, log_file=False)
        inkjets_lc_26632.initiate_test()
        inkjets_lc_26632.navigate_url("https://www.123inkjets.com/Samsung/Compatible/Laser-Toner/Drum/MLT-R116/22770-Product.html?datahound=1")
        inkjets_lc_26632.launch_modal()
        inkjets_lc_26632.lc_input("jdran@mail.com")
        inkjets_lc_26632.click_cta()
        inkjets_lc_26632.email_link_follow("lc", "/html/body/div[2]/div[1]/table/tbody/tr/td/table/tbody/tr/td/a")
        inkjets_lc_26632.click({
                "First HP item":".products-grid ul li.item:first-child .hide480 li:first-child a",
                "Add to cart":".add_to_cart_btn",
                "View Cart":".cart-container .button_primary"
        })
        inkjets_lc_26632.coupon_validation(
                validate_by="element_message",
                target_element=".messages span[ng-bind='messaging.success']",
                message_text="COUPON CODE \"Q4INK123\" WAS APPLIED."
                )
        inkjets_lc_26632.shutdown()  
except BaseException:
        pass
```

#### Running multiple tests
If two or more tests need to be ran in the same file; each
test must be wrapped in a try/execpt block.
```Python

# Test Name 1 
 try:
         company_tt_12345 = USI("Company", "TT", "12345", headless=True, log_file=False)
         company_tt_12345.initiate_test()
         company_tt_12345.navigate_url("wwww.company.com")
         company_tt_12345.launch_modal()
         company_tt_12345.click_cta()
         company_tt_12345.shutdown()  
 except BaseException:
         pass

# Test Name 2 
try:
         company_lc_12345 = USI("Company", "LC", "678910", headless=True, log_file=False)
         company_lc_12345.initiate_test()
         company_lc_12345.navigate_url("wwww.companytwo.com")
         company_lc_12345.launch_modal()
         company_lc_12345.lc_input("emailName@mail.com")
         company_lc_12345.click_cta()
         company_lc_12345.shutdown()  
except BaseException:
        pass
```

#### Succesful Test Output
A succesful test script will display a green Test Complete message.
![Succesful Demo](https://raw.githubusercontent.com/Duran914/images/master/demo_lc.png)


#### Failed Test Output
A test script will terminate if an error is thrown.
Possible Errors Include:
  * Elements that could not be located. 
  * Passing incorrect data types.
  * Missing Arguments.
  * Incorrect driver instantiation.
  * Campaign launch rules not being met.
  * Selenium errors. 

![Failed demo](https://raw.githubusercontent.com/Duran914/images/master/demo_lc_fail.png)


### Log file output 
* When a test has failed, a txt file named QA_Errors_{current_date}.txt will be created.
* The log file will contain the same output as a failed test output would in the terminal.
* Log file writting can be toggled within initiate_test() while developing a test script. 

## USI API 

Before writing a test script you must create an instance of the USI class for EVERY campaign.
```Python
ace_TT_12345 = main.USI("Ace", "TT", "12345", driver="chrome", device_type="desktop", headless=False, log_file=True)
```
* Requires company name, campaign type, site id.
* driver can accept "chrome", "firefox", "safari"; default is set to "chrome".
* device_type accepts "desktop" or "mobile";  default is "desktop". Mobile execution only works on chrome. 
* headless accepts a boolean of "True" or "False"; default is False. Only chrome and firefox support headless.
* log_file will write errors to a log file. Accepts a boolean of true or false. Default is set to True.
Acceptable values are "green", "red", and None. Strictly for visual.

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
click({"Add to Cart Button":"#addBtn"}, locate_by="css", node_index="")
```
* Accepts three arguments 
  * Accepts a dictionary (object) of a element name as a key and a selector as its value. Mulitple objects can be passed if clicking through numerous elements. 
  * locate_by requires a string argument of either "css" or "xpath"; css is the default.
  * node_index accepts a number argument, use when a desired element is returning a node list. node_index=0 will click on the first element in the node list. 
  Hint: Use document.querySelectorAll() in the console to determine if an element is returning a node list. 


#

### hover_and_click()
The hover_and_click function hovers over any specifed element and clicks the desired element once is appears.

#### *Example:*<br> 
```Python
hover_and_click({"checkout button": ['#menuBar', '#dropDown a'}, locate_by="css")
```
* Accepts two arguments 
  * A dictionary (object) of a element name as a key and an array of the visible element selector and the non-visible selector.
  * locate_by requires a string argument of either "css" or "xpath"; css is the default


#

### click_cta()
The click_cta function will click a CTA button.

#### *Example:*<br> 
```Python
click_cta(selector="#usi_content .usi_submitbutton", clicks=1)
```
* Accepts two argument of a selector and clicks 
  * selector accepts a string of a css selector; has a default selector of "#usi_content .usi_submitbutton".
  * clicks accepts a number argument of a desired amount of times to click a CTA.  Has a default value of 1, a different value is only necessary when a cta needs to be clicked more then once and shares the same selector value.

#

### input_text()
The input_text function inserts text into any input field.

#### *Example:*<br> 
```Python
input_text({"Email-address": ["#formFirstname", "Johnny"]}, locate_by="css")
```
* Accepts two arguments 
  * A dictionary (object) of a element name as a key and an array of selector & text as values. Mulitple objects can be passed if needed, such as filling out numerous input fields.
  * locate_by requires a string argument of either "css" or "xpath"; css is the default

#

### lc_input()
The lc_input function inserts an email address into an LC modal.

#### *Example:*<br> 
```Python
lc_input("jdran@mail.com", selector="#usi_content #usi_email_container #usi_email")
```
* Requires a string argument of an email address. 
* Accpets a default argument of a selector, default is "#usi_content #usi_email_container #usi_email" and should
for most LCs.

#

### launch_modal()
The launch_modal function launches an usi TT or LC modal. 

#### *Example:*<br> 
```Python
launch_modal()
```
* No arguments accepted.

#

### select_option()
The select_option function selects an option from a select menu. Will only work for HTML select elements.
 
 
#### *Example:*<br> 
```Python
select_option(select_data={"Size select":[".select-size", "large"]}, select_by="text")
```
* Accepts two arguments of the following
  * select_data requires a dictionary of a name of the select field as a key and an array of selector and value beening scraped for. 
  * select_by accepts a argument of text or value and will scrape the dom based on the innerHTML of the field or its value atrribute; "value" is the default. 

#

### append_url()
The append_url function appeands a parameter to the current url and navigates to the new url.

#### *Example:*<br>
```Python
append_url(param="usi_enable=1", wait_param_exist=False, url=")
```
* Accepts three arguments.
  * param takes a string argument, query components "?" and "&" do not need to be passed in argument.
  * wait_param_exist accepts a boolean argument, True will set a WebdDriverWait to poll until a parameter exists in the URL.
  * url accepts a string argument of string of text that should be present in the url. If the string of text exists, the param string 
  will be inserted into the current url. 

#

### coupon_validation()
The coupon_validation function checks if a coupon code is valid.

#### *Example:*<br> 
```Python
coupon_validation(validate_by="element_text", target_element=".coupon-valid", message_text="Promo code is valid!", locate_by="css")
```

* Accepts four arguments of the following
  * validate_by
    * validate_by="element" checks for validation by an element selector.
    * validate_by="text" checks for validation by a string of text.
    * validate_by="element_text" checks for validation by an element selector and string of text.
  * target_element accepts a string argument of a selector.
  * message_text accepts a string of text to check validation.  An argument must be passed when validating by "text" or "element_text".
  * locate_by requires a string argument of either "css" or "xpath"; css is the default.

#

#

 ### check_product_rec()
The check_product_rec function checks if our USI product rec's item name/price matches up 
with the onsite name/price after CTA has redirected to its respective product page.

 #### *Example:*<br> 
 ```Python
 check_product_rec(usi_product_selectors=[".usi_product_name", ".usi_product_price"], site_product_selectors=[".onsite_name", ".onsite_price"], 
cta_selector=".usi_product_cta1", new_window=True) 
 ```
 * Accepts 4 arguments 
   * usi_product_selector accepts a list of two css selectors, name selector and price selector from our USI modal
   * site_product_selectors accpets a list of the css selector of the onsite name and price of the product you are checking against. Scrape these selectors from the page that the CTA has redirected you too.
   * cta_selector accpets a string argument of a the CTA css selector for a product rec item.
   * new_window accpets a boolean. Set True if rec CTA open in a new window, False for the same window, True is the default

#

#

 ### discount_check()
 The discount_check function calculates discounts and subtotals. Purpose is to check if the correct promotion amount.
 is being given. The coupon_validation() is normally sufficient to check a coupon code's vadility, use only if coupon_validation is not sufficient.

 #### *Example:*<br> 
 ```Python
discount_check(promo_data=["percent", .10], discount_data={"Subtotal":"#selector","Discount":"#selector","Grand Total":"#selector"})
 ```
 * Accepts 2 arguments  promo_date and discount_data
   * promo_data accepts a list of string argument of either "precent" for a percentage discount or "fixed" for a fixed dollar amount.
   * dicount_data accepts a dictionary, keys should be Subtotal, Discount and Grand total with thier value being thier associated css selectors.

 #

### split_test_check()
The split_test_check function determines if a split test campaign is "USI" or "CONTROL". Script will abort if split test is control group.
When a split test results in the control group the test will abort as a warning. Will not be recorded as a failed test.

#### *Example:*<br> 
```Python
split_test_check(dice_roll="usi_dice_roll27248")
```
* Accepts on string argument of the dice_roll cookie name. Naming convention for dice roll is as follows; usi_dice_roll{site id}

#

### email_link_follow()
The email_link_check function opens a LC or PC email and clicks on a specified element by XPATH. Best practive is to scrape for
the first modal a link image as it is likely to stay the same. 
```Python
usi_email_link(campaign_type="lc", element_xpath="/html/body/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/a", override_session_name="", new_window=True)
```
* Accepts four string arguments.
  * campaign_type accepts a string argument of either "lc" or "pc".
  * element_path accpets a string argument of the desired element to click on and follow back to website. Must use an xpath selector as our mjml email templetes do not have classnames or ids.
  * override_session_name accepts an optional argument of a session's cookie name if they're not using their conventional session names.
  * new_window accepts an optional argument of true or false, should only be "False" when an email link is missing a target="_blank" attribute.

#

### check_element_visibility()
The check_element_visibility function checks if a desired element is present on the DOM and visible on page.

#### *Example:*<br> 
```Python
check_element_visibility(element_name="Login Modal", selector="#login-modal", locate_by="css")
```
* Accepts 3 arguments 
  * element_name accepts a string argument of a name for the element.
  * selector accepts a string argument of the element selector class/id.
  * locate_by accpets a string arguemnt of either css or xpath, default is css.

#

### get_cookie()
The get_cookie function will retrieve a cookie. 

#### *Example:*<br> 
```Python
get_cookie("USI_session")
```
* Requires a single string argument of a cookie name.

#

### execute_js()
The execute_js function will execute javascript. 

#### *Example:*<br> 
```Python
execute_js('alert("Hello World");', "Alert box for hello world")
```
* Requires a string of JS code.
* An optional string argument of name can be passed to specify what the javascript's code intended action is. Default will be "JS code".

#

### set_date_window()
The set_date_window function checks if a campaign is under the correct sale window date range.
Function should be called immediately after the initiate_test() function.
When a campaign is out of the specified date range, the test will be aborted. 


#### *Example:*<br> 
 ```Python
set_date_window(start_date="2019-12-10", end_date="2019-12-20")
 ```
 * Accepts two string arguments of a state date and an end date. Date format should be year-month-day; ex. 2019-12-20.

#

### take_screenshot()
The take_screenshot function takes a screenshot of the screen, .png file type. 

#### *Example:*<br> 
```Python
take_screenshot("screenshot_name")
```
* Accepts a string of the screenshot name.

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
* Accepts two default arguments 
  * decision_selector checks for an exepected classname/id after a tab is clicked. Default ".usi_tab_opened", but can accept a different argument.
  * tab has a default seletor of "#usi_tab" for a usi modal tab but can accept a different selector if needed.

#

### boostbar_check()
The boostbar_check function checks if a boost bar has launched.

#### *Example:*<br> 
```Python
boostbar_check(selector="#usi_boost_container")
```
* Accepts a string argument of selector, default is "#usi_boost_container".

#

### switch_tab()
The switch_tab function will change to a specific tab when multiple are open. Tabs start at zero. 

#### *Example:*<br> 
```Python
witch_tab(tab=1)
```
* Accepts a single argument
  *  tab accepts a int argument of the desired tab you want to switch to. 1 is the default tab. 

#

### mobile_interact()
The mobile_interact function interacts with a mobile page to enable our backtrap to function properly on Chrome

#### *Example:*<br> 
```Python
mobile_interact()
```
* No arguments accepted

#

### halt_execution()
The halt_execution function stops execution for a predefined amount of time.<br>
*WARNING: Use with caution, a thread.sleep can be unreliable and slow down tests. All functions have a dynamic 20s wait time to poll the DOM. Use only as a last case scenario. Try using wait_for_element_visibility if you are waiting for an element to appear in the DOM. 

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
* No arguments are accepted.

