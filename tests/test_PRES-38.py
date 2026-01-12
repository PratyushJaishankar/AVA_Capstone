import pytest
from page_objects.delete_address import AddressPage
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers
import time

# Retrieve browser configurations for cross-browser testing
browsers = get_browsers()

@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("address_data", get_data("data/Complete_Test_Data/delete_address.csv"))
@pytest.mark.parametrize("login_data", get_data("data/Complete_Test_Data/login_data.csv"))
def test_delete_address_by_name(driver, address_data, login_data):
    """
    Test Case: Delete Address by Name
    JIRA Task ID: PRES-38

    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Open Login form and login using credentials from login_data.csv
    3. Navigate to Address Management page
    4. Delete the address matching first_name and last_name from delete_address.csv
    5. Wait for deletion to process
    6. Verify that the address is deleted and no longer appears in the address list

    Expected Result:
    - Address deletion is confirmed (is_address_deleted returns True)
    - The address does not appear in the address list
    """

    # Step 1: Navigate to the website
    driver.get("https://market99.com/")

    # Step 2: Login using provided credentials
    login_page = LoginPage(driver)
    login_page.open_login()
    login_page.login(login_data["email"], login_data["password"])
    assert "Market99" in driver.title, f"Unexpected page title after login: {driver.title}"

    # Step 3: Navigate to Address Management page
    address_page = AddressPage(driver)

    # Step 4: Delete the address by name
    first_name = address_data["first_name"]
    last_name = address_data["last_name"]
    address_page.delete_address_by_name(first_name, last_name)

    # Step 5: Wait for deletion to process
    time.sleep(3)

    # Step 6: Verify deletion
    is_deleted = address_page.is_address_deleted(first_name, last_name)
    assert is_deleted, f"Address for {first_name} {last_name} was not deleted!"

    # Additional logging for debugging
    print(f"Test completed: Address for {first_name} {last_name} deleted successfully.")

# Note:
# - This test uses parameterization to run for all combinations of browsers, login credentials, and address data.
# - The AddressPage class uses POM and encapsulates all locators and actions for address management.
# - The test script is modular, readable, and adheres to PEP 8 standards.
# - Ensure that data files (delete_address.csv, login_data.csv) are present and correctly formatted.
