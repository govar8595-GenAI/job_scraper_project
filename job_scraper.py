from playwright.sync_api import sync_playwright
import csv
import time
import os
from datetime import datetime


def create_output_folder():
    if not os.path.exists("output"):
        os.makedirs("output")


def scrape_jobs():
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://in.indeed.com")

        # Fill job title
        page.fill("input[name='q']", "Python Developer")

        # Fill location
        page.fill("input[name='l']", "Chennai")

        # Search
        page.press("input[name='q']", "Enter")

        time.sleep(3)

        listings = page.query_selector_all("div.job_seen_beacon")[:5]

        for job in listings:
            try:
                title_element = job.query_selector("h2.jobTitle")
                company_element = job.query_selector("span[data-testid='company-name']")
                location_element = job.query_selector("div[data-testid='text-location']")

                title = title_element.inner_text().strip() if title_element else "N/A"
                company = company_element.inner_text().strip() if company_element else "N/A"
                location = location_element.inner_text().strip() if location_element else "N/A"

                jobs.append([title, company, location])

            except Exception as e:
                print("Error extracting job:", e)

        page.screenshot(path="output/temp_screenshot.png")
        browser.close()

    return jobs


def save_files(jobs):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_path = f"output/jobs_{timestamp}.csv"
    screenshot_path = f"output/jobs_{timestamp}.png"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location"])
        writer.writerows(jobs)

    return csv_path, screenshot_path


def rename_screenshot(new_path):
    os.rename("output/temp_screenshot.png", new_path)


def open_files(csv_path, screenshot_path):
    os.system(f"open {csv_path}")
    os.system(f"open {screenshot_path}")


def main():
    try:
        create_output_folder()

        jobs = scrape_jobs()

        csv_path, screenshot_path = save_files(jobs)

        rename_screenshot(screenshot_path)

        open_files(csv_path, screenshot_path)

        print("Automation completed successfully.")

    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    main()