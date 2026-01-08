"""
Pytest-compatible test script for Authentication module.
Covers login/logout flow using Selenium-based LoginPage object.
Parameterizes login credentials from CSV, runs on all configured browsers.
Adheres to PEP 8 and includes comments for clarity.
"""

import pytest
import time
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Get list of browsers to test on (e.g., Chrome, Edge)
browsers = get_browsers()

# Load login credentials from CSV for parameterized tests
login_data_list = get_data("data/Complete_Test_Data/login_data.csv")

@pytest.mark.feature("Authentication")
@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("login_data", login_data_list)
def test_login_logout(driver, login_data):
    """
    Test user login and logout functionality.
    Steps:
    1. Navigate to market99.com
    2. Open login form
    3. Perform mouse hover action and assert it returns True
    4. Submit login with credentials from CSV
    5. Wait for login to process
    6. Verify user is logged in
    7. Logout and verify session ends

    Args:
        driver: Selenium WebDriver instance (parametrized for each browser)
        login_data: Dict containing 'email' and 'password' from CSV
    """
    # Step 1: Navigate to site
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Step 2: Open login form
    login_page.open_login()

    # Step 3: Perform required hover action
    mouse_hover_result = login_page.mouse_hover_perform()
    assert mouse_hover_result is True, "Mouse hover action failed on LoginPage"

    # Step 4: Submit login with credentials
    login_page.login(login_data["email"], login_data["password"])

    # Step 5: Wait for login to process (~2s)
    time.sleep(2)

    # Step 6: Verify user is logged in
    assert login_page.is_logged_in(), (
        f"Login failed for user {login_data['email']}. "
        f"Expected is_logged_in() to return True."
    )

    # Step 7: Logout and verify session ends
    login_page.logout()
    time.sleep(2)  # Wait for logout to complete

    # After logout, user should not be logged in
    assert not login_page.is_logged_in(), (
        f"Logout failed for user {login_data['email']}. "
        f"Expected is_logged_in() to return False after logout."
    )

    # Optionally, print for debug/logging
    print(f"Completed login/logout test for: {login_data['email']}")

# Optional: Add setup/teardown fixtures if browser/session management is needed
# (Assuming driver fixture is managed by conftest.py or similar)
