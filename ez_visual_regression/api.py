# Standard lib dependencies
import os                                                              # Path verification & modification
import time                                                            # Allows for pauses
import logging                                                         # Enables logging
from typing import Union, List

# Third Party Dependencies
## Image comparison
from ez_img_diff.api import compare_images

## Browser automation
from selenium.webdriver.common.by import By                            # Specify find_element type
from selenium.webdriver.remote.webdriver import WebDriver              # Used for type hintingc
from selenium.common.exceptions import NoSuchElementException          # Allows for error catching


def get_screenshot(driver:WebDriver, url:str, filename:str, locator:Union[str, None]=None, by:By=By.ID, ignored_elements: List[str]= None):
    """Takes a screenshot of a page or element

    Parameters
    ----------
    driver : WebDriver
        The browser to use for capturing screenshots

    url : str
        The URl you want to get a screenshot from (or filepath)

    filename : str, optional
        The file to export the screenshot to, by default None

    locator : Union[str, None], optional
        The locator to search with (i.e. element ID, class, xpath etc.), by default None

    by : By, optional
        Define how to use the locator to find an element, by default By.ID
        
    ignored_elements: List[str], option
        Use a query selector to specify elements to ignore

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
        
    Examples
    --------
    ### Create a screenshot with no comparisson (fancy alias for driver.save_screenshot() or element.screenshot())
    ```
    from ez_visual_regression import get_screenshot
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

    test_from_config(driver)
    
    get_screenshot(driver,"../tests/examples/v1/index.html", locator="myChart", filename="images/chart-v1.png" )
    get_screenshot(driver,"../tests/examples/v2/index.html", locator="myChart", filename="images/chart-v2.png" )
    ```
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
    if ignored_elements:
        for selector in ignored_elements:
            driver.execute_script(f'document.querySelectorAll("{selector}").forEach((el)=>{{el.style.opacity=0}})')
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

def assert_image_similarity_to_baseline(driver:WebDriver, url:str, folder:str, locator:Union[str, None]=None, by:By=By.ID, warning_threshold:float=10, error_threshold:float=30, ignored_elements: List[str]= None):
    """Asserts the current screenshot of a page is similar to `<folder>/baseline.png` within: 0 < diff < error_threshold

    Parameters
    ----------
    driver : WebDriver
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
    
    ignored_elements: List[str], option
        Use a query selector to specify elements to ignore

    Raises
    ------
    AssertionError
        If diff > error_threshold
        
    Returns
    -------
    float:
        The difference between the two images as a whole number percent (i.e. 1.313 is 1.313% or 15.928 is 15.928%)
    
    Examples
    --------
    ### Create baseline images for a webpage
    ```
    from selenium import webdriver                                         # Instantiates a browser
    from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
    from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
    from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser

    from ez_visual_regression.api import assert_image_similarity_to_baseline
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

    # Creates baseline if one isn't available
    assert_image_similarity_to_baseline(driver,"tests/examples/v1/index.html", locator="myChart", folder="tests/examples/v1" )
    ```
    
    ### Test against baseline image
    ```
    from selenium import webdriver                                         # Instantiates a browser
    from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
    from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
    from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser

    from ez_visual_regression.api import assert_image_similarity_to_baseline
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
    
    try:
        assert_image_similarity_to_baseline(driver,"tests/examples/v1/index.html", locator="myChart", folder="tests/examples/v1" )
    except AssertionError:
        print("Image too far from baseline!")
    ```
    
    ### Take screenshot of whole page while ignoring h2's and elements with id of myChart
    ```
    from selenium import webdriver                                         # Instantiates a browser
    from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
    from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
    from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser

    from ez_visual_regression.api import assert_image_similarity_to_baseline
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

    assert_image_similarity_to_baseline(driver,"tests/example_sites/test/index.html", folder="tests/example_sites/test", ignored_elements=["h2", "#myChart"])
    ```
    """
    if not os.path.isdir(folder):
        print(f"No directory was found called {folder}, creating...")
        os.mkdir(folder)
    if not os.path.exists(os.path.join(folder, "baseline.png")):
        print(f"No baseline image was found called {os.path.join(folder, 'baseline.png')}, creating...")
        get_screenshot(driver, url, os.path.join(folder, "baseline.png"), locator, by, ignored_elements)

    get_screenshot(driver, url, os.path.join(folder, "current.png"), locator, by, ignored_elements)

    diff = compare_images(os.path.join(folder, "baseline.png"), os.path.join(folder, "current.png"), os.path.join(folder, "diff.png"), os.path.join(folder, "thresh.png"))

    if diff > error_threshold:
        logging.error(f"Difference {diff} is over error threshold {error_threshold}")
        raise AssertionError(f"Difference {diff} is over error threshold {error_threshold}")
    if error_threshold > diff > warning_threshold:
        logging.warning(f"Difference {diff} is over warning threshold {error_threshold}")
        
    return diff
