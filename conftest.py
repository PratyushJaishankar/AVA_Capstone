# conftest.py
import os
import pytest
import allure
from utils.driver_utils import get_driver


@pytest.fixture
def driver(request):
    """PyTest fixture that returns a WebDriver instance.

    Use `@pytest.mark.parametrize('driver', ['chrome'], indirect=True)` in tests to pass browser.
    The fixture supports remote execution via the SELENIUM_REMOTE_URL environment variable.
    """
    browser = request.param if hasattr(request, 'param') else os.environ.get('BROWSER', 'chrome')
    remote_url = os.environ.get('SELENIUM_REMOTE_URL')
    caps = None
    driver = get_driver(browser, remote_url, caps)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass


# Attach screenshots on failure to Allure report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        driver = item.funcargs.get('driver') if hasattr(item, 'funcargs') else None
        if not driver:
            # Try alternative access
            driver = item._request.funcargs.get('driver') if hasattr(item, '_request') else None
        if driver:
            try:
                png = driver.get_screenshot_as_png()
                allure.attach(png, name='screenshot', attachment_type=allure.attachment_type.PNG)
            except Exception:
                # don't raise in hook
                pass

