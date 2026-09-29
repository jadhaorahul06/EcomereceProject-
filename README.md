# Ecommerce Project — Selenium Automation

Selenium automation script for the **TutorialsNinja Demo** e-commerce site,
built to satisfy the requirements below.

---

## Project Requirements

- [x] Open http://www.tutorialsninja.com/demo/
- [x] Select 2 iPhones
- [x] Take 1 screenshot
- [x] Select 1 Laptop (HP LP3065)
- [x] Select delivery date: 31-12-2022
- [x] Create a guest account and complete the checkout process
- [x] Print the total price and the confirmation message in the console

---

## What the Script Does

1. Launches Chrome and opens the TutorialsNinja demo store
2. Navigates to **Phones & PDAs -> iPhone**
3. Opens the product image gallery and takes 5 screenshots (1..5)
4. Sets quantity to **2** and adds the iPhone to the cart
5. Navigates to **Laptops & Notebooks -> HP LP3065**
6. Opens the datepicker calendar, navigates to **December 2022**,
   and selects **31-12-2022** as the delivery date
7. Adds HP LP3065 to the cart, then removes the iPhone from the cart
8. Proceeds to checkout as a **Guest**
9. Fills billing details (name, email, address, city, postcode)
   and selects **India / Maharashtra**
10. Continues through shipping method, agrees to terms,
    and continues through payment method
11. Prints the **final price** and the **order confirmation message**
    to the console

---

## Tech Stack

- Python 3.12
- Selenium 4.x
- Chrome + ChromeDriver (managed automatically by Selenium Manager)

---

## Setup

    git clone https://github.com/<your-username>/<repo-name>.git
    cd <repo-name>

    python -m venv .venv
    .venv\Scripts\activate        # Windows
    # source .venv/bin/activate   # macOS / Linux

    pip install -r requirements.txt

---

## Run

    python VerifyLink.py

---

## Project Structure

    EcomereceProject/
    |- VerifyLink.py         # Main automation script
    |- requirements.txt      # Python dependencies
    |- README.md             # This file
    |- .gitignore            # Git ignore rules
    |- screenshot_*.png      # Generated at runtime (ignored by git)

---

## Notes

- Screenshots are written to the project root at runtime and are
  intentionally ignored by Git.
- ChromeDriver is resolved automatically by Selenium Manager
  (Selenium >= 4.6), so no manual driver download is needed.

---

## Author

Rahul Jadhao
