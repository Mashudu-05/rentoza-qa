import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage

def test_cart_and_checkout_flow(driver):
    driver.get("https://rentoza.co.za")

    # Instantiate page objects
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # wait for the page to be ready
    home_page = HomePage(driver)
    home_page.wait_until_ready()

    # Add product
    assert product_page.is_product_displayed()
    product_page.add_product_to_cart()


    print("Current URL:", driver.current_url)
    print("Page source snippet:", driver.page_source[:500])

    # Open cart and apply discount
    cart_page.open_cart()
    assert cart_page.is_cart_loaded()
    cart_page.apply_discount("SAVE10")
    subtotal = cart_page.get_subtotal()
    assert "R" in subtotal

    # Proceed to checkout
    checkout_page.proceed_to_checkout()
    assert checkout_page.is_checkout_ready()
    checkout_page.fill_checkout_form("Andani", "tester@example.com", "123 Tech Street")
    checkout_page.place_order()