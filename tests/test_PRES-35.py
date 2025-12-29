import pytest
from page_objects.add_address import AddressPage
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers
import allure
import time

# Retrieve browser configurations for cross-browser testing
browsers = get_browsers()

@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("address_data", get_data("data/Complete_Test_Data/add_address.csv"))
@pytest.mark.parametrize("login_data", get_data("data/Complete_Test_Data/login_data.csv"))
@allure.feature("Add Address")
def test_add_address(driver, address_data, login_data):
    """
    Test to verify that a user can successfully add a new address after logging in.
    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Open Login form and login using credentials from login_data
    3. Navigate to Add Address page
    4. Verify required address fields are not empty
    5. Fill address form with address_data and submit
    6. Wait for response and verify address appears in address list
    Expected Result:
    - Address is successfully added and AddressPage.isSuccessfullyAdded(first_name) returns True
    - Page title contains 'Market99' after login
    """

    # Step 1: Navigate to site
    driver.get("https://market99.com/")
    
    # Step 2: Login
    login_page = LoginPage(driver)
    login_page.open_login()
    login_page.login(login_data["email"], login_data["password"])
    
    # Assertion: Verify page title after login
    assert "Market99" in driver.title, f"Unexpected page title after login: {driver.title}"
    
    # Step 3: Navigate to Add Address page
    add_address_page = AddressPage(driver)
    
    # Step 4: Verify required address fields are not empty
    for key in ["first_name", "last_name", "address_line_1", "city", "postal_code", "phone_number"]:
        assert address_data[key], f"Address field '{key}' is empty!"
    
    # Step 5: Fill address form and submit
    add_address_page.new_address(
        address_data["first_name"],
        address_data["last_name"],
        address_data.get("company_field", ""),
        address_data.get("province", ""),
        address_data["address_line_1"],
        address_data.get("address_line_2", ""),
        address_data["city"],
        address_data["postal_code"],
        address_data["phone_number"]
    )
    
    # Step 6: Wait for response and verify address appears in address list
    time.sleep(5)  # Wait up to 5 seconds for page response
    result = add_address_page.isSuccessfullyAdded(address_data["first_name"])
    assert result is True, f"Address was not successfully added for {address_data['first_name']}!"
