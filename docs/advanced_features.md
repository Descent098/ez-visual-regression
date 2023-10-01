# Advanced Features

A description of the usage of the more nitty gritty capabilities of ez_visual_regression, and how to use them.

## Configuration files

You can add a configuration file that will allow you to setup tests without needing to write python code. Currently YAML format is supported. Here is an example of a few tests, and a screenshot:

```yaml
driver: Chrome # Can be chrome, firefox, or edge
tests:
    homepage: # minimum example (full page), and will put images in /homepage
        url: tests/example_sites/no_difference/index.html
    nav: # Full example (multiple elements)
        url: https://canadiancoding.ca
        locator: .nav-item p
        ignored_elements: [".hero"]
        folder: results/nav
        multielements: false
screenshots:
    chart:
        url: tests/example_sites/no_difference/index.html
        folder: results/chart # will be saved to results/chart/screenshot.png
        locator: "#myChart"
        ignored_elements: [".hero"]
```

To use this feature programmatically you can use:

```python
from ez_visual_regression.configuration import parse_config, execute_config

config = parse_config("config.yml") # This can be replaced with a manually constructed dictionary
execute_config(config)
```

## Picking a threshold

Picking thresholds can be more of an art than a science. Generally after a baseline image is generated your baseline will be compared to the `current` form of your page. In static pages/elements this should be `0`, if it is not 0, you will want to make sure the threshold is at least higher than whatever value is returned. This commonly happens for pages that have animations and/or dynamic content. I would recommend when setting up your tests intentionally break the system in a few ways and check the differences. Use those differences to determine the threshold you want!

You can then pass in a `warning_threshold` and `error_threshold` for `assert_image_similarity_to_baseline()`. The warning threshold will just show a warning, but **execution is not stopped**, if error_threshhold is crossed an `AssertionError` is raised and the execution is stopped, but the images are generated, so you can check them.

## Ignoring elements

You can ignore elements by sepcifying [Query/CSS selector](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors) in a list, and pass it in as a `ignored_elements` parameter:

```python
from selenium import webdriver                                         # Instantiates a browser
from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser

from ez_visual_regression.api import assert_image_similarity_to_baseline

# Configuration variables
URL = "https://canadiancoding.ca"
folder = "results"
locator = ".nav-item p"
ignored_elements = [".hero", ".card"]

# Setting up a webdriver (doesn't have to be chrome)
chrome_options = Options()
chrome_options.add_argument("--disable-gpu") # Common workaround for laptop GPU issues
chrome_options.add_argument("--no-sandbox")  # Common workaround for laptop GPU issues
driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

# Creates baseline if one isn't available
assert_image_similarity_to_baseline(driver, URL, folder=folder, locator=locator, multielements=True, ignored_elements=ignored_elements)
```

## Other multimedia

Because selenium just uses a browser you can use everything a browser can do. This means you can use it to inspect other multimedia types. In particular browsers have built in viewers for formats like PDF, so you can pass in the absolute path to a PDF and it will be loaded using the `file://` protocol, which will open the PDF and allow you to do visual regression testing on it. 

I am unaware of other built-in filetypes this works for, but I know you can download extensions on most browsers to handle other types of files (like markdown), so this may be useful for things like that!

### Additional PDF tricks

There are some additional tricks that make ez_visual_regression useful for PDF's:

- You can check specific pages of PDF's using `#page=<page_number>` at the end of the URL (i.e. `<file_path>/sample.pdf#page=2`)
- If you know which browser you're using you can inspect just the content by highlighting the element (i.e on edge you can use `#page_div_<page_number - 1>`, so for page 2 you can do `#page_div_1` for the page 2 content)

