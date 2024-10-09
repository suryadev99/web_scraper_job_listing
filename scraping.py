from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime, timedelta
import re  #
import random


# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# Target URL
url = "https://www.gaapweb.com/jobs/"
driver.get(url)

# List to store job data
job_data = []

# Function to extract job details
def extract_job_data():
    # Wait for jobs to be present on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'lister__header'))
    )

    wait = WebDriverWait(driver, 10)

    # Wait for the job listings to load
    jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.lister__item')))

    # Create an empty list to store the job data
    # job_data = []

    # Loop through each job listing
    print("jobs", len(jobs))
    for job in jobs:
        try:
            job_title = job.find_element(By.CSS_SELECTOR, 'h3.lister__header a span').text.strip()
            print(job_title)
            # Wait and extract job title
            # job_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.lister__header a span'))).text
            print( "1",job_title)

            # Extract job URL
            job_url = job.find_element(By.CSS_SELECTOR, 'h3.lister__header a').get_attribute('href')
            print(job_url)


            company_name = job.find_element(By.CSS_SELECTOR, 'li.lister__meta-item--recruiter').text
            print(company_name)

            # Extract location
            location = job.find_element(By.CSS_SELECTOR, 'li.lister__meta-item--location').text
            print(location)

            # Extract salary (optional)
            salary_elements = job.find_elements(By.CSS_SELECTOR, 'li.lister__meta-item--salary')
            salary = salary_elements[0].text if salary_elements else 'N/A'
            print(salary)

            # Extract recruiter name (optional)
            recruiter_elements = job.find_elements(By.CSS_SELECTOR, 'li.lister__meta-item--recruiter')
            recruiter = recruiter_elements[0].text if recruiter_elements else 'N/A'
            print("rec",recruiter)

            # Extract short description
            description = job.find_element(By.CSS_SELECTOR, 'p.lister__description').text
            print("dec",description)

            # Extract the date posted
            date_posted_element = job.find_element(By.CSS_SELECTOR, 'li.job-actions__action.pipe').text.strip()
            print("Date Posted:", date_posted_element)

            # Extract the number of days ago posted
            days_ago = int(re.search(r'(\d+)', date_posted_element).group(1))  # Extract the number of days using regex
            actual_date_posted = datetime.now() - timedelta(days=days_ago)  # Calculate the actual date
            print("Actual Date Posted:", actual_date_posted.strftime('%Y-%m-%d'))

            # if ['£' , 'GBP'] not in salary:
            if not re.search(r'\d', salary):
                salary_in_description = re.search(r'£\d+(?:,\d+)?(?:\.\d+)?', description)
                print("jkol", salary_in_description)
            if salary_in_description:
                salary = f"{salary} ({salary_in_description.group(0)})" if salary != 'N/A' else salary_in_description.group(0)
                print("final", salary)
                # Add job data to the list
            job_data.append({
                'Job Title': job_title,
                'Company Name': company_name,
                'Location': location,
                'Salary': salary,
                'Recruiter': recruiter,
                'Job URL': job_url,
                'Description': description,
                'Date Posted': actual_date_posted.strftime('%Y-%m-%d')  # Format the date as needed
            })
        except Exception as e:
            print(f"Error extracting job data: {e}")
# Function to handle pagination
def scrape_all_pages():
    count = 0
    while True:
        extract_job_data()  # Extract job data from the current page
        try:
            # Wait for the next button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.paginator__item a[rel="next"]'))
            )
            next_button.click()  # Click on the next button
            count+=1
            print("page_nu",count)
            if count == 15 :
                break
            time.sleep(random.randint(2, 3))  # Wait for the new page to load
        except Exception as e:
            print(f"No more pages to scrape or error encountered.{e}")
            break

# Start scraping
scrape_all_pages()

print(job_data)
# Convert to DataFrame and display
df = pd.DataFrame(job_data)
print(df.head())
df.to_csv('webscraped_data.csv', index=False)
# Clean up
driver.quit()
