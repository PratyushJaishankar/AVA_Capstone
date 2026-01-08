import pytest
from page_objects.Signup import AddCustomerPage
from utils.browser_config import get_browsers
import allure
import time
from datetime import datetime

# Inline test data for customer signup
# For success cases, email is generated uniquely using timestamp
customer_rows = [
    {
        "first_name": "Prat",
        "last_name": "Jai",
        "email_prefix": "Prat.Jai",
        "password": "Pass@1234",
        "result": "success"
    },
    # Example negative case (duplicate email)
    {
        "first_name": "Prat",
        "last_name": "Jai",
        "email": "Prat.Jai.test@example.com",
        "password": "Pass@1234",
        "result": "failed"
    },
    {
        "first_name": "Prat",
        "last_name": "Jai",
        "email_prefix": "Prat.Jai.valid",
        "password": "Pass@1234",
        "result": "success"
    },
]

browsers = get_browsers()

def generate_unique_email(prefix):
    """Generate a unique email using timestamp to avoid duplicates."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}.{timestamp}@example.com"

@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("customer_data", customer_rows)
@allure.feature("Add Customer")
def test_add_customer(driver, customer_data):
    """
    Test customer signup functionality.
    - For 'success' cases, expects registration to succeed and redirect to homepage.
    - For 'failed' cases (e.g., duplicate email), expects registration to fail (form remains or not redirected).
    """
    # Step 1: Navigate to the site
    driver.get("https://market99.com/")
    add_customer_page = AddCustomerPage(driver)
    
    # Step 2: Open registration page
    add_customer_page.open_registration()
    
    # Step 3: Prepare email (unique for success, static for failure)
    result = (customer_data.get("result") or "success").strip().lower()
    if result == "failed" and "email" in customer_data:
        email = customer_data["email"]
    else:
        email = generate_unique_email(customer_data["email_prefix"])
    
    # Step 4: Fill registration form and submit
    add_customer_page.add_customer(
        customer_data["first_name"],
        customer_data["last_name"],
        email,
        customer_data["password"]
    )
    
    # Step 5: Wait for page response
    time.sleep(2)
    
    # Step 6: Assert expected outcome
    if result == "success":
        # Registration should succeed and redirect to homepage
        assert add_customer_page.is_registration_successful(), (
            f"Expected registration to succeed for {customer_data} with email {email}, "
            f"but current_url={driver.current_url}"
        )
    else:
        # Registration should fail (form still present or not redirected)
        assert add_customer_page.is_registration_page_loaded() or driver.current_url.strip("/") != "https://market99.com", (
            f"Expected registration to fail for {customer_data} with email {email}, "
            f"but it appears to have succeeded (url={driver.current_url})"
        )
