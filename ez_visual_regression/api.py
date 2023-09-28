# Standard lib dependencies
import os                                                              # Path verification & modification
import time                                                            # Allows for pauses
import logging                                                         # Enables logging
from typing import Union

# Third Party Dependencies
## Image comparison
from ez_img_diff.api import compare_images

## Browser automation
from selenium import webdriver                                         # Instantiates a browser
from selenium.webdriver.common.by import By                            # Specify find_element type
from selenium.common.exceptions import NoSuchElementException          # Allows for error catching

def get_screenshot(driver:webdriver, url:str, filename:str, locator:Union[str, None]=None, by:By=By.ID):
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

def assert_image_similarity_to_baseline(driver:webdriver, url:str, folder:str, locator:Union[str, None]=None, by:By=By.ID, warning_threshold:float=10, error_threshold:float=30):
    """Asserts the current screenshot of a page is similar to `<folder>/baseline.png` within: 0 < diff < error_threshold

    Parameters
    ----------
    driver : webdriver
        The browser to use for capturing screenshots

    url : str
        The URl you want to get a screenshot from (or filepath)

    folder : str
        The folder to save the baseline, threshold, current and difference images to

    locator : Union[str, None], optional
        The locator to search with (i.e. element ID, class, xpath etc.), by default None

    by : By, optional
        Define how to use the locator to find an element, by default By.ID

    warning_threshold : float, optional
        The threshold at which there will be a logged warning, by default 10

    error_threshold : float, optional
        The threshold at which an explicit error will be thrown, by default 30

    Raises
    ------
    AssertionError
        If diff > error_threshold
    """
    if not os.path.isdir(folder):
        print(f"No directory was found called {folder}, creating...")
        os.mkdir(folder)
    if not os.path.exists(os.path.join(folder, "baseline.png")):
        print(f"No baseline image was found called {os.path.join(folder, 'baseline.png')}, creating...")
        get_screenshot(driver, url, os.path.join(folder, "baseline.png"), locator, by)

    get_screenshot(driver, url, os.path.join(folder, "current.png"), locator, by)

    diff = compare_images(os.path.join(folder, "baseline.png"), os.path.join(folder, "current.png"), os.path.join(folder, "diff.png"), os.path.join(folder, "thresh.png"))

    if diff > error_threshold:
        logging.error(f"Difference {diff} is over error threshold {error_threshold}")
        raise AssertionError(f"Difference {diff} is over error threshold {error_threshold}")
    if error_threshold > diff > warning_threshold:
        logging.warning(f"Difference {diff} is over warning threshold {error_threshold}")
