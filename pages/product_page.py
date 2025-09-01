from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # Locators for product grid
        self.product_cards_locator = (By.CSS_SELECTOR, "div[data-product-grid]")
        self.product_title_link = (By.CSS_SELECTOR, ".product-title-container a")
        self.vendor_info = (By.CSS_SELECTOR, ".yv-product-vendor-info")
        self.price_info = (By.CSS_SELECTOR, ".yv-product-price")

        # Locators for product detail
        self.product_title = (By.CSS_SELECTOR, "h2.yv-product-detail-title")
        self.product_price = (By.CSS_SELECTOR, "span.yv-product-price")
        self.product_image = (By.CSS_SELECTOR, "a.yv-product-zoom.no-js-hidden")
        self.availability = (By.CSS_SELECTOR, ".availability")
        self.add_to_cart_btn = (By.CSS_SELECTOR, "button.Sd_addProduct.add_to_cart.button.med-btn.border-none.subscribe-now-btn.text-white.hover\\:text-white.rounded-full")
        self.cart_count = (By.CSS_SELECTOR, "span.pr-2.md\\:pr-10.lg\\:pr-10.text-sm")
        self.variant_radios = (By.CSS_SELECTOR, "input.sub-term-radio-button")

    def search_product(self, name=None, vendor=None, min_price=None, max_price=None, availability_text=None):
        self.wait.until(EC.presence_of_all_elements_located(self.product_cards_locator))
        product_cards = self.driver.find_elements(*self.product_cards_locator)

        for card in product_cards:
            try:
                title = card.find_element(*self.product_title_link).text.strip()
                vendor_name = card.find_element(*self.vendor_info).text.strip()
                price_text = card.find_element(*self.price_info).text.strip()
                availability = card.text

                price = float(''.join(filter(str.isdigit, price_text)))

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

                print(f"Match found: {title} | Vendor: {vendor_name} | Price: R{price}")
                card.find_element(*self.product_title_link).click()
                return True

            except Exception as e:
                print(f"Skipping product due to error: {e}")
                continue

        print("No matching product found.")
        return False

    def is_product_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.product_title))

    def get_product_details(self):
        title = self.driver.find_element(*self.product_title).text.strip()
        price = self.driver.find_element(*self.product_price).text.strip()
        image_src = self.driver.find_element(*self.product_image).get_attribute("src")
        availability = "Available"
        return {
            "title": title,
            "price": price,
            "image": image_src,
            "availability": availability
        }

    def add_product_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.add_to_cart_btn)).click()

    def get_cart_quantity(self):
        quantity_text = self.wait.until(EC.presence_of_element_located(self.cart_count)).text.strip()
        if "Quantity:" in quantity_text:
            try:
                return int(quantity_text.split(":")[1].strip())
            except ValueError:
                return 0
        return 0

    def select_variant_and_get_price(self, months):
        radios = self.driver.find_elements(*self.variant_radios)
        for radio in radios:
            if radio.get_attribute("value") == str(months):
                self.driver.execute_script("arguments[0].click();", radio)
                buyout_price = radio.get_attribute("data-buyout-price")
                return f"R {buyout_price}"
        raise Exception(f"Variant for {months} months not found")