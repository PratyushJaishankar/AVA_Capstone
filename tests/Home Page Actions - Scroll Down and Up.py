import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve the list of browsers to test from the project utility
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target site.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_home_page_scroll_down_and_up(driver, home_page):
    """
    Test Case: Home Page Actions - Scroll Down and Up

    Steps:
    1. Start browser via project driver fixture.
    2. Navigate to https://market99.com/.
    3. Call home_page.page_down().
    4. Wait 2s.
    5. Call home_page.page_up().
    6. Wait 2s.
    7. End session.

    Expected Result: Page scroll down then up occurs without errors.
    """
    # Scroll down the page
    home_page.page_down()
    time.sleep(2)

    # Scroll up the page
    home_page.page_up()
    time.sleep(2)

    # If no exceptions are raised, the test passes
    # Optionally, you can add assertions if page position can be verified
    # For now, we assert True to indicate the test completed successfully
    assert True, "Page scrolled down and up without errors"
