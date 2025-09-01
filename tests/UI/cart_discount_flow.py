import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

@pytest.mark.usefixtures("setup")
class TestCartDiscountFlow:

    def test_full_cart_discount_flow(self, driver):
        # Step 1: Navigate to product listing
        driver.get("https://rentoza.co.za/collections/mobile-phones")

        # Step 2: Wait for homepage to be ready
        home = HomePage(driver)
        home.wait_until_ready()

        # Step 3: Search and validate product
        product_page = ProductPage(driver)
        product_found = product_page.search_product(name="iPhone 16 128GB")
        assert product_found, "No matching product found"

        assert product_page.is_product_displayed(), "Product page did not load"
        details = product_page.get_product_details()
        assert details["title"], "Product title missing"

        # Step 4: Select variant and add to cart
        updated_price = product_page.select_variant_and_get_price("1")
        assert updated_price.startswith("R"), "Price format incorrect"

        product_page.add_product_to_cart()
        quantity = product_page.get_cart_quantity()
        assert quantity > 0, f"Expected quantity > 0, but got {quantity}"

        # Step 5: Open cart and verify it's loaded
        cart = CartPage(driver)
        cart.open_cart()
        assert cart.is_cart_loaded(), "Cart page did not load"

        # Step 6: Get initial cart count
        initial_count = cart.get_cart_count()
        assert initial_count > 0, "Cart should have items"

        # Step 7: Remove one product and validate count
        cart.remove_product(index=0)
        updated_count = cart.get_cart_count()
        assert updated_count == initial_count - 1, "Item not removed correctly"

        # Step 8: Capture subtotal before discount
        subtotal_before = float(cart.get_subtotal().replace("R", "").replace(",", "").strip())

        # Step 9: Apply discount code
        discount_code = "SAVE10"
        cart.apply_discount(discount_code)
        assert cart.is_discount_applied(), "Discount code not applied"

        # Step 10: Validate subtotal remains unchanged
        subtotal_after = float(cart.get_subtotal().replace("R", "").replace(",", "").strip())
        assert subtotal_after == subtotal_before, "Subtotal should remain unchanged after discount"

        # Optional: Validate total if available
        # total = float(cart.get_total().replace("R", "").replace(",", "").strip())
        # assert total < subtotal_after, "Total should reflect discount"