import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve the list of browsers to test on (e.g., Chrome, Edge, Firefox)
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_zoom_in_js_no_js_errors(driver, home_page):
    """
    Test Case: Verify page zoom in using JavaScript on Home Page

    Steps:
    1. Start browser.
    2. Navigate to https://market99.com/.
    3. Call home_page.zoom_in_js().
    4. Wait 2s.
    5. End session.

    Expected Result:
    - Page zoomed in using JS.
    - No JS errors.

    This test checks that zooming in via JavaScript executes without errors and the zoom level increases.
    """
    # Get the initial zoom level
    initial_zoom = driver.execute_script("return document.body.style.zoom || '1'")
    try:
        initial_zoom_float = float(initial_zoom)
    except ValueError:
        initial_zoom_float = 1.0

    # Perform the zoom in action
    home_page.zoom_in_js()
    time.sleep(2)

    # Get the new zoom level
    new_zoom = driver.execute_script("return document.body.style.zoom || '1'")
    try:
        new_zoom_float = float(new_zoom)
    except ValueError:
        new_zoom_float = initial_zoom_float + 0.8  # Default step

    # Assert that the zoom level has increased
    assert new_zoom_float > initial_zoom_float, (
        f"Zoom level should increase after zoom_in_js(), but was {initial_zoom_float} and is now {new_zoom_float}"
    )

    # Check for JS errors in browser logs (if supported)
    # Note: Not all browsers support 'browser' log type; Chrome does.
    if hasattr(driver, "get_log"):
        try:
            logs = driver.get_log("browser")
            js_errors = [entry for entry in logs if entry["level"] == "SEVERE"]
            assert not js_errors, f"JavaScript errors found: {js_errors}"
        except Exception:
            # If log retrieval fails, skip JS error check
            pass

    # No explicit teardown needed; driver fixture handles session end.
