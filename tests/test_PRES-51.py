import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve browser configurations for parameterized testing
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_to_bottom(driver, home_page):
    """
    Test Case: Scroll to Bottom on Home Page (JIRA Task: PRES-51)
    Steps:
        1. Start browser.
        2. Navigate to https://market99.com/.
        3. Call home_page.scroll_to_bottom().
        4. Wait 2s.
        5. End session.
    Expected Result:
        Page scrolls to bottom successfully.
    """
    # Action: Scroll to the bottom of the page
    home_page.scroll_to_bottom()
    time.sleep(2)

    # Assertion: Verify that the page is scrolled to the bottom
    # This can be checked by comparing the scroll position with the page height
    scroll_position = driver.execute_script("return window.scrollY + window.innerHeight;")
    page_height = driver.execute_script("return document.body.scrollHeight;")
    assert abs(scroll_position - page_height) < 5, "Page should be scrolled to the bottom"

    # Teardown: The session will be ended automatically by pytest fixture
