from bs4 import BeautifulSoup
from selenium import webdriver
import csv

the_list = []

page_count  = int(input("Enter How many page do you want to scrap  > "))
search = input("Enter Job Title, Keywords, Company > ")
search = search.replace(" ", "+")


for page_number in range(page_count):
    page = f"https://www.indeed.com/jobs?q={search}&start={page_number * 10}"
    driver = webdriver.Edge()
    driver.get(page)
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    cards = soup.find_all("div", class_="job_seen_beacon")
    for card in cards:
        job_link = card.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")
        if job_link:
            job_link = job_link.get("href")
            driver2 = webdriver.Edge()
            driver2.get("https://www.indeed.com"+job_link)
            src2 = driver2.page_source
            soup2 = BeautifulSoup(src2, 'html.parser')
            job_name = soup2.find("h1")
            if job_name:
                job_name = job_name.text.strip()
            company_name = soup2.find('div', {'data-company-name': 'true', 'data-testid': 'inlineHeader-companyName'})
            if company_name:
                company_name = company_name.text.strip()           
            location = soup2.find('div', {'data-testid': 'inlineHeader-companyLocation'})
            if location:
                location = location.text.strip()
            else:
                location = "Not Avalible"
            job_info = soup2.find("span", class_="eu4oa1w0")

            if job_info:
                job_info = job_info.text.strip()

            else:
                job_info = "Remote"

            the_list.append({"Job Title":job_name,                            
                            "Company":company_name,                           
                            "Location":location,
                            "Job Info":job_info,
                            "Job Link":f"https://www.indeed.com/"+job_link,
                            })
            
            
keys = the_list[0].keys()


with open("jobs.csv","w" , newline="" , encoding="UTF-8") as f:

    writer = csv.DictWriter(f,keys)
    writer.writeheader()
    writer.writerows(the_list)

    print("File Created")


        

driver.quit()
