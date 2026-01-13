import pytest
from page_objects.add_address import AddressPage
from page_objects.login_page import LoginPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers
import allure
import time

# Retrieve configured browsers for cross-browser testing
browsers = get_browsers()

@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("address_data", get_data("data/Complete_Test_Data/add_address.csv"))
@pytest.mark.parametrize("login_data", get_data("data/Complete_Test_Data/login_data.csv"))
@allure.feature("Add Address")
def test_add_address(driver, address_data, login_data):
    """
    Test to verify that a user can successfully add an address with valid data.
    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Open Login form and login using credentials from login_data
    3. Navigate to Add Address page
    4. Verify required address fields are not empty
    5. Fill address form and submit
    6. Wait for response
    7. Verify address appears in address list
    Expected Result:
    - Address is successfully added and isSuccessfullyAdded returns True
    - Page title contains 'Market99' after login
    """

    print(f"\nStarting test with login: {login_data['email']}")
    print(f"Address data: {address_data}")

    # Step 1: Navigate to site
    driver.get("https://market99.com/")

    # Step 2: Login
    login_page = LoginPage(driver)
    login_page.open_login()
    login_page.login(login_data["email"], login_data["password"])
    print("Login submitted.")

    # Step 3: Assert page title contains expected keyword after login
    assert "Market99" in driver.title, f"Unexpected page title after login: {driver.title}"

    # Step 4: Navigate to Add Address page
    add_address_page = AddressPage(driver)

    # Step 5: Assert address fields are not empty
    for key in ["first_name", "last_name", "address_line_1", "city", "postal_code", "phone_number"]:
        assert address_data[key], f"Address field '{key}' is empty!"

    print("All required address fields are present.")

    # Step 6: Fill address form and submit
    add_address_page.new_address(
        address_data["first_name"],
        address_data["last_name"],
        address_data.get("company_field", ""),  # Optional field
        address_data.get("province", ""),       # Optional field
        address_data["address_line_1"],
        address_data.get("address_line_2", ""), # Optional field
        address_data["city"],
        address_data["postal_code"],
        address_data["phone_number"]
    )
    print("Address submission attempted.")

    # Step 7: Wait briefly for the page to respond / redirect
    time.sleep(5)

    # Step 8: Verify address appears in address list
    result = add_address_page.isSuccessfullyAdded(address_data["first_name"])
    print(f"Address add result for {address_data['first_name']}: {result}")
    assert result is True, f"Address was not successfully added for {address_data['first_name']}!"

    print("Test completed successfully.")
