"""
TestCase_Name: test_search_product_functionality
JIRA_TaskID: PRES-57

Functional/Regression test for Search module on https://market99.com/
Test Data: data/Complete_Test_Data/search_data.xlsx
Pre-Conditions:
    - Search product rows exist in `search_data.xlsx`
    - Site reachable
    - Browsers configured

Expected Result:
    - Search result and product page reflect the searched product
    - After adding quantity 6, the cart contains quantity '6'
    - URLs include 'search' then 'products' and the product name
    - Cart quantity matches the requested amount
"""

import time
import pytest
from page_objects.search_page import SearchPage
from data.Complete_Test_Data.data_loader import get_data
from utils.browser_config import get_browsers

# Retrieve browser configurations (e.g., Chrome, Firefox)
browsers = get_browsers()

@pytest.mark.parametrize("driver", browsers, indirect=True)
@pytest.mark.parametrize("search_data", get_data("data/Complete_Test_Data/search_data.xlsx"))
def test_search_product_functionality(driver, search_data):
    """
    Test the search functionality and cart quantity update for multiple products.
    Steps:
        1. Start browser.
        2. Navigate to https://market99.com/.
        3. Instantiate SearchPage.
        4. Open search.
        5. Enter product value from Excel and search.
        6. Assert 'search' in URL and product name included.
        7. Open product details.
        8. Assert 'products' in URL and product present.
        9. Copy and paste code (per flow).
        10. Set quantity (6) and add to cart.
        11. Get cart quantity and assert it matches.
    """
    # Step 2: Navigate to site
    driver.get("https://market99.com/")
    search_page = SearchPage(driver)
    time.sleep(2)  # Wait for page to load

    product_name = search_data["product"]

    # Step 4: Open search
    search_page.open_search()

    # Step 5: Search for product
    search_page.search_product(product_name)
    time.sleep(2)  # Wait for search results

    # Step 6: Assert 'search' in URL and product name included
    current_url = driver.current_url
    assert "search" in current_url, f"'search' not found in URL: {current_url}"
    assert product_name in current_url, f"'{product_name}' not found in URL: {current_url}"

    # Step 7: Open product details
    search_page.get_result(product_name)
    time.sleep(2)  # Wait for product page

    # Step 8: Assert 'products' in URL and product present
    current_url = driver.current_url
    assert "products" in current_url, f"'products' not found in URL: {current_url}"
    assert product_name in current_url, f"'{product_name}' not found in URL: {current_url}"

    # Step 9: Copy and paste code (if required by flow)
    search_page.copy_code()
    search_page.paste_code()

    # Step 10: Set quantity and add to cart
    quantity_query = 6
    time.sleep(2)
    search_page.add_product_to_cart(str(quantity_query))
    time.sleep(2)

    # Step 11: Get cart quantity and assert
    cart_quantity = search_page.verify_cart()
    time.sleep(2)
    assert str(quantity_query) in cart_quantity, f"Expected cart quantity '{quantity_query}', got '{cart_quantity}'"

# Note:
# - The test is parameterized for multiple browsers and products from the Excel file.
# - All SearchPage methods are used as per the test flow.
# - Sleeps are used for demo purposes; consider using WebDriverWait for production.
# - To run: pytest tests/test_search_product.py
