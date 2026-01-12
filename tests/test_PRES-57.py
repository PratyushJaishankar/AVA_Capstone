import time
import pytest
from page_objects.search_page import SearchPage
import allure
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Retrieve browser configurations for cross-browser testing
browsers = get_browsers()

@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("search_data", get_data("data/Complete_Test_Data/search_data.xlsx"))
@allure.feature("Search Page")
def test_search_product_flow(driver, search_data):
    """
    Test the complete search product flow:
    1. Open the site and instantiate SearchPage.
    2. Perform search using product name from test data.
    3. Assert search results and product details page.
    4. Copy and paste coupon code as per flow.
    5. Add product to cart with quantity 6.
    6. Assert cart quantity matches requested amount.
    """

    # Step 1: Start browser and navigate to the site
    driver.get("https://market99.com/")
    search_page = SearchPage(driver)
    time.sleep(2)  # Wait for page to load

    # Step 2: Perform search
    product_name = search_data["product"]
    search_page.open_search()
    search_page.search_product(product_name)
    time.sleep(2)  # Wait for search results

    # Step 3: Assert search results page
    current_url = driver.current_url
    assert "search" in current_url, f"'search' not found in URL: {current_url}"
    assert product_name in current_url, f"'{product_name}' not found in URL: {current_url}"

    # Step 4: Open product details and assert
    search_page.get_result(product_name)
    time.sleep(2)  # Wait for product details page
    current_url = driver.current_url
    assert "products" in current_url, f"'products' not found in URL: {current_url}"
    assert product_name in current_url, f"'{product_name}' not found in URL: {current_url}"

    # Step 5: Copy and paste coupon code (as per test flow)
    search_page.copy_code()
    search_page.paste_code()

    # Step 6: Add product to cart with quantity 6
    quantity_query = 6
    time.sleep(2)
    search_page.add_product_to_cart(str(quantity_query))
    time.sleep(2)
    cart_quantity = search_page.verify_cart()
    time.sleep(2)

    # Step 7: Assert cart quantity matches requested amount
    assert str(quantity_query) in cart_quantity, f"Cart quantity '{cart_quantity}' does not match expected '{quantity_query}'"
