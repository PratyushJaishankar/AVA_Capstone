import pytest
import time
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Retrieve all configured browsers for cross-browser testing
browsers = get_browsers()

# Load positive test data from CSV (each row is a valid credential set)
positive_login_data = get_data("data/Complete_Test_Data/login_data.csv")

@pytest.mark.feature("Login & Logout")
@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("login_data", positive_login_data)
def test_login_logout_with_valid_credentials(driver, login_data):
    """
    Test user login and logout functionality using valid credentials.
    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Open Login form.
    3. Perform required hover action and confirm it returns True.
    4. Submit login with credentials from login_data.csv.
    5. Wait ~2s.
    6. Verify user is logged in via is_logged_in().
    7. Call logout().
    8. Wait and ensure logout completes.
    Expected Result:
    - User is logged in after valid credentials: is_logged_in() returns True.
    - After logout, session ends and logout completed successfully.
    """
    # Step 1: Navigate to site
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Step 2: Open Login form
    login_page.open_login()

    # Step 3: Perform hover action and assert result
    mouse_hover_result = login_page.mouse_hover_perform()
    assert mouse_hover_result is True, "Hover action on login button should change its color"

    # Step 4: Submit login with credentials
    login_page.login(login_data["email"], login_data["password"])

    # Step 5: Wait for login to process
    time.sleep(2)

    # Step 6: Verify user is logged in
    assert login_page.is_logged_in(), (
        f"Expected login to succeed for {login_data}, but user is not logged in (url={driver.current_url})"
    )

    # Step 7: Logout
    login_page.logout()

    # Step 8: Wait for logout to complete
    time.sleep(2)

    # Step 9: Verify user is logged out (logout link should not be present)
    assert not login_page.is_logged_in(), (
        f"Expected user to be logged out for {login_data}, but user is still logged in (url={driver.current_url})"
    )
