import pytest
import time
from page_objects.login_page import LoginPage
import csv
from selenium import webdriver

def load_negative_login_data(csv_path):
    """
    Loads negative login credentials from a CSV file.
    Returns a list of dictionaries with 'email' and 'password' keys.
    """
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({'email': row['email'], 'password': row['password']})
    return data

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and quit the browser driver.
    """
    driver = webdriver.Chrome()  # Or use any configured browser
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Load negative test data from CSV
negative_login_data = load_negative_login_data("data/Failed_Test_Data/negative_login_data.csv")

@pytest.mark.parametrize("login_data", negative_login_data)
def test_negative_login(driver, login_data):
    """
    Test Case: Negative Login
    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Open Login form
    3. Perform mouse hover on submit button and assert effect
    4. Submit login with invalid credentials
    5. Wait ~2s
    6. Assert login failed and login form remains
    """
    # Step 1: Navigate to the site
    driver.get("https://market99.com/")
    login_page = LoginPage(driver)

    # Step 2: Open the login form
    login_page.open_login()

    # Step 3: Mouse hover on submit button and assert color change
    assert login_page.mouse_hover_perform() is True, "Mouse hover did not trigger expected effect on submit button."

    # Step 4: Attempt login with invalid credentials
    email = login_data["email"]
    password = login_data["password"]
    login_page.login(email, password)

    # Step 5: Wait for ~2 seconds to allow for UI response
    time.sleep(2)

    # Step 6: Assert that login fails and login form remains
    assert not login_page.is_logged_in(), (
        f"Expected login to fail for {email}, but user appears logged in (url={driver.current_url})"
    )
    assert login_page.is_login_page_loaded(), (
        f"Expected login page/form to remain after failed login for {email}"
    )
