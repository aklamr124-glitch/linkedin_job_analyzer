import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- الإعدادات ---
# هنا بتحط المسار بتاع ChromeDriver اللي نزلته.
# مثال: 'C:/Users/amro/Downloads/chromedriver.exe'
# لو مش عارف المسار، سيبها فاضية بس تأكد إن ChromeDriver موجود في نفس مجلد المشروع
DRIVER_PATH = 'chromedriver.exe'

# الكلمات اللي عايز تبحث بيها
SEARCH_KEYWORDS = ["Python Automation", "Data Analyst", "Web Scraping"]

# المكان اللي عايز تبحث فيه
SEARCH_LOCATION = "Egypt" # لو عايز تدور في العالم كله سيبها فاضية ""

# --- بداية الكود ---
def scrape_linkedin_jobs():
    """
    يجمع بيانات الوظائف من LinkedIn بناءً على كلمات مفتاحية.
    """
    try:
        service = Service(DRIVER_PATH)
        options = Options()
        # لو عايز الكود يشتغل في الخلفية من غير ما يفتح متصفح، شيل علامة # من السطر اللي تحت
        # options.add_argument("--headless")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.linkedin.com/jobs/search/")
        print("فتح LinkedIn...")
        time.sleep(3)

        job_data_list = []

        for keyword in SEARCH_KEYWORDS:
            print(f"البحث عن وظائف: {keyword}")
            # البحث عن خانة البحث وإدخال الكلمة المفتاحية
            search_box = driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            # لو فيه مكان محدد للبحث، دخل المكان
            if SEARCH_LOCATION:
                location_box = driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input--location")
                location_box.clear()
                location_box.send_keys(SEARCH_LOCATION)
                location_box.send_keys(Keys.RETURN)
                time.sleep(3)
            
            # جمع البيانات من الصفحة
            job_listings = driver.find_elements(By.CLASS_NAME, "job-search-card")
            
            for job in job_listings:
                try:
                    title = job.find_element(By.CLASS_NAME, "base-search-card__title").text
                    company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
                    location = job.find_element(By.CLASS_NAME, "job-search-card__location").text
                    job_url = job.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute('href')
                    
                    job_data_list.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": location,
                        "URL": job_url
                    })
                except Exception as e:
                    print(f"حدث خطأ أثناء جمع بيانات وظيفة: {e}")
                    continue

        driver.quit()
        
        # تحويل البيانات لملف CSV
        if job_data_list:
            df = pd.DataFrame(job_data_list)
            df.to_csv("linkedin_jobs.csv", index=False)
            print("تم حفظ البيانات بنجاح في ملف linkedin_jobs.csv")
        else:
            print("لم يتم العثور على أي بيانات.")
            
    except Exception as e:
        print(f"حدث خطأ كبير في الكود: {e}")
        
if __name__ == "__main__":
    scrape_linkedin_jobs()
