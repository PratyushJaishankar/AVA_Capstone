import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve available browsers from the project utility
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_to_top(driver, home_page):
    """
    Test Case: Verify scroll to top on Home Page

    Steps:
    1. Start browser.
    2. Navigate to https://market99.com/.
    3. Call home_page.scroll_to_top().
    4. Wait 2s.
    5. End session.

    Expected Result:
    - Page scrolls to top; no exceptions.

    This test ensures that the scroll_to_top method executes without raising any exceptions.
    """
    # Action: Scroll to top of the page
    try:
        home_page.scroll_to_top()
        time.sleep(2)
    except Exception as e:
        pytest.fail(f"Exception occurred while scrolling to top: {e}")

    # Assertion: No exception should be raised, and the page should be at the top
    # Optionally, verify scroll position is at the top (y == 0)
    scroll_y = driver.execute_script("return window.scrollY;")
    assert scroll_y == 0, "Page should be scrolled to the top (window.scrollY == 0)"