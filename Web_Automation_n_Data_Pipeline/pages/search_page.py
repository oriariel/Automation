# pages/search_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchPage(BasePage):
    # Locators (Using standard CSS/XPath selectors)
    PRODUCT_CARDS = (By.CSS_SELECTOR, "li.product")
    PRODUCT_TITLES = (By.CSS_SELECTOR, "h2.woocommerce-loop-product__title")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "span.woocommerce-Price-amount")

    def extract_product_data(self):
        """Parses the visible grid items and extracts titles and prices."""
        # Ensure the product listings have loaded before trying to parse them
        self.wait_for_element(self.PRODUCT_CARDS)
        
        titles = self.driver.find_elements(*self.PRODUCT_TITLES)
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        
        extracted_data = []
        for title, price in zip(titles, prices):
            extracted_data.append({
                "item": title.text.strip(),
                "price": price.text.strip()
            })
            
        return extracted_data