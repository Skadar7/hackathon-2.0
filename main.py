import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import pandas as pd
import re


class HackPars:
    def __init__(self, file):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options,
                                  executable_path=r"chromedriver.exe")

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        self.file = file
        self.links = []
        self.company_and_texts = []

    def write_company_info(self):
        data = pd.DataFrame(self.company_and_texts).to_csv('link_adn_text.csv', encoding='cp1251')
        data1 = pd.DataFrame(self.company_and_texts)
        print(data1)

    def get_links(self):
        print('Ищу ссылки...')
        exel_file = pd.read_excel(r'C:\Users\Professional\Desktop\cmp.xlsx')
        temp = 0
        for link in exel_file['Сайт']:
            temp += 1
            url = f'{link}'
            print(url)
            self.links.append(url)
            self.company_and_texts.append({'link': url, 'text': ''})
            self.driver.get(url)
            menu_links = self.driver.find_element(By.LINK_TEXT, 'О компании')#.find_elements(By.TAG_NAME, 'a')#find_element(By.XPATH, "//nav[contains( text(), 'О компании')]").click()#find_elements(By.TAG_NAME, 'a')#.#или nav, пока так#
            #print(menu_links.get_attribute('href'))
            self.links.append(menu_links.get_attribute('href'))
            """for menu_link in menu_links:
                link = menu_link.get_attribute('href')
                print(link)
                if url in link:
                    self.links.append(link)"""
            if temp > 10:
                break

    def get_text(self):
        l = len(self.links)
        print(f'Записываю текст, еще осталось {l}')
        i = 0
        temp = 0
        for link in self.links:
            temp += 1
            print(link)
            self.driver.get(link)
            if self.company_and_texts[i]['link'] not in link:
                i += 1
            self.company_and_texts[i]['text'] += re.sub(r'[^А-Яа-я]', ' ',
                                                        self.driver.find_element(By.XPATH, '/html/body').text)
            l -= 1
            print(f'Записываю текст, еще осталось {l}')
            print(self.company_and_texts)
            if temp > 10:
                break



start = HackPars(r'C:\Users\Professional\Desktop\cmp.csv')
start.get_links()
start.get_text()
start.write_company_info()

