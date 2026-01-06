import pytest
import time
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Load browser configurations and negative test data
browsers = get_browsers()
negative_login_data = get_data("data/Failed_Test_Data/negative_login_data.csv")

@pytest.mark.feature("Authentication")
@pytest.mark.negativecases
@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("login_data", negative_login_data)
def test_negative_login_authentication(driver, login_data):
    """
    Test Case: Negative Login - Authentication Failure with Invalid Credentials

    Steps:
    1. Start browser and navigate to https://market99.com/.
    2. Open Login form.
    3. Perform mouse hover on the submit button and assert it returns True.
    4. Submit login with invalid/negative credentials from CSV.
    5. Wait for ~2 seconds.
    6. Verify login failed: LoginPage.is_logged_in() returns False and LoginPage.is_login_page_loaded() returns True.

    Expected Result:
    - Login must fail: user is not logged in and the login form remains available; no redirect to authenticated area.
    """
    # Step 1: Navigate to the login page
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Step 2: Open the login form
    login_page.open_login()

    # Step 3: Perform mouse hover on the submit button
    mouse_hover_result = login_page.mouse_hover_perform()
    assert mouse_hover_result is True, "Mouse hover on submit button should change its color"

    # Step 4: Submit login with invalid credentials
    email = login_data["email"]
    password = login_data["password"]
    login_page.login(email, password)

    # Step 5: Wait for ~2 seconds to allow UI to update
    time.sleep(2)

    # Step 6: Verify login failed
    assert not login_page.is_logged_in(), (
        f"Expected login to fail for credentials: {login_data}, but user appears logged in (url={driver.current_url})"
    )
    assert login_page.is_login_page_loaded(), (
        f"Expected login page/form to remain after failed login for credentials: {login_data}"
    )
