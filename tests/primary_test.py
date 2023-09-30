import os

import pytest

## Browser automation
from selenium import webdriver                                         # Instantiates a browser
from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser

## Regression testing
from ez_visual_regression.api import assert_image_similarity_to_baseline


def test_element_diff():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

    examples_folder = os.path.join(os.path.dirname(__file__), "example_sites")
    try:
        # New setup (creates baseline)
        new_setup_folder = os.path.join(examples_folder, "new_setup")
        diff = assert_image_similarity_to_baseline(driver, os.path.join(new_setup_folder, "index.html"), locator="myChart", folder=new_setup_folder)
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
        diff = assert_image_similarity_to_baseline(driver, os.path.join(no_difference_folder, "index.html"), locator="myChart", folder=no_difference_folder)
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
        diff = assert_image_similarity_to_baseline(driver, os.path.join(small_difference_folder, "index.html"), locator="myChart", folder=small_difference_folder)
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
            assert_image_similarity_to_baseline(driver, os.path.join(large_difference_folder, "index.html"), locator="myChart", folder=large_difference_folder)
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
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

    examples_folder = os.path.join(os.path.dirname(__file__), "example_sites")
    
    try:
        ...
    finally:
        driver.close()
    
