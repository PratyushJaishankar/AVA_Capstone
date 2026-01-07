import pytest
import time
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Retrieve all configured browsers for cross-browser testing
browsers = get_browsers()

# Load login test data from CSV file
login_data = get_data("data/Complete_Test_Data/login_data.csv")

@pytest.mark.feature("Authentication")
@pytest.mark.priority("High")
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("user", login_data)
def test_login_logout_valid_credentials(driver, user):
    """
    Test Case: Verify login and logout functionality with valid credentials.
    Steps:
    1. Start browser and navigate to https://market99.com/.
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

    # Step 3: Perform hover action and verify
    assert login_page.mouse_hover_perform() is True, "Mouse hover did not change button color as expected."

    # Step 4: Submit login with credentials
    login_page.login(user["email"], user["password"])

    # Step 5: Wait for login to process
    time.sleep(2)

    # Step 6: Verify user is logged in
    assert login_page.is_logged_in(), (
        f"Login failed for user {user['email']}. Expected is_logged_in() to return True."
    )

    # Step 7: Logout
    login_page.logout()

    # Step 8: Wait for logout to complete
    time.sleep(2)

    # Step 9: Verify user is logged out (should not be logged in anymore)
    assert not login_page.is_logged_in(), (
        f"Logout failed for user {user['email']}. Expected is_logged_in() to return False after logout."
    )

    # Optionally, verify login page is loaded after logout
    assert login_page.is_login_page_loaded(), (
        f"Login page not loaded after logout for user {user['email']}."
    )

# Note:
# - The test is parameterized to run for each browser and each row in login_data.csv.
# - The driver fixture is assumed to be provided by the test framework/environment.
# - All assertions include descriptive error messages for easier debugging.
# - Comments are provided for clarity and maintainability.
