import os
from playwright.sync_api import sync_playwright, Page, expect

def run_verification(page: Page):
    """
    Verifies the core functionality changes: appointment overlapping and re-optimization.
    """
    # Get the absolute path to the index.html file
    file_path = os.path.abspath('index.html')

    # 1. Navigate to the local HTML file
    page.goto(f'file://{file_path}')

    # 2. Wait for the main heading to be visible to ensure the app has loaded
    expect(page.get_by_role("heading", name="Interactive Therapy Scheduler")).to_be_visible()

    # 3. Add two patients to the queue
    # Patient 1: 30 minutes
    page.get_by_placeholder("Duration (min)").fill("30")
    page.locator('button[data-action="add-patient"]').click()
    # Patient 2: 50 minutes
    page.get_by_placeholder("Duration (min)").fill("50")
    page.locator('button[data-action="add-patient"]').click()

    # Expect to see both patients in the queue
    expect(page.locator('.patient-item')).to_have_count(2)

    # 4. Drag and drop both patients to the first gap to create an overlap
    first_patient = page.locator('.patient-item').first
    second_patient = page.locator('.patient-item').last
    first_gap = page.locator('.timeline-gap').first

    first_patient.drag_to(first_gap)
    # Wait for the first appointment to appear on the timeline before dragging the second
    expect(page.locator('.timeline-appointment-item')).to_have_count(1)

    second_patient.drag_to(first_gap)

    # 5. Verify that two appointments are now on the timeline and take a screenshot
    expect(page.locator('.timeline-appointment-item')).to_have_count(2)
    page.screenshot(path="jules-scratch/verification/01_overlapping_appointments.png")

    # 6. Click the "Re-Optimize" button
    page.get_by_role('button', name='Re-Optimize', exact=True).click()

    # 7. Verify that the appointments are rescheduled automatically.
    # The auto-scheduler runs after the re-optimize action.
    # We expect to see both appointments back on the timeline.
    expect(page.locator('.timeline-appointment-item')).to_have_count(2)

    # 8. Take a final screenshot of the re-optimized schedule
    page.screenshot(path="jules-scratch/verification/02_reoptimized_schedule.png")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        run_verification(page)
        browser.close()

if __name__ == "__main__":
    main()