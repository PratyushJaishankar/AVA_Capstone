import pytest
import csv
import time
from selenium import webdriver
from page_objects.login_page import LoginPage

# Utility to read credentials from CSV
def read_login_data(csv_path):
    data = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((row['username'], row['password']))
    return data

@pytest.fixture(scope="function")
def driver():
    # Setup: Start browser
    driver = webdriver.Chrome()  # Or use webdriver.Firefox() as needed
    driver.maximize_window()
    yield driver
    # Teardown: Quit browser
    driver.quit()

@pytest.mark.parametrize("username,password", read_login_data("data/Complete_Test_Data/login_data.csv"))
def test_verify_user_login_and_logout(driver, username, password):
    """
    Test user login and logout functionality using valid credentials.
    Steps:
    1. Navigate to https://market99.com/
    2. Open Login form.
    3. Perform required hover action and confirm it returns True.
    4. Submit login with credentials from CSV.
    5. Wait ~2s.
    6. Verify user is logged in.
    7. Call logout and ensure logout completes.
    """
    # Step 1: Navigate to site
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Step 2: Open Login form
    login_page.open_login()

    # Step 3: Perform hover action and verify
    assert login_page.mouse_hover_perform() is True, "Hover action on login submit button should change its color."

    # Step 4: Submit login with credentials
    login_page.login(username, password)

    # Step 5: Wait for login to process
    time.sleep(2)

    # Step 6: Verify user is logged in
    assert login_page.is_logged_in(), "User should be logged in after submitting valid credentials."

    # Step 7: Logout and verify
    login_page.logout()
    time.sleep(2)  # Wait for logout to complete

    # After logout, user should not be logged in
    assert not login_page.is_logged_in(), "User should be logged out after logout action."
