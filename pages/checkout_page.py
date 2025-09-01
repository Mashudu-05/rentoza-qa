from selenium.webdriver.common.by import By
from utils.action_helper import ActionHelper

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.action = ActionHelper(driver)

    # Locators
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".checkout-btn")
    NAME_FIELD = (By.ID, "name")
    EMAIL_FIELD = (By.ID, "email")
    ADDRESS_FIELD = (By.ID, "address")
    PLACE_ORDER = (By.ID, "place-order")

    # Actions
    def proceed_to_checkout(self):
        self.action.click(self.CHECKOUT_BUTTON)

    def fill_checkout_form(self, name, email, address):
        self.action.type_text(self.NAME_FIELD, name)
        self.action.type_text(self.EMAIL_FIELD, email)
        self.action.type_text(self.ADDRESS_FIELD, address)

    def place_order(self):
        self.action.click(self.PLACE_ORDER)

    def is_checkout_ready(self):
        return self.action.is_displayed(self.NAME_FIELD)