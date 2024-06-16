""""Main app for scrapping"""
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    """Main Function"""
    driver = webdriver.Chrome()

    # List that will store the scraped data
    data = [['title', 'href']]
    for i in range(1, 10):
        base_url = os.getenv('URL')
        url = base_url + str(i)
        driver.get(url)

        # Asserts that the page is loaded to start the next step
        _ = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "olx-button__content-wrapper"))
        )

        # Parsing through the html content in order to find the img urls
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        tags = soup.find_all('li', class_="olx-image-carousel__item")
        for tag in tags:
            images = tag.find_all('img')
            for img in images:
                title = img['alt']
                src = img['src']
                data.append([title, src])

    # Writing into csv formating for later use
    with open('results.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    driver.close()

if __name__ == '__main__':
    main()
