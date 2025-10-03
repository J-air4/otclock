import asyncio
from playwright.sync_api import sync_playwright, expect
import os
import re

def verify_ui_glitches():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        page.goto(f'file://{file_path}')

        # 1. Add a patient to the queue and schedule it
        page.locator('#patient-duration-input').fill('45')
        page.locator('button[data-action="add-patient"]').click()
        page.locator('button[data-action="auto-schedule"]').click()

        # Wait for the appointment to appear on the timeline
        appointment_on_timeline = page.locator('.timeline-appointment-item')
        expect(appointment_on_timeline).to_have_count(1)

        # 2. Hover over the appointment to check resize handles
        appointment_on_timeline.hover()

        # 3. Test settings panel stability
        # The "Work Day & Breaks" panel is open by default. Add a break.
        page.locator('button[data-action="add-break"]').click()

        # Wait for the notification that the break was added
        notification_container = page.locator('#notification-container')
        expect(notification_container).to_contain_text("New Break added.")

        # Scroll down to ensure the break is visible in the timeline
        timeline_scroll_container = page.locator('.timeline-scroll-container')
        timeline_scroll_container.evaluate('node => node.scrollTop = node.scrollHeight')

        # Check that the break item is now on the timeline
        expect(page.locator('div[data-id^="break-"]:has-text("New Break")')).to_be_visible()

        # Take a screenshot to verify the UI fixes
        page.screenshot(path="jules-scratch/verification/verification_ui_glitches.png")

        browser.close()

if __name__ == "__main__":
    verify_ui_glitches()