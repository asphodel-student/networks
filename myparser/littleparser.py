from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup as bs
import pandas as pd
    

def parse_this_page(address: str) -> str:
    """
    Function for parsing web page.
    Args:
    address : str -> web page address

    Output:
    path_to_table : str -> name of created file
    """

    # Create a web driver
    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    current_page = 1
    items, price, describtion = [], [], []
    while True:  
        # Getting next page's text and parsing it
        site_address = address + f'?page={current_page}'
        driver.get(site_address)
        html = driver.page_source
        soup = bs(html, features='html.parser')

        founded_items = []; founded_price = []; founded_describtion = []

        # Finding all items
        for tag in soup.find_all('a', class_='link'):
            valid_tag = filter_tags(tag)
            if valid_tag: 
                founded_items.append(tag.text)

        # Finding item's price
        for tag in soup.find_all('span', class_='price__value'):
            founded_price.append(tag.text)

        # Finding name of a company
        for tag in soup.find_all('div', class_='item__mnf'):
            founded_describtion.append(tag.text)

        # A little kostlyl'. If there're no founded companies, it means that there're no pages anymore.
        if len(founded_describtion) == 0:
            break

        items += founded_items[1:]
        price += founded_price[1:]
        describtion += founded_describtion[:]

        # Printing debug information
        print(f'Page: {current_page}, founded items: {len(founded_items)}')
        current_page += 1
        
        
    # Saving all data
    price = pd.Series(price, name='Price')
    items = pd.Series(items, name='Items')
    describtion = pd.Series(describtion, name='Company')

    data_to_save = pd.DataFrame({'Items' : items, 'Company: ' : describtion, 'Price ' : price})
    path_to_table = 'data.csv'
    data_to_save.to_csv(path_to_table)

    # Closing the session
    driver.quit()

    return path_to_table


# Filter-function
def filter_tags(tag):
    if len(tag['class']) == 1:
        return 1
    else:
        return 0