from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ProductGridPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.product_cards = (By.CSS_SELECTOR, "div[data-product-grid]")

    def search_product(self, name=None, vendor=None, min_price=None, max_price=None, availability_text=None):
        self.wait.until(EC.presence_of_all_elements_located(self.product_cards))
        products = self.driver.find_elements(*self.product_cards)

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, ".product-title-container a").text.strip()
                vendor_name = product.find_element(By.CSS_SELECTOR, ".yv-product-vendor-info").text.strip()
                price_text = product.find_element(By.CSS_SELECTOR, ".yv-product-price").text.strip()
                availability = product.text  # fallback: search entire card text

                price = float(''.join(filter(str.isdigit, price_text)))  # crude price extraction

                if name and name.lower() not in title.lower():
                    continue
                if vendor and vendor.lower() not in vendor_name.lower():
                    continue
                if min_price and price < min_price:
                    continue
                if max_price and price > max_price:
                    continue
                if availability_text and availability_text.lower() not in availability.lower():
                    continue

                print(f"✅ Match found: {title} | Vendor: {vendor_name} | Price: R{price}")
                product.find_element(By.CSS_SELECTOR, ".product-title-container a").click()
                return True

            except Exception as e:
                print(f"⚠️ Skipping product due to error: {e}")
                continue

        print("❌ No matching product found.")
        return False