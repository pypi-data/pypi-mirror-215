## [Browser activities](browser-manager)
### [1. Chrome.py](browser-manager/chrome.py)  
Here you can find ChromeBrowser class. 
This class is used to create a browser object. 
It Heritages from the Chrome class and implements some custom methods to make browser automation easier.

#### Arguments:
1. driver_path: path to the driver
2. undetectable: if True, the browser will not be detected by antispam systems.
 
#### Attributes:
1. driver_path: path to the driver
2. undetectable: if True, the browser will not be detected by antispam systems.
3. chrome_version: version of chrome
4. options: options for the browser

#### Custom Methods:
1. open(): open the browser and load defined options.
2. ignore_images(): ignore images in the browser.
3. ignore_popups(): ignore popups in the browser.
4. ignore_notifications(): ignore notifications in the browser.
5. ignore_errors(): ignore errors in the browser.
6. headless(): open the browser in headless mode.
7. save_cookies(): save the cookies of the browser.
8. load_cookies(): load the cookies of the browser.
9. set_proxy(proxy): set a proxy for the browser.
10. set_user_agent(user_agent): set a user agent for the browser.
11. set_profile(path): set a profile for the browser.
12. scrolldown(h): scroll down to % height of the page .
13. scrollup(h): scroll up to % height of the page .
14. scroll_to_element(element): scroll to the element.
15. set_download_folder(folder): set the download folder.
16. element_exists(element): check if the element exists.
17. add_tab(): add a new tab.
18. get_tabs(): get the tabs of the browser.
19. close_tab(): close the current tab.
20. switch_to_tab(tab_number): switch to the tab.
21. wait_for_element(element, timeout): wait for the element to appear.
22. wait_for_element_to_disappear(element, timeout): wait for the element to disappear.
23. wait_for_element_to_be_clickable(element, timeout): wait for the element to be clickable.

### [2. firefox.py](browser-manager/firefox.py)  
Here you can find FirefoxBrowser class.  This class is used to create a browser object.
It Heritages from the Firefox class and implements some custom methods to make browser automation easier.

### Arguments:
driver_path: path to the driver
undetectable: if True, to hide bot info in the browser.
### Attributes:
1. driver_path: path to the driver
2. undetectable: if True, to hide bot info in the browser.
### Methods:
1. open(): This method opens firefox browser to start the navigation. Set Custom options before using this method.
2. ignore_images(): This method ignores images in the browser. 
3. ignore_popups(): This method ignores popups in the browser. 
4. ignore_notifications(): This method ignores notifications in the browser. 
5. ignore_errors(): This method ignores errors in the browser. 
6. headless(): This method ignores 
7. save_cookies(): This method saves cookies in the browser. 
8. load_cookies(): This method loads cookies in the browser. 
9. set_proxy(): This method sets proxy in the browser. 
10. set_user_agent(): This method sets user agent in the browser. 
11. set_profile(): This method sets profile in the browser. 
12. set_download_folder(): This method sets download folder in the browser. 
13. scrolldown(): This method scrolls down the browser. 
14. scrollup(): This method scrolls up the browser. 
15. scroll_to_element(): This method scrolls to the element in the browser. 
16. element_exists(): This method checks if the element exists in the browser. 
17. add_tab(): This method adds a new tab in the browser. 
18. get_tabs(): This method gets all the tabs in the browser. 
19. switch_tab(): This method switches to the tab in the browser. 
20. wait_for_element(): This method waits for the element in the browser. 
21. wait_for_element_to_disappear(): This method waits for the element to disappear in the browser. 
22. wait_for_element_to_be_clickable(): This method waits for the element to be clickable in the browser. 

### [3. web_elements.py]('browser-manager/web_elements.py) 
Custom WebElement class to add custom methods to WebElement class.
### Methods:
1. double_click() : Double click on the element. 
2. enter(): Enter text in the element. 
3. tab(): Tab on the element. 
4. escape(): Escape on the element. 
5. backspace(): Backspace on the element. 
6. write(text): Write text in the element. 
7. clear(): Clear the element. 
8. get_text(): Get text from the element. 
9. get_link(): Get link from the element. 
10. get_attribute(attribute): Get attribute from the element.
