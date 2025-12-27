import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def _local_driver(browser_name):
    # Check if running in CI environment (GitHub Actions sets CI=true)
    # On local Windows, this will be False, so browser runs normally
    is_ci = os.environ.get('CI', 'false').lower() == 'true'

    if browser_name == "chrome":
        options = ChromeOptions()
        # Only apply headless and CI-specific options when running in CI
        if is_ci:
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-setuid-sandbox')
        return webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if is_ci:
            options.add_argument('--headless')
        return webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()

        # Critical flags for Jenkins/Windows service context
        # These prevent Edge from crashing when run as a service
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        options.add_argument('--no-first-run')
        options.add_argument('--safebrowsing-disable-auto-update')
        options.add_argument('--disable-blink-features=AutomationControlled')

        # Fix for DevToolsActivePort error in Windows service context
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-features=msSmartScreenProtection')

        # Create a temp user data directory to avoid profile access issues
        import tempfile
        temp_dir = tempfile.mkdtemp(prefix='edge_profile_')
        options.add_argument(f'--user-data-dir={temp_dir}')
        options.add_argument('--profile-directory=Default')

        if is_ci:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
        else:
            # For local runs, maximize window for better visibility
            options.add_argument('--start-maximized')

        # Check if EDGE_DRIVER_PATH is set in the environment
        edge_driver_path = os.environ.get("EDGE_DRIVER_PATH")
        if edge_driver_path:
            # Use the specified driver path
            service = EdgeService(executable_path=edge_driver_path)
            return webdriver.Edge(service=service, options=options)
        else:
            # Let Selenium Manager handle the driver
            return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported local browser: {browser_name}")


def _remote_driver(browser_name, remote_url, capabilities_overrides=None):
    caps = None
    if browser_name == "chrome":
        caps = DesiredCapabilities.CHROME.copy()
    elif browser_name == "firefox":
        caps = DesiredCapabilities.FIREFOX.copy()
    elif browser_name == "edge":
        caps = DesiredCapabilities.EDGE.copy()
    else:
        raise ValueError(f"Unsupported remote browser: {browser_name}")

    if capabilities_overrides:
        caps.update(capabilities_overrides)

    # Use positional args for Remote to avoid static analysis warning about keyword names
    return webdriver.Remote(remote_url, caps)


def get_driver(browser: str = "chrome", remote_url: str | None = None, capabilities_overrides: dict | None = None):
    """
    Return a WebDriver instance.

    - If `remote_url` is provided (or environment variable SELENIUM_REMOTE_URL is set), a Remote WebDriver is created.
    - Otherwise a local WebDriver is created.

    Args:
        browser: "chrome" | "firefox" | "edge"
        remote_url: selenium hub/grid URL (optional)
        capabilities_overrides: extra desired capabilities for remote hubs
    """
    # allow environment override
    env_remote = os.environ.get("SELENIUM_REMOTE_URL")
    if remote_url is None and env_remote:
        remote_url = env_remote

    if remote_url:
        return _remote_driver(browser, remote_url, capabilities_overrides)
    else:
        return _local_driver(browser)
