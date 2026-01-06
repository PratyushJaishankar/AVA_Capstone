import pytest
import time
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Get list of browser drivers to test against
browsers = get_browsers()

# Load negative login test data from CSV
negative_login_data = get_data("data/Failed_Test_Data/negative_login_data.csv")

@pytest.mark.feature("Login & Logout")
@pytest.mark.negativecases
@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("login_data", negative_login_data)
def test_login_logout_negative(driver, login_data):
    """
    Negative login test for market99.com using invalid credentials.
    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Open login form using LoginPage.open_login()
    3. Perform mouse_hover_perform() and assert it returns True
    4. Submit login with invalid credentials from CSV
    5. Wait ~2s
    6. Assert that LoginPage.is_logged_in() returns False and LoginPage.is_login_page_loaded() returns True
    """
    print(f"Starting negative login test for: {login_data.get('email', 'unknown')}")
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Open the login form
    login_page.open_login()

    # Perform mouse hover and assert it succeeds
    mouse_hover_result = login_page.mouse_hover_perform()
    assert mouse_hover_result is True, "Mouse hover on login form failed"

    # Attempt login with invalid credentials
    print(f"Attempting negative login for: {login_data.get('email', 'unknown')}")
    login_page.login(login_data["email"], login_data["password"])
    time.sleep(2)  # Wait for login attempt to process

    # Assert login fails and login form remains visible
    assert not login_page.is_logged_in(), (
        f"Expected login to fail for {login_data}, but user appears logged in (url={driver.current_url})"
    )
    assert login_page.is_login_page_loaded(), (
        f"Expected login page/form to remain after failed login for {login_data}"
    )
    print(f"Completed negative login test for: {login_data.get('email', 'unknown')}")
