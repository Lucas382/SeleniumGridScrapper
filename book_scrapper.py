import csv
from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Book():
    title: str
    price: str
    stock: str


def extract_html_element(html, selector, output):
    element = html.select_one(selector)
    if element is not None:
        if output == "text":
            return element.get_text(strip=True)
        elif output == "attrs":
            return element.attrs
        
def save_books_to_csv(books, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'Stock']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for book in books:
            writer.writerow({'Title': book.title, 'Price': book.price, 'Stock': book.stock})

def process_page(url):

    options = webdriver.ChromeOptions()

    #Conecta ao serviço remoto do Selenium Grid
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ol_list = soup.select_one('section div ol')

    books = []

    if ol_list:
        li_items = ol_list.find_all('li', recursive=False)

        for li in li_items:
            title = extract_html_element(li, 'h3 a', 'text')
            price = extract_html_element(li, '.price_color', 'text')
            stock = extract_html_element(li, '.availability', 'text')

            book = Book(title=title, price=price, stock=stock)

            books.append(book)

    driver.quit()
    return books
        
def main():

    max_pages = 20
    books = []
    urls = [f"https://books.toscrape.com/catalogue/page-{page}.html" for page in range(1, max_pages + 1)]


    #Separa em Threads a execução do processamento de cada pagina
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_page, urls)
        for result in results:
            books.extend(result)


    save_books_to_csv(books, "books.csv")

    


if __name__ == "__main__":
    main()
    print("Done!! All books Scraped.")
