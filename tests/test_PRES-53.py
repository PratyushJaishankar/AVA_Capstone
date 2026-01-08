import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve all browser configurations for cross-browser testing
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_zoom_out_home_page_js(driver, home_page):
    """
    Test Case: Zoom Out Home Page Using JS

    Steps:
    1. Start browser.
    2. Navigate to https://market99.com/.
    3. Call home_page.zoom_out_js().
    4. Wait 2s.
    5. End session.

    Expected Result:
    - Page zoomed out using JS.
    - No JS errors should occur.

    This test verifies that the zoom out functionality works as expected and does not produce JavaScript errors.
    """
    # Action: Zoom out using JavaScript
    try:
        home_page.zoom_out_js()
        time.sleep(2)
        # Assertion: Check for JS errors in browser logs
        logs = driver.get_log("browser")
        js_errors = [entry for entry in logs if entry["level"] == "SEVERE"]
        assert not js_errors, f"JavaScript errors found: {js_errors}"
    except Exception as e:
        pytest.fail(f"Test failed due to exception: {e}")
