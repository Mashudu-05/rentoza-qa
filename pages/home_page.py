from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.main_content = (By.CSS_SELECTOR, ".main-content")
        self.modal_close_button = (By.CLASS_NAME, "klaviyo-close-form")

    def wait_until_ready(self, timeout=15):
        wait = WebDriverWait(self.driver, timeout)

        try:
            # Wait for main content to be visible
            wait.until(EC.visibility_of_element_located(self.main_content))
        except Exception as e:
            print(f"Main content not visible: {e}")

        try:
            # If modal appears, close it
            modal = wait.until(EC.element_to_be_clickable(self.modal_close_button))
            modal.click()
        except Exception:
            # Modal didn't appear—no action needed
            pass