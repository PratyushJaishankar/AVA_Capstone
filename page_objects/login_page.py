"""
Author_Name: Pratyush Jaishankar
Project_Name: ASC_Capstone

Functions created in this module:
- __init__(driver)
- mouse_hover_perform()
- open_login()
- login(email, password)
- logout()
- is_logged_in(timeout=3)
- is_login_page_loaded(timeout=3)
"""

import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    LOGIN_ICON = (By.CSS_SELECTOR, "a[href='/account']")
    EMAIL_INPUT = (By.ID, "CustomerEmail")
    PASSWORD_INPUT = (By.ID, "CustomerPassword")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space(text())='Sign In']")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")
    LOGIN_WITH_EMAIL_BUTTON = (By.ID, "loginWithEmailButton")
    LOGOUT_MYACCOUNT=(By.XPATH, "//*[@id='NavStandard']/div[5]/div[1]/a")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def mouse_hover_perform(self):
        before_color=self.get_color(self.SUBMIT_BUTTON,"background-color")
        self.mouse_hover(self.SUBMIT_BUTTON)
        time.sleep(1)
        after_color=self.get_color(self.SUBMIT_BUTTON,"background-color")
        if before_color != after_color:
            return True
        else:
            return False

    def open_login(self):
        self.click(self.LOGIN_ICON)
        self.click(self.LOGIN_WITH_EMAIL_BUTTON)

    def login(self, email, password):
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)

    def logout(self):
        self.click(self.LOGOUT_MYACCOUNT)
        self.click(self.LOGOUT_LINK)

    # Helper: return True when logout link is visible (user is logged in)
    def is_logged_in(self, timeout=3):
        homepage_url = "https://market99.com"
        try:
            # Wait until current_url becomes the homepage (strip trailing slashes)
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.current_url.rstrip('/') == homepage_url.rstrip('/')
            )
            return True
        except Exception:
            # Fallback: check for logout link presence (covers UIs that don't redirect)
            try:
                try:
                    self.click(self.LOGIN_ICON)
                except Exception:
                    # best-effort: ignore if we can't click the icon
                    pass
                self.find_elements(self.LOGOUT_LINK)
                return True
            except Exception:
                return False

    def is_login_page_loaded(self, timeout=3):
        """Check if the login page/form is still displayed (used for negative test validation)"""
        try:
            # Check if URL contains /account/login (indicating failed login kept user on login page)
            if '/account/login' in self.driver.current_url:
                return True
            # Also check if the email input field is still visible as a fallback
        except Exception:
            return False
