# Standard lib dependencies
import os                                                              # Path verification & modification
import time                                                            # Allows for pauses
import logging                                                         # Enables logging
from typing import Union

## Browser automation
from selenium import webdriver                                         # Instantiates a browser
from selenium.webdriver.common.by import By                            # Specify find_element type
from selenium.common.exceptions import NoSuchElementException          # Allows for error catching

def get_screenshot(driver:webdriver.Chrome, url:str, filename:str, locator:Union[str, None]=None, by:By=By.ID):
    """Takes a screenshot of a page or element

    Parameters
    ----------
    driver : webdriver
        The browser to use for capturing screenshots
    url : str
        The URl you want to get a screenshot from (or filepath)
    filename : str, optional
        The file to export the screenshot to, by default None
    locator : Union[str, None], optional
        The locator to search with (i.e. element ID, class, xpath etc.), by default None
    by : By, optional
        Define how to use the locator to find an element, by default By.ID

    Notes
    -----
    - If locator is not specified a full page screenshot is used
    
    
    References
    ----------
    - How to use by if you've never seen it https://selenium-python.readthedocs.io/locating-elements.html
    
    Raises
    ------
    FileNotFoundError
        If the URL is a file path and it does not exist
    """
    if not url.startswith("http"):
        if url.endswith(".html") and not url.startswith("file://"): # Assume file path
            logging.debug("URL provided does not have protocol, defaulting to file")
            abs_fp = os.path.abspath(url).replace("\\","/")
            if not os.path.exists(abs_fp):
                raise FileNotFoundError(f"File path {abs_fp} does not exist")
            url = f'file://{abs_fp}'
        else:
            url = "http://" + url

    driver.get(url)
    
    # Wait for page to load and run all animations
    time.sleep(3) # TODO: Be better
    
    if locator: # Screenshot element
        if by == By.ID:
            try:
                driver.find_element(by, locator).screenshot(filename)
            except NoSuchElementException:
                logging.error(f"\033[0;31m Element does not exist when looking for an {by} with {locator} confirm spelling and capitalization\033[1;37m")
                exit(1)
        else:
            try:
                driver.find_elements(by, locator)[0].screenshot(filename)
            except NoSuchElementException:
                logging.error(f"\033[0;m Element does not exist when looking for a {by} with {locator} confirm spelling and capitalization\033[1;37m")
                exit(1)
    else: # Screenshot page
        driver.save_screenshot(filename)
