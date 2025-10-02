from playwright.sync_api import sync_playwright, expect
import os

def run_verification(page):
    # Get the absolute path to the HTML file
    file_path = os.path.abspath('index.html')
    page.goto(f'file://{file_path}')

    # Add a patient to the queue
    page.locator("#patient-duration-input").fill("30")
    page.locator("button[data-action='add-patient']").click()
    expect(page.locator(".patient-item").first).to_be_visible()

    # Drag the patient to the timeline to create an appointment
    patient_item = page.locator(".patient-item").first
    timeline_gap = page.locator(".timeline-gap").first
    patient_item.hover()
    page.mouse.down()
    timeline_gap.hover()
    page.mouse.up()

    # Expect the appointment to be created
    appointment_item = page.locator(".timeline-appointment-item").first
    expect(appointment_item).to_be_visible()

    # Add a break
    page.locator("button[data-action='add-break']").click()
    expect(page.locator("div[data-id^='break-']")).to_be_visible()

    # Add a task
    page.locator("#details-tasks summary").click()
    page.locator("button[data-action='add-task']").click()
    expect(page.locator("div[data-id^='otherTask-']")).to_be_visible()

    # Resize the appointment
    resize_handle = appointment_item.locator(".resize-handle.bottom")
    box = resize_handle.bounding_box()
    if box:
        drag_start_x = box['x'] + box['width'] / 2
        drag_start_y = box['y'] + box['height'] / 2

        page.mouse.move(drag_start_x, drag_start_y)
        page.mouse.down()
        page.mouse.move(drag_start_x, drag_start_y + 60)
        page.mouse.up()

    # Toggle the workday panel closed for the screenshot
    page.locator("#details-workday summary").click()

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    run_verification(page)
    browser.close()