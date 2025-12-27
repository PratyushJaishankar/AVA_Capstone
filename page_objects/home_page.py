"""
Author_Name: Pratyush Jaishankar
Project_Name: ASC_Capstone

Functions created in this module:
- page_up()
- page_down()
- scroll_by_pixel(pixels)
- scroll_to_top()
- scroll_to_bottom()
- zoom_in_js(step=0.8)
- zoom_out_js(step=0.8)
- mouse_scroll(pixels)
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    def page_up(self):
        """Scroll up using keyboard Page Up key."""
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)

    def page_down(self):
        """Scroll down using keyboard Page Down key."""
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    def scroll_by_pixel(self, pixels):
        """Scroll vertically by a number of pixels using JavaScript."""
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def scroll_to_top(self):
        """Scroll to the top of the page using JavaScript."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page using JavaScript."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def zoom_in_js(self, step=0.8):
        """Zoom in using JavaScript (increase page zoom by step)."""
        current_zoom = self.driver.execute_script("return document.body.style.zoom || '1'")
        try:
            new_zoom = float(current_zoom) + step
        except ValueError:
            new_zoom = 1 + step
        self.driver.execute_script(f"document.body.style.zoom='{new_zoom}'")
        print(f"Zoomed in: {new_zoom}")

    def zoom_out_js(self, step=0.8):
        """Zoom out using JavaScript (decrease page zoom by step)."""
        current_zoom = self.driver.execute_script("return document.body.style.zoom || '1'")
        try:
            new_zoom = max(float(current_zoom) - step, 0.1)
        except ValueError:
            new_zoom = 1 - step
        self.driver.execute_script(f"document.body.style.zoom='{new_zoom}'")
        print(f"Zoomed out: {new_zoom}")

    def mouse_scroll(self, pixels):
        """Scroll using mouse wheel simulation (ActionChains)."""
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(self.driver)
        actions.scroll_by_amount(0, pixels).perform()
