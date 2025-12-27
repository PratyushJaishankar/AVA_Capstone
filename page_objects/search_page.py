"""
Author_Name: Pratyush Jaishankar
Project_Name: ASC_Capstone

Functions created in this module:
- open_search()
- search_product(query)
- get_result(query)
- add_product_to_cart(quantity)
- copy_code()
- paste_code()
- verify_cart()
"""

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from .base_page import BasePage
import time
import os

class SearchPage(BasePage):
    SEARCH_BUTTON =(By.XPATH, "//*[@id='NavStandard']/div[5]/search-popdown/details/summary")
    SEARCH_BOX=(By.ID,"searchInput-desktop")
    PRODUCT_LOCATOR = (By.CSS_SELECTOR, "div.product-title")
    COUPON = (By.ID, "cpnCode")
    COUPON_COPY_BUTTON = (By.ID, "cpnBtn")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "button[class='select-popout__toggle']")

    RESULT_EMAIL = (By.XPATH, "//div[contains(@class, 'customer-email')]")
    RESULT_NAME = (By.XPATH, "//div[contains(@class, 'customer-name')]")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[name='add']")
    VERIFY_CART_QUANTITY=(By.XPATH,"//*[@id='cart-drawer']/div[2]/h3/span")

    def open_search(self):
        # In CI, wait for page load before clicking
        if os.environ.get('CI', 'false').lower() == 'true':
            self.wait_for_page_load()
            time.sleep(1)
        self.click(self.SEARCH_BUTTON)
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(0.5)

    # Renamed from `search_product` to `search_customer` to match tests
    def search_product(self, query):
        self.enter_text(self.SEARCH_BOX, query)
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(0.5)
        # send RETURN to the specific search input element
        self.send_keys(Keys.RETURN, by_locator=self.SEARCH_BOX)
        # In CI, wait for search results to load
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(2)

    def get_result(self, query):
        # In CI, wait for products to load and scroll into view
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(1)
        products = self.find_elements(self.PRODUCT_LOCATOR)
        for element in products:
            if query in element.text.lower():
                # In CI, scroll element into view before clicking
                if os.environ.get('CI', 'false').lower() == 'true':
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.5)
                element.click()
                break

    def add_product_to_cart(self,quantity):
        # In CI, wait for product page to load
        if os.environ.get('CI', 'false').lower() == 'true':
            self.wait_for_page_load()
            time.sleep(1)
        quantity_locator = (By.XPATH, f"//a[@data-value='{quantity}']")
        self.cart_dropdown(self.QUANTITY_INPUT, quantity_locator)
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(0.5)
        self.click(self.ADD_TO_CART_BUTTON)
        # In CI, wait for cart to update
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(2)

    def copy_code(self):
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(1)
        self.double_click(self.COUPON)
        time.sleep(2)
        self.click(self.COUPON_COPY_BUTTON)
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(1)

    def paste_code(self):
        self.click(self.SEARCH_BUTTON)
        time.sleep(2)
        self.paste_text(self.SEARCH_BOX)

    def verify_cart(self):
        if os.environ.get('CI', 'false').lower() == 'true':
            time.sleep(1)
        quantity = self.get_text(self.VERIFY_CART_QUANTITY)
        return quantity
