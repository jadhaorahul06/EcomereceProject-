from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime


# ==================================================
# 1. OPEN BROWSER
# ==================================================

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

driver.get("https://tutorialsninja.com/demo/")
driver.maximize_window()

print("Website opened successfully")


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_calendar_header():
    """Return visible bootstrap-datepicker header (Month Year)."""
    candidates = [
        "div.datepicker-days th.datepicker-switch",
        "div.datepicker-days th.picker-switch",
        "div.datepicker-days th.switch",
        "div.datepicker th.datepicker-switch",
        "div.datepicker th.picker-switch",
        "div.datepicker th.switch",
    ]
    for css in candidates:
        try:
            for e in driver.find_elements(By.CSS_SELECTOR, css):
                if e.is_displayed():
                    return e
        except Exception:
            continue
    return None


def get_visible_panel(*css_list):
    """Return first visible element matching any of the given CSS selectors."""
    for css in css_list:
        for e in driver.find_elements(By.CSS_SELECTOR, css):
            if e.is_displayed():
                return e
    return None


def dump_checkout_buttons():
    """Debug helper: print all visible buttons on the page."""
    print("=== VISIBLE BUTTONS ON PAGE ===")
    for b in driver.find_elements(By.XPATH, '//input[@type="button"] | //button'):
        try:
            if b.is_displayed():
                print(
                    "id:", b.get_attribute("id"),
                    "| name:", b.get_attribute("name"),
                    "| value:", b.get_attribute("value"),
                    "| text:", (b.text or "").strip()[:40]
                )
        except Exception:
            pass


def type_into(field_id, text):
    """
    Robust text-entry: re-locates element, types, verifies value stuck,
    retries once. Fires input/change/blur so OpenCart's validator sees it.
    """
    for attempt in range(2):
        try:
            el = wait.until(
                EC.element_to_be_clickable((By.ID, field_id))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
            el.clear()
            el.send_keys(text)

            driver.execute_script("""
                var el = arguments[0];
                el.dispatchEvent(new Event('input',  {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
                el.dispatchEvent(new Event('blur',   {bubbles: true}));
            """, el)

            if el.get_attribute("value") == text:
                return el

            print(f"  retry {field_id}: got '{el.get_attribute('value')}'")
            time.sleep(0.5)

        except Exception as e:
            print(f"  retry {field_id}: {e}")
            time.sleep(0.5)

    raise Exception(f"Could not set value for #{field_id}")


# ==================================================
# 2. OPEN PHONES & PDAs
# ==================================================

phone = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="menu"]/div[2]/ul/li[6]/a')
    )
)
phone.click()
print("Phones & PDAs opened")


# ==================================================
# 3. OPEN iPHONE
# ==================================================

iphone = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,
         '//*[@id="content"]/div[2]/div[2]/div/div[2]/div[1]/h4/a')
    )
)
iphone.click()
time.sleep(2)
print("iPhone product page opened")


# ==================================================
# 4. OPEN PRODUCT IMAGE
# ==================================================

product_image = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//ul[contains(@class,"thumbnails")]/li[1]/a/img')
    )
)
product_image.click()
time.sleep(2)
print("Product image popup opened")


# ==================================================
# 5. CLICK NEXT IMAGE AND TAKE SCREENSHOTS
# ==================================================

for i in range(5):
    next_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(@class,"mfp-arrow-right")]')
        )
    )
    next_click.click()
    time.sleep(1)

    driver.save_screenshot("screenshot_" + str(i + 1) + ".png")
    print("Screenshot taken:", i + 1)


# ==================================================
# 6. CLOSE IMAGE POPUP
# ==================================================

x_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(@class,"mfp-close")]')
    )
)
x_button.click()
time.sleep(1)
print("Image popup closed")


# ==================================================
# 7. CHANGE iPHONE QUANTITY
# ==================================================

quantity = wait.until(
    EC.element_to_be_clickable((By.ID, "input-quantity"))
)
quantity.clear()
quantity.send_keys("2")
print("Quantity changed to 2")


# ==================================================
# 8. ADD iPHONE TO CART
# ==================================================

add_to_button = wait.until(
    EC.element_to_be_clickable((By.ID, "button-cart"))
)
add_to_button.click()
time.sleep(3)
print("iPhone added to cart")


# ==================================================
# 9. OPEN LAPTOPS & NOTEBOOKS CATEGORY
# ==================================================

driver.get(
    "https://tutorialsninja.com/demo/index.php?route=product/category&path=18"
)
time.sleep(3)
print("Laptops & Notebooks category opened")
print("Current URL:", driver.current_url)
print("Current page title:", driver.title)


# ==================================================
# 10. OPEN HP LP3065 DIRECTLY
# ==================================================

driver.get(
    "https://tutorialsninja.com/demo/index.php?route=product/product&product_id=47"
)
time.sleep(3)
print("HP LP3065 product page opened")
print("Product URL:", driver.current_url)
print("Product page title:", driver.title)


# ==================================================
# 11. FIND ADD TO CART BUTTON
# ==================================================

add_to_button_2 = wait.until(
    EC.presence_of_element_located((By.ID, "button-cart"))
)


# ==================================================
# 12. SCROLL TO ADD TO CART BUTTON
# ==================================================

driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    add_to_button_2
)
time.sleep(1)


# ==================================================
# 13. OPEN DELIVERY DATE CALENDAR
# ==================================================

date_input = wait.until(
    EC.presence_of_element_located((By.ID, "input-option225"))
)

driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    date_input
)
time.sleep(1)

date_input.click()
time.sleep(0.5)

icon = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//i[contains(@class,"fa-calendar")]/..')
    )
)

if not any(
    d.is_displayed()
    for d in driver.find_elements(By.CLASS_NAME, "datepicker")
):
    icon.click()
    time.sleep(0.5)

wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.datepicker-days")
    )
)
print("Calendar opened")


# ==================================================
# 14. READ CURRENT CALENDAR MONTH
# ==================================================

header_elem = None
for _ in range(10):
    header_elem = get_calendar_header()
    if header_elem:
        break
    time.sleep(0.4)

if not header_elem:
    print("!!! Calendar header NOT found. Dumping calendar HTML: !!!")
    try:
        cal = driver.find_element(By.CSS_SELECTOR, "div.datepicker")
        print(cal.get_attribute("outerHTML"))
    except Exception:
        print("Could not find div.datepicker either.")
    raise Exception("Calendar header locator failed.")

print("Current calendar month:", header_elem.text.strip())


# ==================================================
# 15. TARGET DATE
# ==================================================

target_day = 31
target_month = 12      # December
target_year = 2022


# ==================================================
# 16. NAVIGATE: days -> months -> years
# ==================================================

header_days = get_calendar_header()
if not header_days:
    raise Exception("Days-view header not found.")
driver.execute_script("arguments[0].click();", header_days)
time.sleep(0.6)

months_panel = None
for _ in range(10):
    months_panel = get_visible_panel(
        "div.datepicker-months",
        "div.datepicker.months"
    )
    if months_panel:
        break
    time.sleep(0.3)

if not months_panel:
    print("Months panel not found — dumping HTML:")
    print(driver.find_element(
        By.CSS_SELECTOR, "div.datepicker"
    ).get_attribute("outerHTML"))
    raise Exception("Could not reach months view.")

header_months = get_calendar_header()
if not header_months:
    raise Exception("Months-view header not found.")
driver.execute_script("arguments[0].click();", header_months)
time.sleep(0.6)

years_panel = None
for _ in range(10):
    years_panel = get_visible_panel(
        "div.datepicker-years",
        "div.datepicker.years"
    )
    if years_panel:
        break
    time.sleep(0.3)

if not years_panel:
    raise Exception("Years view not found.")


# ==================================================
# 16a. NAVIGATE YEARS UNTIL TARGET YEAR VISIBLE
# ==================================================

MAX_YEAR_CLICKS = 30

for _ in range(MAX_YEAR_CLICKS):
    year_spans = years_panel.find_elements(By.CSS_SELECTOR, "span.year")
    year_values = [int(y.text) for y in year_spans if y.text.strip().isdigit()]

    if not year_values:
        break

    if target_year in year_values:
        break

    if max(year_values) < target_year:
        nxt = years_panel.find_element(By.CSS_SELECTOR, "th.next")
        driver.execute_script("arguments[0].click();", nxt)
    else:
        prv = years_panel.find_element(By.CSS_SELECTOR, "th.prev")
        driver.execute_script("arguments[0].click();", prv)

    time.sleep(0.3)

clicked_year = False
for y in years_panel.find_elements(By.CSS_SELECTOR, "span.year"):
    if y.text.strip() == str(target_year):
        driver.execute_script("arguments[0].click();", y)
        clicked_year = True
        break

if not clicked_year:
    raise Exception(f"Could not click year {target_year}")

time.sleep(0.6)


# ==================================================
# 16b. CLICK TARGET MONTH
# ==================================================

months_panel = None
for _ in range(10):
    months_panel = get_visible_panel(
        "div.datepicker-months",
        "div.datepicker.months"
    )
    if months_panel:
        break
    time.sleep(0.3)

if not months_panel:
    raise Exception("Months view not found after year click.")

target_month_abbr = datetime(2000, target_month, 1).strftime("%b")

clicked_month = False
for m in months_panel.find_elements(By.CSS_SELECTOR, "span.month"):
    if m.text.strip() == target_month_abbr:
        driver.execute_script("arguments[0].click();", m)
        clicked_month = True
        break

if not clicked_month:
    raise Exception(f"Could not click month {target_month_abbr}")

time.sleep(0.6)


# ==================================================
# 16c. VERIFY MONTH / YEAR
# ==================================================

header_days = get_calendar_header()
if header_days:
    print("Calendar now showing:", header_days.text.strip())


# ==================================================
# 17. SELECT DATE 31
# ==================================================

calendar_date = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//div[contains(@class,"datepicker-days")]'
            '//td[contains(@class,"day") '
            'and not(contains(@class,"old")) '
            'and not(contains(@class,"new")) '
            'and normalize-space(.)="' + str(target_day) + '"]'
        )
    )
)
calendar_date.click()
time.sleep(2)

print(f"{target_year}-{target_month:02d}-{target_day} selected")


# ==================================================
# 18. VERIFY SELECTED DATE
# ==================================================

selected_date = driver.find_element(
    By.ID, "input-option225"
).get_attribute("value")

print("Selected delivery date:", selected_date)


# ==================================================
# 19. ADD HP LP3065 TO CART
# ==================================================

add_to_button_2 = wait.until(
    EC.element_to_be_clickable((By.ID, "button-cart"))
)
add_to_button_2.click()
time.sleep(3)
print("HP LP3065 added to cart")


# ==================================================
# 19a. REMOVE iPHONE FROM CART
# ==================================================

cart_toggle = wait.until(
    EC.element_to_be_clickable((By.ID, "cart-total"))
)
cart_toggle.click()
time.sleep(1)

removed = False

try:
    iphone_remove_btn = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//div[@id="cart"]'
                '//tr[.//td//a[contains(text(),"iPhone")]]'
                '//button[contains(@onclick,"cart.remove")]'
            )
        )
    )
    driver.execute_script("arguments[0].click();", iphone_remove_btn)
    time.sleep(2)
    print("iPhone removed from cart")
    removed = True
except Exception as e:
    print("Button-based remove failed:", e)

if not removed:
    try:
        iphone_remove_link = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[@id="cart"]'
                    '//tr[.//td//a[contains(text(),"iPhone")]]'
                    '//a[contains(@onclick,"cart.remove")]'
                )
            )
        )
        driver.execute_script("arguments[0].click();", iphone_remove_link)
        time.sleep(2)
        print("iPhone removed from cart (link fallback)")
        removed = True
    except Exception as e:
        print("Link-based remove failed:", e)

if not removed:
    try:
        any_remove = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[@id="cart"]'
                    '//tr[.//td//a[contains(text(),"iPhone")]]'
                    '//*[contains(@onclick,"cart.remove")]'
                )
            )
        )
        driver.execute_script("arguments[0].click();", any_remove)
        time.sleep(2)
        print("iPhone removed from cart (generic fallback)")
        removed = True
    except Exception as e:
        print("Generic remove failed:", e)

if not removed:
    print("!!! Could not remove iPhone. Cart HTML: !!!")
    try:
        print(driver.find_element(By.ID, "cart").get_attribute("outerHTML"))
    except Exception:
        pass

try:
    cart_toggle.click()
    time.sleep(1)
except Exception:
    pass


# ==================================================
# 20. OPEN CART
# ==================================================

go_to_cart = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="cart-total"]'))
)
go_to_cart.click()
time.sleep(2)
print("Cart opened")


# ==================================================
# 21. CLICK CHECKOUT
# ==================================================

checkout = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="cart"]/ul/li[2]/div/p/a[2]')
    )
)
checkout.click()
time.sleep(3)
print("Checkout page opened")


# ==================================================
# 22. CHECKOUT ACCOUNT OPTIONS (TWO-STEP FLOW, NATIVE CLICKS)
# ==================================================
#
# OpenCart 3.x tutorialsninja checkout:
#
#   Step A: Checkout Options panel (id="collapse-checkout-option")
#           - radio name=account value=register
#           - radio name=account value=guest
#           - radio name=account value=login
#           - button #button-account (value="Continue")
#
#   Step B: After clicking #button-account with guest selected,
#           OpenCart AJAX-injects #button-guest into the DOM.
#
# #button-guest DOES NOT EXIST until #button-account is clicked.
#
# CRITICAL: Use NATIVE .click() everywhere here. JS clicks bypass
# the 'change' event bubbling that OpenCart's checkout JS relies on,
# which prevents the server-side session from advancing to Step 2.
# ==================================================

print("Current checkout URL:", driver.current_url)
print("Current checkout page title:", driver.title)

time.sleep(2)

# ------------------------------------------------------------
# Step A1: Ensure Checkout Options panel is expanded
# ------------------------------------------------------------
options_panel = driver.find_elements(By.ID, "collapse-checkout-option")
if options_panel and not options_panel[0].is_displayed():
    heading = driver.find_element(
        By.CSS_SELECTOR, 'a[href="#collapse-checkout-option"]'
    )
    heading.click()   # native
    time.sleep(1)

# ------------------------------------------------------------
# Step A2: Confirm guest radio exists
# ------------------------------------------------------------
guest_radios = driver.find_elements(
    By.CSS_SELECTOR, 'input[name="account"][value="guest"]'
)

if not guest_radios:
    print("Guest Checkout option NOT found")
    login_radios = driver.find_elements(
        By.CSS_SELECTOR, 'input[name="account"][value="login"]'
    )
    if login_radios:
        raise Exception("Login required; guest checkout not available.")
    else:
        print(driver.find_element(By.TAG_NAME, "body").text)
        raise Exception("Cannot proceed — no checkout option found.")

print("Guest Checkout option found")

# ------------------------------------------------------------
# Step A3: Select Guest Checkout radio — NATIVE click
# ------------------------------------------------------------
guest = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'input[name="account"][value="guest"]')
    )
)
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", guest
)
time.sleep(0.3)
guest.click()   # native click
time.sleep(0.5)
print("Guest radio selected:", guest.is_selected())

# ------------------------------------------------------------
# Step A4: Click #button-account — NATIVE click
# ------------------------------------------------------------
button_account = wait.until(
    EC.element_to_be_clickable((By.ID, "button-account"))
)
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", button_account
)
time.sleep(0.3)
button_account.click()   # native click
print("Clicked #button-account — waiting for guest panel to load …")

# ------------------------------------------------------------
# Step B1: Wait for #button-guest to appear
# ------------------------------------------------------------
continue_guest = None
for attempt in range(30):
    try:
        el = driver.find_element(By.ID, "button-guest")
        if el.is_displayed() and el.is_enabled():
            continue_guest = el
            print(f"#button-guest visible after {attempt + 1} attempt(s)")
            break
    except Exception:
        pass
    time.sleep(0.5)

if continue_guest is None:
    print("!!! #button-guest never became visible. Dumping state: !!!")
    dump_checkout_buttons()
    raise Exception("Guest Continue button (#button-guest) not visible.")

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", continue_guest
)
time.sleep(0.3)
continue_guest.click()   # native click
print("Clicked #button-guest — waiting for billing form …")

# ------------------------------------------------------------
# Step B2: Wait for billing form to appear
# ------------------------------------------------------------
wait.until(
    EC.visibility_of_element_located(
        (By.ID, "input-payment-firstname")
    )
)
print("Guest Checkout selected — billing form visible")

# ------------------------------------------------------------
# Step B3: Wait for country dropdown AJAX to finish
# ------------------------------------------------------------
print("Waiting for country dropdown to populate …")
wait.until(
    lambda d: len(
        d.find_elements(By.CSS_SELECTOR, "#input-payment-country option")
    ) > 1
)
print("Country dropdown ready")
time.sleep(1.5)


# ==================================================
# 23. ENTER BILLING DETAILS
# ==================================================

type_into("input-payment-firstname", "Rahul")
time.sleep(0.3)
type_into("input-payment-lastname", "Jadhao")
time.sleep(0.3)
type_into("input-payment-email", "test@test.com")
time.sleep(0.3)
type_into("input-payment-telephone", "9022113344")
time.sleep(0.3)
type_into("input-payment-address-1", "ADDRESS IS PUNE")
time.sleep(0.3)
type_into("input-payment-city", "Pune")
time.sleep(0.3)
type_into("input-payment-postcode", "411001")
time.sleep(0.3)

print("Billing text fields filled")


# ==================================================
# 24. SELECT COUNTRY
# ==================================================

country_el = wait.until(
    EC.visibility_of_element_located((By.ID, "input-payment-country"))
)
Select(country_el).select_by_visible_text("India")

# Fire change event natively
driver.execute_script("""
    var el = arguments[0];
    el.dispatchEvent(new Event('change', {bubbles: true}));
""", country_el)

print("Country selected: India")

wait.until(
    lambda d: len(
        d.find_elements(By.CSS_SELECTOR, "#input-payment-zone option")
    ) > 1
)
time.sleep(1)
print("Zone dropdown populated")


# ==================================================
# 25. SELECT REGION / STATE
# ==================================================

region_el = wait.until(
    EC.visibility_of_element_located((By.ID, "input-payment-zone"))
)
Select(region_el).select_by_visible_text("Maharashtra")

driver.execute_script("""
    var el = arguments[0];
    el.dispatchEvent(new Event('change', {bubbles: true}));
""", region_el)

time.sleep(1)
print("Region selected: Maharashtra")


# ==================================================
# 26. VERIFY FIELDS + CONTINUE BILLING (RESILIENT)
# ==================================================

# Re-verify all text fields survived the country/zone AJAX
print("Verifying field values before Continue …")
expected = {
    "input-payment-firstname": "Rahul",
    "input-payment-lastname": "Jadhao",
    "input-payment-email": "test@test.com",
    "input-payment-telephone": "9022113344",
    "input-payment-address-1": "ADDRESS IS PUNE",
    "input-payment-city": "Pune",
    "input-payment-postcode": "411001",
}
for fid, want in expected.items():
    got = driver.find_element(By.ID, fid).get_attribute("value")
    status = "OK" if got == want else "MISMATCH"
    print(f"  {fid}: {status} (got='{got}')")
    if got != want:
        type_into(fid, want)
        time.sleep(0.2)

c_val = Select(
    driver.find_element(By.ID, "input-payment-country")
).first_selected_option.text
z_val = Select(
    driver.find_element(By.ID, "input-payment-zone")
).first_selected_option.text
print(f"  country: {c_val}")
print(f"  zone: {z_val}")

# ---- Find the correct Step-2 continue button ----
time.sleep(1.5)
print("=== Buttons before advancing billing ===")
dump_checkout_buttons()

form_el = driver.find_element(By.ID, "input-payment-firstname")
form_y  = form_el.location['y']

continue_2 = None
for bid in ["button-payment-address", "button-guest", "button-register"]:
    try:
        el = driver.find_element(By.ID, bid)
        if el.is_displayed() and el.is_enabled():
            # Must be BELOW the billing form (Step 2 continue)
            if el.location['y'] > form_y:
                continue_2 = el
                print(f"Using #{bid} to continue billing")
                break
    except Exception:
        continue

if continue_2 is None:
    print("!!! No Step-2 continue button found below the form. Dump: !!!")
    dump_checkout_buttons()
    print("=== Button positions ===")
    for b in driver.find_elements(
        By.XPATH, '//input[@type="button"] | //button'
    ):
        try:
            if b.is_displayed():
                print(
                    f"  id={b.get_attribute('id')} "
                    f"y={b.location['y']} "
                    f"value={b.get_attribute('value')}"
                )
        except Exception:
            pass
    raise Exception("Could not find billing continue button")

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", continue_2
)
time.sleep(0.3)
continue_2.click()   # native click
print("Billing details completed")
time.sleep(3)


# ==================================================
# 27. SHIPPING METHOD
# ==================================================

try:
    continue_3 = wait.until(
        EC.visibility_of_element_located((By.ID, "button-shipping-method"))
    )
except Exception:
    print("button-shipping-method not found — dumping buttons:")
    dump_checkout_buttons()
    raise

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});",
    continue_3
)
time.sleep(0.3)
continue_3.click()   # native click
time.sleep(3)
print("Shipping method continued")


# ==================================================
# 28. AGREE TO TERMS
# ==================================================

t_e = wait.until(
    EC.presence_of_element_located((By.NAME, "agree"))
)
if not t_e.is_selected():
    t_e.click()   # native click
time.sleep(1)


# ==================================================
# 29. CONTINUE PAYMENT METHOD
# ==================================================

try:
    continue_4 = wait.until(
        EC.visibility_of_element_located((By.ID, "button-payment-method"))
    )
except Exception:
    print("button-payment-method not found — dumping buttons:")
    dump_checkout_buttons()
    raise

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});",
    continue_4
)
time.sleep(0.3)
continue_4.click()   # native click
time.sleep(3)
print("Payment method continued")


# ==================================================
# 30. GET FINAL PRICE
# ==================================================

final_price = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            '//table[@class="table table-bordered table-hover"]'
            '/tfoot/tr[3]/td[2]'
        )
    )
)
print("Final price of products: " + final_price.text)


# ==================================================
# 31. CONFIRM ORDER
# ==================================================

confirmation_button = wait.until(
    EC.element_to_be_clickable((By.ID, "button-confirm"))
)
confirmation_button.click()
time.sleep(3)


# ==================================================
# 32. ORDER SUCCESS MESSAGE
# ==================================================

success_text = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//div[@class="col-sm-12"]/h1')
    )
)
print("Order confirmation:", success_text.text)
time.sleep(2)


# ==================================================
# 33. TEST COMPLETED
# ==================================================

print("----------------------------------")
print("TEST EXECUTION COMPLETED")
print("----------------------------------")


# ==================================================
# 34. CLOSE BROWSER
# ==================================================

driver.quit()
print("Browser closed")