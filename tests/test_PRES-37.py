import pytest
from page_objects.Signup import AddCustomerPage
from utils.browser_config import get_browsers
import time

@pytest.mark.parametrize("driver", get_browsers(), indirect=True)
def test_registration_fails_for_duplicate_email(driver):
    """
    Negative test: Verify that registration fails when using a duplicate/static email.
    Steps:
      1. Start browser and navigate to https://market99.com/
      2. Open registration page.
      3. Fill registration form with static duplicate email and valid data.
      4. Submit the form and wait for response.
      5. Assert that registration fails (form remains or no redirect to homepage).
    Expected Result:
      Registration should fail for duplicate email. The registration page/form should remain loaded,
      or the site should not redirect to homepage. No account should be created for the duplicate email.
    """
    # Test data for negative case (duplicate email)
    first_name = "Prat"
    last_name = "Jai"
    email = "Prat.Jai.test@example.com"  # Static duplicate email
    password = "Pass@1234"

    # Step 1: Navigate to site
    driver.get("https://market99.com/")
    add_customer_page = AddCustomerPage(driver)

    # Step 2: Open registration page
    add_customer_page.open_registration()

    # Step 3: Fill registration form
    add_customer_page.add_customer(first_name, last_name, email, password)

    # Step 4: Submit and wait for response
    time.sleep(2)  # Wait for page to respond

    # Step 5: Assert registration fails (form remains or no redirect)
    assert add_customer_page.is_registration_page_loaded() or driver.current_url.strip("/") != "https://market99.com", \
        f"Expected registration to fail for duplicate email {email}, but it appears to have succeeded (url={driver.current_url})"
