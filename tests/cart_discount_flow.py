from pages.product_search import ProductGridPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

def test_cart_flow_with_product_grid(driver):
    driver.get("https://rentoza.co.za")

    # Page objects
    grid = ProductGridPage(driver)
    product = ProductPage(driver)
    cart = CartPage(driver)

    # Step 1: Search for a product
    grid = ProductGridPage(driver)
    product_found = grid.search_product(
         name="iPhone 16 128GB"           # Example filter — adjust as needed
        # vendor="Apple",
        # min_price=500,
        # max_price=20000,
        # availability_text="In Stock"
    )
    assert product_found, "No matching product found in grid"

    # Step 2: Add product to cart
    assert product.is_product_displayed(), "Product page not loaded"
    product.add_product_to_cart()

    # Step 3: Open cart and validate
    cart.open_cart()
    assert cart.is_cart_loaded(), "Cart not loaded"
    assert cart.get_cart_count() > 0, "Cart is empty"

    titles = cart.get_product_titles()
    prices = cart.get_product_prices()
    quantity = cart.get_quantity()

    print("Cart Titles:", titles)
    print("Prices:", prices)
    print("Quantity:", quantity)

    # Step 4: Apply discount
    subtotal_before = cart.get_subtotal()
    cart.apply_discount("SAVE10")

    driver.implicitly_wait(3)
    subtotal_after = cart.get_subtotal()

    print("📉 Subtotal before:", subtotal_before)
    print("📈 Subtotal after:", subtotal_after)

    assert subtotal_after != subtotal_before, "Discount not applied"
    assert cart.is_discount_applied(), "Discount code not reflected"

    # Step 5: Remove product
    cart.remove_product(0)
    driver.implicitly_wait(2)
    assert cart.get_cart_count() == 0, "Product not removed from cart"