from playwright.sync_api import sync_playwright, expect
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        page.goto(f'file://{file_path}')

        # 1. Add a patient and schedule them
        page.fill('#patient-duration-input', '30')
        page.click('button[data-action="add-patient"]')
        page.click('button[data-action="auto-schedule"]')

        # Verify the appointment is scheduled at 8:35 AM (8:30 start + 5 min default setup)
        appointment_item = page.locator('.timeline-appointment-item')
        expect(appointment_item).to_be_visible()
        expect(appointment_item).to_contain_text('8:35 AM')

        # 2. Increase setup time to create a gap
        page.click('#details-tasks summary')
        setup_time_input = page.locator('input[data-field="setupTime"]')
        expect(setup_time_input).to_be_visible()
        setup_time_input.fill('15')

        # Click out to trigger the change and wait for UI to update
        page.click('body')
        page.wait_for_timeout(500) # Give time for re-render

        # 3. Click the "Re-optimize" button
        page.click('button[data-action="reoptimize-schedule"]')

        # 4. Verify the schedule has been re-optimized
        # The appointment should now start at 8:45 AM (8:30 start + 15 min new setup)
        reoptimized_appointment = page.locator('.timeline-appointment-item')
        expect(reoptimized_appointment).to_be_visible()
        expect(reoptimized_appointment).to_contain_text('8:45 AM')

        # Take a screenshot
        page.screenshot(path='jules-scratch/verification/reoptimize_verification.png')

        browser.close()

if __name__ == "__main__":
    run_verification()