# pages/base_page.py
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import IMPLICIT_TIMEOUT

class BasePage:
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, IMPLICIT_TIMEOUT)

    def navigate_to(self, url: str):
        """Safely navigates to a URL."""
        self.driver.get(url)

    def wait_for_element(self, locator: tuple):
        """Waits for an element to be present in the DOM."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator: tuple):
        """Waits for an element to be visible on screen."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple):
        """Waits for an element to be clickable before execution."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator: tuple, text: str):
        """Finds an input field, clears it, and types text safely."""
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)