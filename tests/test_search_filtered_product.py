from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.product_search import ProductGridPage

def test_product_page_flow(driver):
    driver.get("https://rentoza.co.za/collections/mobile-phones")

    # Wait for homepage to be ready
    home = HomePage(driver)
    home.wait_until_ready()

    # Search and click on a product from the grid
    grid = ProductGridPage(driver)
    product_found = grid.search_product(
        name="iPhone 16 128GB",
        # vendor="Apple",
        # min_price=500,
        # max_price=50000,
        # availability_text="In Stock"
    )
    assert product_found, "No matching product found in grid"

    # Validate product page
    page = ProductPage(driver)
    details = page.get_product_details()

    assert details["title"], "Product title is missing"
    # assert details["price"].startswith("R"), "Price format is incorrect"
    # assert details["image"].startswith("https://"), "Image URL is invalid"
    # # assert "In Stock" in details["availability"] or "Available" in details["availability"], "Availability text missing"

    # Variant selection
    updated_price = page.select_variant_and_get_price("12 Months")
    assert updated_price.startswith("R"), "Updated price format is incorrect"

    # Add to cart
    page.add_product_to_cart()
    quantity = page.get_cart_quantity()
    assert quantity > 0, f"Expected quantity > 0, but got {quantity}"