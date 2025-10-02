from playwright.sync_api import sync_playwright
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        page.goto(f'file://{file_path}')

        # Wait for the calculator to be visible
        page.wait_for_selector('#details-productivity-manual')

        # Fill in the calculator inputs
        page.fill('#tx-time', '480')
        page.fill('#productivity-input', '90')
        page.fill('#clock-out', '17:30')
        page.fill('#lunch-out', '12:00')
        page.fill('#lunchIn', '12:30')

        # Click the "Get Productivity" button and verify
        page.click('button[data-action="get-productivity"]')
        from playwright.sync_api import expect
        expect(page.locator('#get-productivity-out')).to_have_text('94.1 %')

        # Click the "Get Clock Out" button and verify
        page.click('button[data-action="get-clock-out"]')
        expect(page.locator('#get-clock-out')).to_have_text('5:53 PM')

        # Take a screenshot of the day summary container
        summary_element = page.query_selector('#day-summary-container')
        if summary_element:
            summary_element.screenshot(path='jules-scratch/verification/calculator_verification.png')
        else:
            page.screenshot(path='jules-scratch/verification/calculator_verification.png')

        browser.close()

if __name__ == "__main__":
    run_verification()