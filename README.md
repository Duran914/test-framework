# Test Automation Library 
### Library for genereating automating UI tests for Campaigns. 

## Requirements

* Python 3 (3.6 or higher)
  * https://www.python.org/downloads/
* Selenium WebDriver 
  * https://www.seleniumhq.org/download/ or use pjp install selenium
* Termcolor
  * pip install termcolor
* Download browsers Drivers
    * https://www.seleniumhq.org/download/ (Currently only supports Chrome, Firefox, and Safari)
    * Safari driver driver can be found at /usr/bin/safaridriver
    
  
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
necessary configuration for the webdriver webdriver. 

#### *Example:*<br> initiate_test("Ace", "TT", "12345", driver="chrome", device_type="desktop", headless=False)
* Requires company name, campaign type, site id
* driver can accept "chrome", "firefox", "safari"; default is set to "chrome"
* device_type accepts "desktop" or "mobile";  default is "desktop". Mobile execution only work on chrome. 
* headless accepts a boolean of "True" or "False".



### navigate_url()
The navigate_url function navigates to a specified url. 

#### *Example:*<br> navigate_url("http://www.ace.com")
* Requires a string url to be pass

#

### click()
The click function clicks an any specifed link, button etc.

#### *Example:*<br> click({"Add to Cart Button":"#addBtn"})
* Accepts a dictionary(object) of name of the target element & a selector

