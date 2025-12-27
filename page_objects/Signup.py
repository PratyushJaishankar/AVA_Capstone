"""
Author_Name: Pratyush Jaishankar
Project_Name: ASC_Capstone

Functions created in this module:
- open_registration()
- add_customer(first_name, last_name, email, password)
- is_registration_successful(homepage_url="https://market99.com")
- is_registration_page_loaded(timeout=2)
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class AddCustomerPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "FirstName")
    LAST_NAME_INPUT = (By.ID, "LastName")
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "CreatePassword")
    # match by exact text and type
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space(text())='Create']")

    def open_registration(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/account']"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "loginWithEmailButton"))).click()
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sign up"))).click()
        time.sleep(3)  # Wait for the registration page to load

    def add_customer(self, first_name, last_name, email, password):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)

    # Helper: return True when current URL looks like the site homepage (registration succeeded)
    def is_registration_successful(self, homepage_url="https://market99.com"):
        try:
            return self.driver.current_url.strip("/") == homepage_url
        except Exception:
            return False

    # Helper: return True if the registration form is still present on the page (used for negative tests)
    def is_registration_page_loaded(self, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.FIRST_NAME_INPUT))
            return True
        except Exception:
            return False
