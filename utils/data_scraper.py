from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import traceback
from urllib.parse import urlencode
from selenium.common.exceptions import TimeoutException
from utils.salary_extractor import extract_upper_salary

jobs = []


def data_scraper(position, batch, location, desired_salary):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration (optional)
    chrome_options.add_argument("--no-sandbox")  # Useful in some environments like Docker (optional)
    
    # Initialize the WebDriver with the headless options
    driver = webdriver.Chrome(options=chrome_options)
    try:
        for page in range(1,3):

            params = {
                'position': position,
                'batch': batch,
                'location': location,
            }
            if page > 1:
                params['page'] = page

            url = f"https://thejobcompany.in/?{urlencode(params, doseq=True)}"
            driver.get(url)

            try:
                # Wait for the job posts to load
                print(f"Waiting for job posts to load on page {page}...")
                job_posts = WebDriverWait(driver,30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'job-listing'))
                )
                if not job_posts:
                    print(f"No job posts found on page {page}. Closing browser.")
                    break

                print(f"Job posts loaded on page {page}.")

                # Extract job post details
                for post in job_posts:
                    try:
                        company_title = post.find_element(By.XPATH, ".//p[contains(@class, 'company-title')]").text
                        company_name = company_title.split(' is hiring')[0]
                        title_name = company_title.split(' is hiring')[1].strip()
                        batch_name = post.find_element(By.XPATH, ".//p/strong[contains(text(), 'Batch :')]/..").text.split(":")[1].strip()
                        location_name = post.find_element(By.XPATH, ".//p/strong[contains(text(), 'Location :')]/..").text.split(":")[1].strip()
                        salary_range = post.find_element(By.XPATH, ".//p/strong[contains(text(), 'Salary :')]/..").text.split(":")[1].strip()
                        job_apply_url = post.find_element(By.XPATH, ".//a[contains(@class, 'job-apply')]").get_attribute("href")

                        if extract_upper_salary(salary_range) >= desired_salary:
                            jobs.append({"company": company_name, "title": title_name, "batch": batch_name, "location": location_name, "salary": salary_range, "url": job_apply_url})
                        ##Check the salary range

                    except Exception as e:
                        print(f"Error extracting job details: {e}")
                        traceback.print_exc()

            except TimeoutException:
                print(f"No job posts found on page {page} due to timeout. Closing browser.")
                break
            except Exception as e:
                print(f"An error occurred on page {page}: {e}")
                traceback.print_exc()
                break

    finally:
        driver.quit()
        print("Browser closed successfully")
    return jobs