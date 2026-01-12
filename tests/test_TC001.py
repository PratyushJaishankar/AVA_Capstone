import pytest
from page_objects.Signup import AddCustomerPage
from utils.browser_config import get_browsers
import allure
import time
from datetime import datetime

# Inline test data for customer signup
# For successful registration, a unique email is generated using timestamp
# For failed registration (duplicate email), a static email is used
customer_rows = [
    {
        "first_name": "Prat",
        "last_name": "Jai",
        "email_prefix": "Prat.Jai",
        "password": "Pass@1234",
        "result": "success"
    },
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

    Steps:
    1. Start browser and navigate to https://market99.com/.
    2. Open registration page using AddCustomerPage.open_registration().
    3. Generate a unique email for success cases, use static email for failed cases.
    4. Fill first name, last name, email, password and submit.
    5. Wait for page response.
    6. Verify registration success or failure.

    Expected:
    - For success: Registration is successful, user is redirected to homepage.
    - For failure: Registration fails, user remains on registration form.
    """
    driver.get("https://market99.com/")
    add_customer_page = AddCustomerPage(driver)
    add_customer_page.open_registration()

    # Determine email based on test case type
    result = (customer_data.get("result") or "success").strip().lower()
    if result == "failed" and "email" in customer_data:
        # Use static email for intentional failure
        email = customer_data["email"]
    else:
        # Generate unique email for success cases
        email = generate_unique_email(customer_data["email_prefix"])

    add_customer_page.add_customer(
        customer_data["first_name"],
        customer_data["last_name"],
        email,
        customer_data["password"]
    )

    # Wait briefly for the page to respond / redirect
    time.sleep(2)

    if result == "success":
        # Positive test: expect redirect to homepage (registration successful)
        assert add_customer_page.is_registration_successful(), (
            f"Expected registration to succeed for {customer_data} with email {email}, "
            f"but current_url={driver.current_url}"
        )
    else:
        # Negative test: expect registration to fail (form still present or not redirected)
        assert add_customer_page.is_registration_page_loaded() or driver.current_url.strip("/") != "https://market99.com", (
            f"Expected registration to fail for {customer_data} with email {email}, "
            f"but it appears to have succeeded (url={driver.current_url})"
        )
