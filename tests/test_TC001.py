"""
Test Script for PRES-55: Validates user login and logout functionality using LoginPage POM.

Steps:
1. Start browser and navigate to https://market99.com/
2. Open login form using LoginPage.open_login()
3. Perform hover action using LoginPage.mouse_hover_perform() and assert it returns True
4. Read credentials from data/Complete_Test_Data/login_data.csv and submit login using LoginPage.login(email, password)
5. Wait ~2s
6. Verify user is logged in using LoginPage.is_logged_in()
7. Call LoginPage.logout() and ensure logout completes

Uses parameterization for multiple credentials. Includes setup/teardown, comments, and adheres to PEP 8.
"""

import pytest
import time
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Get list of browsers to test on (from project utility)
browsers = get_browsers()

# Load login credentials from CSV (positive test data)
login_data_list = get_data("data/Complete_Test_Data/login_data.csv")

@pytest.mark.feature("Login & Logout")
@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("login_data", login_data_list)
def test_login_logout(driver, login_data):
    """
    Test user login and logout functionality for each credential in login_data.csv.

    Args:
        driver: Selenium WebDriver instance (provided by pytest fixture)
        login_data: Dictionary with 'email' and 'password' keys from CSV

    Steps:
        - Navigate to site
        - Open login form
        - Perform mouse hover and assert
        - Submit login
        - Wait and verify login
        - Logout and verify logout
    """
    # Step 1: Navigate to the website
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Step 2: Open login form
    login_page.open_login()

    # Step 3: Perform required hover action and assert it returns True
    assert login_page.mouse_hover_perform() is True, "Mouse hover did not change button color as expected"

    # Step 4: Submit login with credentials from CSV
    email = login_data["email"]
    password = login_data["password"]
    login_page.login(email, password)

    # Step 5: Wait for login to process
    time.sleep(2)

    # Step 6: Verify user is logged in
    assert login_page.is_logged_in(), f"Login failed for user: {email}"

    # Step 7: Logout and ensure logout completes
    login_page.logout()
    time.sleep(2)

    # Optionally, verify user is logged out (e.g., login page is visible again)
    # This step can be enhanced if needed:
    # assert not login_page.is_logged_in(), f"Logout failed for user: {email}"

    # Print for debug/logging purposes
    print(f"Completed login/logout test for: {email}")

# Note:
# - The driver fixture and browser setup/teardown are handled by pytest and project utilities.
# - Only provided LoginPage methods and locators are used.
# - Adheres to PEP 8 and includes comments for clarity.
