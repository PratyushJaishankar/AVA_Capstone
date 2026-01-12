# File: tests/test_add_customer.py

import pytest
from page_objects.Signup import AddCustomerPage
import time
from datetime import datetime

# Test data for parameterization
customer_rows = [
    {
        "first_name": "Test",
        "last_name": "User",
        "email_prefix": "test.user",
        "password": "Test@1234"
    },
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "email_prefix": "alice.smith",
        "password": "Alice@1234"
    },
    # Add more test data as needed
]

def generate_unique_email(prefix):
    """
    Generate a unique email address using the current timestamp.
    Ensures each test run uses a new email to avoid conflicts.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}.{timestamp}@example.com"

@pytest.mark.parametrize("customer_data", customer_rows)
def test_customer_signup_flow(driver, customer_data):
    """
    Test the customer signup flow:
    1. Start browser and navigate to https://market99.com/
    2. Open registration form using AddCustomerPage.open_registration()
    3. Generate a unique email address
    4. Fill in first name, last name, email, and password using AddCustomerPage.add_customer()
    5. Wait for page response
    6. Assert registration success using AddCustomerPage.is_registration_successful()
    7. Ensure user is redirected to homepage and not stuck on registration form
    """
    # Step 1: Navigate to homepage
    driver.get("https://market99.com/")
    add_customer_page = AddCustomerPage(driver)

    # Step 2: Open registration form
    add_customer_page.open_registration()

    # Step 3: Generate unique email
    email = generate_unique_email(customer_data["email_prefix"])

    # Step 4: Fill registration form and submit
    add_customer_page.add_customer(
        customer_data["first_name"],
        customer_data["last_name"],
        email,
        customer_data["password"]
    )

    # Step 5: Wait for page response (~2 seconds)
    time.sleep(2)

    # Step 6: Assert registration success
    assert add_customer_page.is_registration_successful(), (
        f"Registration failed for email {email}. "
        f"Current URL: {driver.current_url}"
    )

    # Step 7: Ensure user is redirected to homepage
    assert driver.current_url.strip("/") == "https://market99.com", (
        f"User not redirected to homepage after registration. "
        f"Current URL: {driver.current_url}"
    )

# Notes:
# - This script uses pytest parameterization for input data.
# - Comments are included for clarity.
# - The script is modular and follows PEP 8.
# - It strictly uses the provided POM methods.
# - Place this file in `tests/test_add_customer.py`.
# - The `driver` fixture should be provided by your test framework/conftest.py.
