from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
from selenium_stealth import stealth
import re

def initialize_driver():
    # INSERT BEFORE USE
    # User Agent Strings | https://www.useragentstring.com/pages/Browserlist/
    user_agents = [
        ]
    user_agent = random.choice(user_agents)

    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={user_agent}")
    #chrome_options.add_argument("--headless") # run in the background
    #chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Apply stealth settings to the driver
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver
def get_links(html):

    links = []
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all('a', {'type': 'link', 'class': 'commandLink_TITLE-BLUE'})
    for title in titles:
        links.append(title.attrs["href"])
    if len(links) > 1:
        print("Multiple links found")
    else:
        print("Nah")

    return links

def fetch_info(url):
    driver = initialize_driver()
    info = {}
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")


        #Title
        title = soup.find("div", {'class' : 'formOutputText_HIDDEN-LABEL outputText_TITLE-BLACK', 'style' : 'text-align: left;'})
        if title:
            info["Title"] = title.text.strip()
            print(f"Title: {info['Title']}")
        else:
            print(f"No Title at {url}")

        # Quotation

        quotation_div = soup.find("div",
                               {"id": "contentForm:j_idt251", 'class': 'formOutputText_MAIN form2_ROW-SEPARATOR'})
        if quotation_div:
            quotation_label = quotation_div.find_next('label', {'for': 'contentForm:j_idt251_inputTextarea'})
            if 'Quotation No.' in quotation_label.get_text(strip=True):
                quotation_name = quotation_div.find_next('div', {'class': 'formOutputText_VALUE-DIV',
                                                           'style': 'text-align: left;'})
                if quotation_name:
                    info["Quotation No."] = quotation_name.get_text(strip=True)
                    print(f"Quotation No.: {info['Quotation No.']}")
                else:
                    print("No Quotation No. name found")
            else:
                print("Label does not contain 'Quotation No.'")
        else:
            print("Quotation No. div not found")


        #Tender
        tender_div = soup.find("div",
                               {"id": "contentForm:j_idt251", 'class': 'formOutputText_MAIN form2_ROW-SEPARATOR'})
        if tender_div:
            print("Found tender_div")
            tender_label = tender_div.find_next('label', {'for': 'contentForm:j_idt251_inputTextarea'})
            if tender_label:
                print("Found tender_label")
                if 'Tender No.' in tender_label.get_text(strip=True):
                    print("Label contains 'Tender No.'")
                    tender_name = tender_div.find_next('div', {'class': 'formOutputText_VALUE-DIV',
                                                               'style': 'text-align: left;'})
                    if tender_name:
                        info["Tender No."] = tender_name.get_text(strip=True)
                        print(f"Tender No.: {info['Tender No.']}")
                    else:
                        print("No Tender No. name found")
                else:
                    print("Label does not contain 'Tender No.'")
            else:
                print("Tender label not found")
        else:
            print("Tender No. div not found")




        # Agency
        agency_div = soup.find("div",
                                {"id": "contentForm:j_idt253", 'class': 'formOutputText_MAIN form2_ROW-SEPARATOR'})
        if agency_div:
            agency_label = agency_div.find_next('label', {'for': 'contentForm:j_idt253_inputTextarea'})
            if 'Agency' in agency_label.get_text(strip=True):
                agency_name = agency_div.find_next('div', {'class': 'formOutputText_VALUE-DIV',
                                                                   'style': 'text-align: left;'})
                if agency_name:
                    info["Agency"] = agency_name.get_text(strip=True)
                    print(f"Agency: {info['Agency']}")
                else:
                    print("No Agency name found")
            else:
                print("Label does not contain 'Agency'")
        else:
            print("Agency div not found")



        # Find the procurement category
        category_div = soup.find("div", {"id": "contentForm:j_idt286", 'class': 'formOutputText_MAIN'})
        if category_div:
            category_label = category_div.find('label', {'for': 'contentForm:j_idt286_inputTextarea'})
            if category_label and 'Procurement Category' in category_label.get_text(strip=True):
                category_name = category_div.find_next('div', {'class': 'formOutputText_VALUE-DIV',
                                                                             'style': 'text-align: left;'})
                if category_name:
                    info["Procurement Category"] = category_name.get_text(strip=True)
                    print(f"Procurement Category: {info['Procurement Category']}")
                else:
                    print("No Procurement Category name found")
            else:
                print("Label does not contain 'Procurement Category'")
        else:
            print("Procurement Category div not found")

        #Awarding Agency
        award_div = soup.find("div", {"id": "contentForm:j_idt483:j_id29:j_idt485", 'class': 'formOutputText_MAIN'})
        if award_div:
            award_label = award_div.find('label', {'for': 'contentForm:j_idt483:j_id29:j_idt485_inputTextarea'})
            if award_label and 'Awarding Agency' in award_label.get_text(strip=True):
                award_name = award_div.find_next('div', {'class': 'formOutputText_VALUE-DIV',
                                                               'style': 'text-align: left;'})
                if award_name:
                    info["Awarding Agency"] = award_name.get_text(strip=True)
                    print(f"Awarding Agency: {info['Awarding Agency']}")
                else:
                    print("No Awarding Agencyname found")
                    info["Awarding Agency"] = "N/A"
            else:
                print("Label does not contain 'Awarding Agency'")
                info["Awarding Agency"] = "N/A"
        else:
            print("Awarding Agencydiv not found")
            info["Awarding Agency"] = "N/A"


# EMAIL
        def extract_emails(strings):
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = set()
            for string in strings:
                found_emails = re.findall(email_pattern, string)
                for email in found_emails:
                    emails.add(email)

            return list(emails)

        # Find all strings containing "@" and extract emails
        strings_with_emails = soup.find_all(string=lambda string: string and "@" in string)
        unique_emails = extract_emails(strings_with_emails)

        # Add emails to the info dictionary and print them

        for i, email in enumerate(unique_emails):
            info[f"Email {i + 1}"] = email
            print(f"Email {i + 1}:", email)


    except Exception as e:
        print(f"An error occurred with URL {url}: {e}")
        return None

    finally:
        return info


def main():
    driver = initialize_driver()
    links = []
    failed_links = []
    data = []
    base =  # Constant link e.g. www.youtube.com 
    test = # follows after base
    driver.get(test)

    # Closed Tenders
    xpath1 = "//input[@id='contentForm:j_idt800_TabAction_1']" # specific element on the page to extract
    try:
        # Find the closed button
        closed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath1)))
        closed_button.click()
        print("Clicked CLOSED TENDER")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath1))
        )  # Wait for the next page to load
        time.sleep(5)  # Allow some time for the page to load completely
    except Exception as e:
        print(f"Failed to click closed tender button: {e}")
        driver.quit()


    page = 2

    # Get all links
    while True:
        try:
            xpath = f"//input[@id='contentForm:j_idt912:j_idt963_{page}_{page}']"
            print("Page:", page)
            # Get all links from the current page
            new_links = get_links(driver.page_source)
            links.extend(new_links)

            # Wait for the "Next" button to be clickable and click it
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            next_button.click()
            print("Clicked NEXT PAGE")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )  # Wait for the next page to load
            time.sleep(5)  # Allow some time for the page to load completely
            page += 1
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break

    print(f"There are {len(links)} links")



    # Fetch info from all collected links
    try:
        for link in links:
            url = base + link
            company_info = fetch_info(url)
            print("\n")
            if company_info:
                data.append(company_info)
            else:
                failed_links.append(url)

    except Exception as e:
        print("An error occurred:", e)


    finally:
        df = pd.DataFrame(data)
        print(df.head())
        df.to_excel('CLOSEDGeBizTenderRequests.xlsx', index=False)

        driver.quit()




        print("Failed links:", set(failed_links))

main()



