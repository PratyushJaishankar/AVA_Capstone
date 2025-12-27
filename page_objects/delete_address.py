"""
Author_Name: Pratyush Jaishankar
Project_Name: ASC_Capstone

Functions created in this module:
- __init__(driver)
- delete_address_by_name(first_name, last_name)
- is_address_deleted(first_name, last_name)
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class AddressPage(BasePage):
    MY_ACCOUNT_ICON = (By.XPATH, "//*[@id='NavStandard']/div[5]/div[1]/a")
    VIEW_ADDRESS = (By.CSS_SELECTOR, 'a[href="/account/addresses"]')
    ALL_ADDRESSES = (By.CSS_SELECTOR, "div.address")
    SPECIFIC_ADDRESS = (By.TAG_NAME, "p")
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def delete_address_by_name(self, first_name, last_name):
        # Get all address containers
        self.click(self.MY_ACCOUNT_ICON)
        self.click(self.VIEW_ADDRESS)
        address_blocks = self.find_elements(self.ALL_ADDRESSES)
        target_name = f"{first_name} {last_name}".strip().lower()
        for address in address_blocks:
            # Get the text inside <p> (which contains the name and address)
            p_tag = address.find_element(By.TAG_NAME, "p")
            p_text = p_tag.text.strip().lower()
            if target_name in p_text:
                # Found the matching address
                delete_button = address.find_element(By.CSS_SELECTOR, "a[data-button-delete]")
                self.execute_script("arguments[0].scrollIntoView(true);", delete_button)
                delete_button.click()
                alert = self.driver.switch_to.alert
                time.sleep(2)
                print("Alert text:", alert.text)

                # Accept (click OK) on the alert
                alert.accept()
                print("Alert accepted. Address deleted.")
                print(f"Clicked delete for {target_name}")
                break
        else:
            print(f"No address found for {target_name}")

    def is_address_deleted(self, first_name, last_name):
        addresses = self.find_elements(self.ALL_ADDRESSES)
        target_name = f"{first_name} {last_name}".strip().lower()
        for address in addresses:
            p_tag = address.find_element(self.SPECIFIC_ADDRESS[0], self.SPECIFIC_ADDRESS[1])
            if target_name in p_tag.text.strip().lower():
                return False
        return True
