import csv
import time
from typing import List, Dict

from selenium.webdriver.common.by import By

# Minimal keyword-driven runner. Steps CSV should contain columns:
# action, locator_type, locator, value
# Supported actions: open_url, click, enter_text, assert_text, sleep

LOCATOR_MAP = {
    'id': By.ID,
    'css': By.CSS_SELECTOR,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'name': By.NAME,
}


def load_keywords(path: str) -> List[Dict[str, str]]:
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def run_keywords(driver, steps: List[Dict[str, str]]):
    for step in steps:
        action = (step.get('action') or '').strip()
        locator_type = (step.get('locator_type') or '').strip()
        locator = (step.get('locator') or '').strip()
        value = step.get('value') or ''

        if action == 'open_url':
            driver.get(value)
        elif action == 'sleep':
            time.sleep(float(value) if value else 1)
        elif action in ('click', 'enter_text', 'assert_text'):
            if not locator_type or not locator:
                raise ValueError(f"Missing locator for action {action}: {step}")
            by = LOCATOR_MAP.get(locator_type.lower())
            if not by:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            if action == 'click':
                driver.find_element(by, locator).click()
            elif action == 'enter_text':
                elem = driver.find_element(by, locator)
                elem.clear()
                elem.send_keys(value)
            elif action == 'assert_text':
                elem = driver.find_element(by, locator)
                assert value in elem.text, f"Expected '{value}' in element text '{elem.text}'"
        else:
            raise ValueError(f"Unsupported action: {action}")

