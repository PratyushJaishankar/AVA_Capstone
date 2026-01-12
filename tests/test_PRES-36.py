"""
TestCase_Name: Customer Signup Flow
JIRA_TaskID: PRES-36

Automated test for customer signup on https://market99.com/
Validates registration success and homepage redirect.
"""

import pytest
import time
from datetime import datetime
from page_objects.Signup import AddCustomerPage

# Example user data for parameterization
customer_test_data = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "email_prefix": "alice.smith",
        "password": "Test@1234"
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email_prefix": "bob.johnson",
        "password": "Secure@5678"
    }
]

@pytest.fixture
def browser():
    """
    Pytest fixture to initialize and teardown the browser.
    Replace with your actual browser setup (e.g., Selenium WebDriver).
    """
    from selenium import webdriver
    driver = webdriver.Chrome()  # Or use your project-specific driver setup
    yield driver
    driver.quit()

def generate_unique_email(prefix):
    """
    Generates a unique email address using the current timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}.{timestamp}@example.com"

@pytest.mark.parametrize("user", customer_test_data)
def test_customer_signup_flow(browser, user):
    """
    Test the customer signup flow:
    1. Open browser and navigate to https://market99.com/
    2. Open registration form using AddCustomerPage.open_registration()
    3. Generate a unique email
    4. Fill in first name, last name, email, password, and submit
    5. Wait for ~2 seconds for page response
    6. Assert registration success and homepage redirect
    """
    # Step 1: Navigate to site
    browser.get("https://market99.com/")
    
    # Step 2: Initialize AddCustomerPage and open registration form
    add_customer_page = AddCustomerPage(browser)
    add_customer_page.open_registration()
    
    # Step 3: Generate unique email
    email = generate_unique_email(user["email_prefix"])
    
    # Step 4: Fill in registration details and submit
    add_customer_page.add_customer(
        user["first_name"],
        user["last_name"],
        email,
        user["password"]
    )
    
    # Step 5: Wait for page response
    time.sleep(2)
    
    # Step 6: Assert registration success and homepage redirect
    assert add_customer_page.is_registration_successful(), (
        f"Registration failed for user {user['first_name']} {user['last_name']} with email {email}"
    )
    assert browser.current_url.strip("/") == "https://market99.com", (
        f"User was not redirected to homepage after registration. Current URL: {browser.current_url}"
    )

# End of test script
