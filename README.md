# ez-visual-regression

*Used to take screenshots with selenium (pages or elements) and compare to baseline*

## What does ez-visual-regression do?

*Provide a brief exposition on what the purpose of your package is, or change this heading to goals (like [sdu](https://github.com/Descent098/sdu#goals))*

## Features & Roadmap

*Include a bullet point list of implemented features, and either a link to the github planning board or list of coming-soon features*

## Why should I use ez_img_diff?

There are a ton of great and more robust tools out there for this analysis, or for visual regression testing, but I found each of them had their own problems, here's a list:

|Package|Issue|
|-------|-----|
|[needle](https://github.com/python-needle/needle)| Requires a Nose test runner, and had out of date dependencies|
|[pytest-needle](https://github.com/jlane9/pytest-needle) | Works well, but cannot use [webdiver_manager](https://pypi.org/project/webdriver-manager/) with it | 
|[dpxdt](https://github.com/bslatkin/dpxdt) | Didn't test, but was 7 years old and mostly focused on CI/CD usage|
|[Visual Regression Tracker](https://github.com/Visual-Regression-Tracker/Visual-Regression-Tracker) | Works great, but for some of my use cases I need an API not a full application|
|[hermione](https://github.com/gemini-testing/hermione)|Could not use javascript/nodeJS for my use case|
|[specter](https://github.com/letsgetrandy/specter)|Could not use javascript/nodeJS for my use case|
|[Cypress-image-screenshot](https://github.com/jaredpalmer/cypress-image-snapshot)|Could not use javascript/nodeJS for my use case|

## Who is ez-visual-regression for?

*If your package has multiple uses in seperate domains it may be worth explaning use cases in different domains; see [ahd](https://github.com/Descent098/ahd#who-is-ahd-for) for example*

## Quick-start

*Include how people can get started using your project in the shortest time possible*

### Installation

#### From source

1. Clone this repo: (put github/source code link here)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory

#### From PyPi

1. Run ```pip install ez-visual-regression```

#### Examples

*Include an example or two of usage, or common use cases*

## Usage

*Include how to use your package as an API (if that's what you're going for)*

### Arguments

*If you are writing a script, include some helpful/often used arguments here. If you decide to use [docopt](http://docopt.org/) the usage string should do.* 

## Additional Documentation

*If you have any supplementary documentation elsewhere (i.e. https://readthedocs.org/) include references to it here.*
