import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os


def main():
    i = 1
    while i in range(1, 475):
        link = str(i).zfill(3)
        driver = webdriver.Edge()
        driver.get(f"https://sejm.gov.pl/Sejm9.nsf/posel.xsp?id={link}&type=A")
        time.sleep(1)
        title = driver.title
        title = title.replace(' - Sejm Rzeczypospolitej Polskiej', '')
        print(title)

        osw_button = driver.find_element(By.ID, "osw")
        time.sleep(1)
        osw_button.click()
        osw_button.click()
        time.sleep(1)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        pdf_links = [link.get('href') for link in links if link.get('href').endswith('.pdf')]

        if not os.path.exists(f"posłowie/{title}"):
            os.makedirs(f"posłowie/{title}")

        for link in pdf_links:
            # Pobieranie pliku PDF
            response = requests.get(link)
            # Parsowanie nazwy pliku z atrybutu 'title' linku
            for l in links:
                if l.get('href') == link:
                    filename = l.get('title') + '.pdf'
                    break
            # Zapisywanie pliku PDF
            with open(os.path.join(f"posłowie/{title}", filename), 'wb') as f:
                f.write(response.content)
            time.sleep(1)

        driver.close()
        i += 1


if __name__ == '__main__':
    main()
