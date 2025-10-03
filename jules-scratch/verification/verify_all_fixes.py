import asyncio
from playwright.sync_api import sync_playwright, expect
import os
import re

def verify_all_fixes():
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

        # 2. Verify "Actionable Insights" is removed
        actionable_insights_header = page.locator('h4:has-text("Actionable Insights")')
        expect(actionable_insights_header).to_have_count(0)

        # 3. Verify Productivity Calculation
        clock_out_input_container = page.locator('.custom-time-input[data-id="productivity.endTime"]')
        hour_input = clock_out_input_container.locator('.time-input-hour')
        minute_input = clock_out_input_container.locator('.time-input-minute')

        hour_input.fill("9")
        minute_input.fill("30")
        page.locator('h2:has-text("Day Summary")').click()

        productivity_value_element = page.locator("div.grid > div:nth-child(3) > div.font-bold")
        expect(productivity_value_element).to_have_text("100.0%")
        expect(productivity_value_element).to_have_class(re.compile(r'text-green-400'))

        # 4. Verify settings panel stability by adding a break
        page.locator('button[data-action="add-break"]').click()
        expect(notification_container).to_contain_text("New Break added.")

        timeline_scroll_container = page.locator('.timeline-scroll-container')
        timeline_scroll_container.evaluate('node => node.scrollTop = node.scrollHeight')

        expect(page.locator('div[data-id^="break-"]:has-text("New Break")')).to_be_visible()

        # 5. Re-optimize and verify
        page.locator('button[data-action="reoptimize"]').click()
        expect(notification_container).to_contain_text("Schedule has been re-optimized.")

        # The appointment should be rescheduled around the break
        expect(appointment_on_timeline).to_have_count(1)

        # 6. Take final screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    verify_all_fixes()