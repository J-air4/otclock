import asyncio
from playwright.sync_api import sync_playwright, expect
import os
import re

def verify_productivity():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        page.goto(f'file://{file_path}')

        # 1. Add a patient and auto-schedule
        page.locator('#patient-duration-input').fill('60')
        page.locator('button[data-action="add-patient"]').click()

        # Wait for notification
        notification_container = page.locator('#notification-container')
        expect(notification_container).to_contain_text("Patient P1 added to queue.")

        page.locator('button[data-action="auto-schedule"]').click()

        # Wait for notification
        expect(notification_container).to_contain_text("1 patient(s) auto-scheduled!")

        # Wait for the appointment to appear on the timeline
        appointment_on_timeline = page.locator('.timeline-appointment-item')
        expect(appointment_on_timeline).to_have_count(1)

        # 2. Verify Productivity Calculation
        clock_out_input_container = page.locator('.custom-time-input[data-id="productivity.endTime"]')
        hour_input = clock_out_input_container.locator('.time-input-hour')
        minute_input = clock_out_input_container.locator('.time-input-minute')

        hour_input.fill("9")
        minute_input.fill("30")
        page.locator('h2:has-text("Day Summary")').click()

        productivity_value_element = page.locator("div.grid > div:nth-child(3) > div.font-bold")
        expect(productivity_value_element).to_have_text("100.0%")
        expect(productivity_value_element).to_have_class(re.compile(r'text-green-400'))

        # 3. Take final screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    verify_productivity()