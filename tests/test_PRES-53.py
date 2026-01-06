import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_zoom_out_js_no_js_errors(driver, home_page):
    """
    Test Case: PRES-53 - Home Page Actions - Zoom Out JS

    Steps:
    1. Start browser (handled by fixture).
    2. Navigate to https://market99.com/ (handled by fixture).
    3. Call home_page.zoom_out_js(step=0.8) to decrease page zoom using JS.
    4. Wait 2 seconds.
    5. End session (handled by fixture teardown).

    Expected Result:
    - Page zoomed out using JS.
    - No JavaScript errors present in browser logs.

    This test is parameterized to run on all browsers returned by get_browsers().
    """
    print("[Test] Starting test_zoom_out_js_no_js_errors...")

    # Zoom out the page using JavaScript
    print("Zooming out using JavaScript...")
    home_page.zoom_out_js(step=0.8)
    time.sleep(2)

    # Retrieve browser logs and check for JS errors
    # Note: Not all browsers support 'browser' log type (Chrome does, Edge may, Firefox may not)
    js_errors = []
    try:
        # Only attempt if driver supports log retrieval
        if hasattr(driver, "get_log"):
            for entry in driver.get_log("browser"):
                if entry.get("level") == "SEVERE" or "error" in entry.get("message", "").lower():
                    js_errors.append(entry)
        else:
            # For drivers that do not support get_log, skip log check
            print("Browser log retrieval not supported for this driver.")
    except Exception as e:
        print(f"Exception while retrieving browser logs: {e}")

    # Assert that there are no JS errors after zoom out
    assert not js_errors, f"JavaScript errors found in browser logs after zoom out: {js_errors}"

    print("[Test] Finished test_zoom_out_js_no_js_errors.")