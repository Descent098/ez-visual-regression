import os

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

## Regression testing
from ez_visual_regression.api import *
from ez_visual_regression.configuration import *

def setup_driver() -> WebDriver:
    if os.getenv("GITHUB_ACTIONS") == "true": # Give headless chrome head ;)
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
        from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 800))  
        display.start()

        chrome_options = webdriver.ChromeOptions()    
        # Add your options as needed    
        options = [
        # Define window size here
        "--window-size=1200,1200",
            "--ignore-certificate-errors"]
        for option in options:
            chrome_options.add_argument(option)
        return webdriver.Chrome(options = chrome_options, service=ChromeService(ChromeDriverManager().install()))
    else:
        return instantiate_driver("chrome")   


def test_element_diff():
    driver = setup_driver()

    examples_folder = os.path.join(os.path.dirname(__file__), "example_sites")
    try:
        # New setup (creates baseline)
        new_setup_folder = os.path.join(examples_folder, "new_setup")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(new_setup_folder, "index.html"), locator="#myChart", folder=new_setup_folder)
        assert os.path.exists(os.path.join(new_setup_folder, "baseline.png"))
        assert os.path.exists(os.path.join(new_setup_folder, "current.png"))
        assert os.path.exists(os.path.join(new_setup_folder, "diff.png"))
        assert os.path.exists(os.path.join(new_setup_folder, "thresh.png"))
        os.remove(os.path.join(new_setup_folder, "baseline.png"))
        os.remove(os.path.join(new_setup_folder, "current.png"))
        os.remove(os.path.join(new_setup_folder, "diff.png"))
        os.remove(os.path.join(new_setup_folder, "thresh.png"))
        
        assert .01> diff 
        
        # No difference
        no_difference_folder = os.path.join(examples_folder, "no_difference")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(no_difference_folder, "index.html"), locator="#myChart", folder=no_difference_folder)
        assert os.path.exists(os.path.join(no_difference_folder, "baseline.png"))
        assert os.path.exists(os.path.join(no_difference_folder, "current.png"))
        assert os.path.exists(os.path.join(no_difference_folder, "diff.png"))
        assert os.path.exists(os.path.join(no_difference_folder, "thresh.png"))
        os.remove(os.path.join(no_difference_folder, "current.png"))
        os.remove(os.path.join(no_difference_folder, "diff.png"))
        os.remove(os.path.join(no_difference_folder, "thresh.png"))
        assert .01> diff 
        
        # Small difference
        small_difference_folder = os.path.join(examples_folder, "small_difference")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(small_difference_folder, "index.html"), locator="#myChart", folder=small_difference_folder)
        assert os.path.exists(os.path.join(small_difference_folder, "baseline.png"))
        assert os.path.exists(os.path.join(small_difference_folder, "current.png"))
        assert os.path.exists(os.path.join(small_difference_folder, "diff.png"))
        assert os.path.exists(os.path.join(small_difference_folder, "thresh.png"))
        os.remove(os.path.join(small_difference_folder, "current.png"))
        os.remove(os.path.join(small_difference_folder, "diff.png"))
        os.remove(os.path.join(small_difference_folder, "thresh.png"))
        assert 30> diff >10
        
        # large difference
        large_difference_folder = os.path.join(examples_folder, "large_difference")
        with pytest.raises(AssertionError):
            assert_image_similarity_to_baseline(driver, os.path.join(large_difference_folder, "index.html"), locator="#myChart", folder=large_difference_folder)
        assert os.path.exists(os.path.join(large_difference_folder, "baseline.png"))
        assert os.path.exists(os.path.join(large_difference_folder, "current.png"))
        assert os.path.exists(os.path.join(large_difference_folder, "diff.png"))
        assert os.path.exists(os.path.join(large_difference_folder, "thresh.png"))
        
        os.remove(os.path.join(large_difference_folder, "current.png"))
        os.remove(os.path.join(large_difference_folder, "diff.png"))
        os.remove(os.path.join(large_difference_folder, "thresh.png"))
    finally:
        driver.close()

def test_full_page_diff():
    driver = setup_driver()

    examples_folder = os.path.join(os.path.dirname(__file__), "example_sites")
    
    try:
        # New setup (creates baseline)
        new_setup_folder = os.path.join(examples_folder, "full_page_new")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(new_setup_folder, "index.html"),folder=new_setup_folder)
        assert os.path.exists(os.path.join(new_setup_folder, "baseline.png"))
        assert os.path.exists(os.path.join(new_setup_folder, "current.png"))
        assert os.path.exists(os.path.join(new_setup_folder, "diff.png"))
        assert os.path.exists(os.path.join(new_setup_folder, "thresh.png"))
        os.remove(os.path.join(new_setup_folder, "baseline.png"))
        os.remove(os.path.join(new_setup_folder, "current.png"))
        os.remove(os.path.join(new_setup_folder, "diff.png"))
        os.remove(os.path.join(new_setup_folder, "thresh.png"))
        
        assert .01> diff 
        
        # No difference
        no_difference_folder = os.path.join(examples_folder, "full_page_new_no_diff")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(no_difference_folder, "index.html"), folder=no_difference_folder)
        assert os.path.exists(os.path.join(no_difference_folder, "baseline.png"))
        assert os.path.exists(os.path.join(no_difference_folder, "current.png"))
        assert os.path.exists(os.path.join(no_difference_folder, "diff.png"))
        assert os.path.exists(os.path.join(no_difference_folder, "thresh.png"))
        os.remove(os.path.join(no_difference_folder, "current.png"))
        os.remove(os.path.join(no_difference_folder, "diff.png"))
        os.remove(os.path.join(no_difference_folder, "thresh.png"))
        assert .01> diff 
        
        # Small difference
        small_difference_folder = os.path.join(examples_folder, "full_page_small_difference")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(small_difference_folder, "index.html"), folder=small_difference_folder)
        assert os.path.exists(os.path.join(small_difference_folder, "baseline.png"))
        assert os.path.exists(os.path.join(small_difference_folder, "current.png"))
        assert os.path.exists(os.path.join(small_difference_folder, "diff.png"))
        assert os.path.exists(os.path.join(small_difference_folder, "thresh.png"))
        os.remove(os.path.join(small_difference_folder, "current.png"))
        os.remove(os.path.join(small_difference_folder, "diff.png"))
        os.remove(os.path.join(small_difference_folder, "thresh.png"))
        assert 30> diff >10
        
        # large difference
        large_difference_folder = os.path.join(examples_folder, "full_page_large_difference")
        with pytest.raises(AssertionError):
            assert_image_similarity_to_baseline(driver, os.path.join(large_difference_folder, "index.html"), folder=large_difference_folder)
        assert os.path.exists(os.path.join(large_difference_folder, "baseline.png"))
        assert os.path.exists(os.path.join(large_difference_folder, "current.png"))
        assert os.path.exists(os.path.join(large_difference_folder, "diff.png"))
        assert os.path.exists(os.path.join(large_difference_folder, "thresh.png"))
        os.remove(os.path.join(large_difference_folder, "current.png"))
        os.remove(os.path.join(large_difference_folder, "diff.png"))
        os.remove(os.path.join(large_difference_folder, "thresh.png"))
    finally:
        driver.close()
    
def test_config():
    examples_folder = os.path.join(os.path.dirname(__file__), "example_sites")
    config = parse_config(os.path.join(examples_folder,"config.yml"))

    test = config["tests"][0]
    url,folder,locator,warning_threshold,error_threshold,ignored_elements,multielements = test

    assert url == "tests/example_sites/no_difference/index.html"
    assert folder == "nav"
    assert locator == "#myChart"
    assert warning_threshold == 10
    assert error_threshold == 30
    assert ignored_elements == [".hero"]
    assert multielements == False

    screenshots = config["screenshots"][0]
    url,filename,locator, ignored_elements = screenshots
    
    assert url == "tests/example_sites/no_difference/index.html"
    assert filename == os.path.join("chart","screenshot.png")
    assert locator == "#myChart"
    assert ignored_elements == [".hero"]
    try:
        execute_config(config)
    finally:
        os.remove(filename)
        os.rmdir("chart")
        os.remove(os.path.join("nav", "baseline.png"))
        os.remove(os.path.join("nav", "diff.png"))
        os.remove(os.path.join("nav", "thresh.png"))
        os.remove(os.path.join("nav", "current.png"))
        os.rmdir("nav")

    

    