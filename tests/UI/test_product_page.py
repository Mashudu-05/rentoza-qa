from pages.home_page import HomePage
from pages.product_page import ProductPage

def test_product_page_flow(driver):
    driver.get("https://rentoza.co.za/collections/mobile-phones")

    # Wait for homepage to be ready
    home = HomePage(driver)
    home.wait_until_ready()

    # Use ProductPage to search and validate product
    page = ProductPage(driver)
    product_found = page.search_product(
        name="iPhone 16 128GB",
        # vendor="Apple",
        # min_price=500,
        # max_price=50000,
        # availability_text="In Stock"
    )
    assert product_found, "No matching product found in grid"

    # Validate product detail page
    assert page.is_product_displayed(), "Product page did not load correctly"
    details = page.get_product_details()

    assert details["title"], "Product title is missing"
    # assert details["price"].startswith("R"), "Price format is incorrect"
    # assert details["image"].startswith("https://"), "Image URL is invalid"
    # assert "In Stock" in details["availability"] or "Available" in details["availability"], "Availability text missing"

    # Variant selection
    updated_price = page.select_variant_and_get_price("1")
    assert updated_price.startswith("R"), "Updated price format is incorrect"

    # Add to cart
    page.add_product_to_cart()
    quantity = page.get_cart_quantity()
    assert quantity > 0, f"Expected quantity > 0, but got {quantity}"