"""
Author_Name: Pratyush Jaishankar
Project_Name: ASC_Capstone

Functions created in this module:
- cart_dropdown(by_locator, option_locator)
- paste_text(by_locator)
- double_click(by_locator)
- get_color(by_locator, css_property)
- mouse_hover(by_locator)
- click(by_locator)
- enter_text(by_locator, text)
- find_element(by_locator)
- find_elements(by_locator)
- select_from_dropdown(by_locator, text)
- get_text(by_locator)
- is_visible(by_locator)
- scroll_to_element(by_locator)
- execute_script(script, *args)
- send_keys(keys, by_locator=None)
- wait_for_page_load(timeout=30)
"""

import time
import os

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Increase wait time for CI environments
        wait_timeout = 30 if os.environ.get('CI', 'false').lower() == 'true' else 10
        self.wait = WebDriverWait(driver, wait_timeout)

    def cart_dropdown(self, by_locator, option_locator):
        dropdown_toggle = self.wait.until(EC.element_to_be_clickable(by_locator))
        dropdown_toggle.click()
        time.sleep(0.5)  # Small delay for dropdown animation
        # 2️⃣ Select the quantity '6'
        option = self.wait.until(EC.element_to_be_clickable(option_locator))
        option.click()

    def paste_text(self, by_locator):
        elem = self.wait.until(EC.visibility_of_element_located(by_locator))
        elem.clear()
        # In CI environment, clipboard operations don't work reliably
        try:
            elem.send_keys(Keys.CONTROL, 'v')
        except:
            # Fallback: just clear the field
            pass
        time.sleep(2)
        try:
            elem.send_keys(Keys.ESCAPE)
        except:
            pass
        time.sleep(2)

    def double_click(self, by_locator):
        elem = self.wait.until(EC.visibility_of_element_located(by_locator))
        action = ActionChains(self.driver)
        action.double_click(elem).perform()

    def get_color(self, by_locator, css_property):
        elem = self.wait.until(EC.visibility_of_element_located(by_locator))
        return elem.value_of_css_property(css_property)

    def mouse_hover(self, by_locator):
        elem = self.wait.until(EC.visibility_of_element_located(by_locator))
        action = ActionChains(self.driver)
        action.move_to_element(elem).perform()

    def click(self, by_locator):
        element = self.wait.until(EC.element_to_be_clickable(by_locator))
        # Scroll element into view before clicking (helps in CI)
        if os.environ.get('CI', 'false').lower() == 'true':
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)
        element.click()

    def enter_text(self, by_locator, text):
        elem = self.wait.until(EC.visibility_of_element_located(by_locator))
        # Scroll into view in CI
        if os.environ.get('CI', 'false').lower() == 'true':
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            time.sleep(0.3)
        elem.clear()
        elem.send_keys(text)

    def find_element(self, by_locator):
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def find_elements(self, by_locator):
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))


    def select_from_dropdown(self, by_locator, text):
        elem = self.wait.until(EC.visibility_of_element_located(by_locator))
        select = Select(elem)
        select.select_by_visible_text(text)

    def get_text(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        # Scroll into view to ensure element is rendered in CI
        if os.environ.get('CI', 'false').lower() == 'true':
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
        return element.text

    def is_visible(self, by_locator):
        return self.wait.until(EC.visibility_of_element_located(by_locator))

    def scroll_to_element(self, by_locator):
        """Scroll to make an element visible in the viewport"""
        element = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        time.sleep(0.5)  # Brief pause after scrolling

    # Added helper to execute JavaScript on the page
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    # Added helper to send keys to the active element or to a specific locator
    def send_keys(self, keys, by_locator=None):
        if by_locator:
            elem = self.wait.until(EC.visibility_of_element_located(by_locator))
            elem.send_keys(keys)
        else:
            # send to the currently focused element
            self.driver.switch_to.active_element.send_keys(keys)

    # Add method to wait for page load
    def wait_for_page_load(self, timeout=30):
        """Wait for page to be fully loaded"""
        self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
