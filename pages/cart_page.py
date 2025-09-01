from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.action_helper import ActionHelper

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.action = ActionHelper(driver)

        # Locators
        self.product_titles = (By.CSS_SELECTOR, ".product-title span")
        self.product_prices = (By.CSS_SELECTOR, ".cart-item-price span.font-semibold")
        self.quantity_labels = (By.XPATH, "//span[contains(text(),'Quantity')]")
        self.remove_buttons = (By.CSS_SELECTOR, "button.sd_mini_removeproduct")
        self.discount_input = (By.ID, "coupons_stacker_input")
        self.discount_apply_button = (By.ID, "coupons_stacker_add_button")
        self.stack_subtotal = (By.ID, "stack-discounts-subtotal-value")

    # Actions
    def open_cart(self):
        self.driver.get("https://rentoza.co.za/cart")

    def is_cart_loaded(self):
        return self.wait.until(EC.visibility_of_element_located(self.product_titles))

    def get_cart_count(self):
        return len(self.driver.find_elements(*self.product_titles))

    def get_product_titles(self):
        return [el.text.strip() for el in self.driver.find_elements(*self.product_titles)]

    def get_product_prices(self):
        return [el.text.strip() for el in self.driver.find_elements(*self.product_prices)]

    def get_quantity(self):
        quantity_text = self.driver.find_element(*self.quantity_labels).text
        return int(quantity_text.split(":")[1].strip())

    def remove_product(self, index=0):
        buttons = self.driver.find_elements(*self.remove_buttons)
        if index < len(buttons):
            self.action.click_element(buttons[index])

    def apply_discount(self, code):
        self.action.type_text(self.discount_input, code)
        self.action.click(self.discount_apply_button)

    def get_subtotal(self):
        return self.driver.find_element(*self.stack_subtotal).text.strip()

    def is_discount_applied(self):
        return "Discount" in self.driver.page_source or "SAVE10" in self.driver.page_source