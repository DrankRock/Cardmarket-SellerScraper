import csv
import re
import sys
import time
import argparse
from tqdm import tqdm

import requests
import lxml
from bs4 import BeautifulSoup

headers_list = [{
    'Host': 'www.cardmarket.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}, {
    'Host': 'www.cardmarket.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}, {
    'Host': 'www.cardmarket.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}, {
    'Host': 'www.cardmarket.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}]

session = None
SLEEP_TIME = 5


def init_process():
    """
    Initialize the session for the requests
    """
    global session
    session = requests.Session()


def request_block(input_url):
    """
    Does a request with timeout of 8. If connection refuser, sleep for some time.
    This is to avoid drowning cardmarket with requests while the ip is blocked

    :param input_url: the url to request
    :return: the soup associated to the response
    """
    tries = 1
    working = True
    while True:
        try:
            if tries >= 13:
                raise ValueError("REQUEST NOT WORKING AFTER 70 SEC")
            # proxy = prox.randomProxy()
            # proxyDict = {'http': proxy, 'https': proxy}
            # headers = random.choice(headers_list)
            # response = session.get(input_url.url, headers=headers, proxies=proxyDict, timeout=5)
            # response = session.get(input_url, timeout=5)
            response = session.get(input_url, timeout=8)

            if response.status_code == 429:
                raise ValueError("TOO MANY REQUESTS")
        # text = "Status_code : {} - proxy : {} - {} tries".format(response.status_code,proxy,tries)
        except Exception as exp:
            print(exp)
            if tries >= 14:
                working = False
                break
            else:
                tries = tries + 1
                time.sleep(SLEEP_TIME)
                continue
        break
    if working:
        soup = BeautifulSoup(response.text, 'lxml')
        # list_scrap = scrapers.CMSoupScraper(input_url.url, soup)
        # sellers = []
        # if check_sellers and list_scrap != -1:
        #     sellers = findTopSellers.soupToTopXSellers(soup, n_sellers)
        # if list_scrap != -1:
        #     list_scrap.insert(0, input_url.attribute)
        return soup
    else:
        return -1


def scraping(url, seller):
    """
    Scrapes a url by creating the soup, and finding all the data with regex operations
    :param url: the page url
    :param seller: the name of the seller
    :return: a list of list of each item to sell
    """
    soup = request_block(url)
    if soup != -1 :
        table_body = soup.find('div', class_='table-body')
        article_divs = table_body.find_all('div',
                                           {'class': 'row no-gutters article-row', 'id': lambda x: x.startswith('article')})
        out = []

        for div in article_divs:
            current = [seller]
            line = f"{div}"
            soup2 = BeautifulSoup(line, "html.parser")
            name_info = soup2.findAll("div", class_="row no-gutters")
            temp = re.findall(r'<a(.*?)</a>', str(name_info[0]))[0]
            name = re.findall(r'">(.*?)$', temp)[0]
            mouse_overs = re.findall(r'title="(.*?)"', str(div))
            if "&lt;img" in mouse_overs[0]:
                mouse_overs = mouse_overs[1:]
            infos_list = mouse_overs.copy()
            for i in range(1, len(mouse_overs)):
                if mouse_overs[i] == mouse_overs[i-1] :
                    infos_list.remove(mouse_overs[i])
            mouse_overs = infos_list
            lst = [mouse_overs[0], name, mouse_overs[1], mouse_overs[2], mouse_overs[3]]
            current += lst
            price = re.findall(r'<span class="font-weight-bold color-primary small '
                               r'text-right text-nowrap">(.*?)</span>', str(div))[0]
            current.append(price)
            quantity = re.findall(r'<span class="item-count small text-right">(.*?)</span>', str(div))[0]
            current.append(quantity)
            out.append(current)
        return out
    else:
        return -1


def main(url, filename):
    """
    Main function to scrape all the pages in a user, and output to filename
    :param url: url to scrape
    :param filename: csv file to output
    """
    current_url = url
    init_process()
    soup = request_block(url)
    if soup == -1:
        print("Request could not be possible, are you sure that the entered url is correct ?")
        sys.exit(1)

    num_page_html = soup.find_all('span', class_="mx-1")
    page_num = num_page_html[-1]
    max_page = int(re.findall("\d+", str(page_num))[-1])
    if max_page == 15:
        print("Max page 15, csv output will contain only the first 300 elements")
    seller_html = soup.find("div", class_="flex-grow-1")
    seller = re.findall(r"<h1>(.*?)<span", str(seller_html))[0]

    print("Scraping the {} pages from the link of seller {}".format(max_page, seller))
    pbar1 = tqdm(total=max_page, position=1)
    if "site=" in current_url:
        current_url = re.sub("site=\d", "", url)
    if "?" not in current_url:
        current_url += "?"
    all = []
    error_pages=[]
    for i in range(1, max_page + 1):
        page_i = current_url + "&site=" + str(i)
        page_i_result = scraping(page_i, seller)
        if page_i_result != -1 :
            all += page_i_result
        else :
            error_pages.append(i)
        pbar1.update(1)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['seller', 'expansion', 'name', 'rarity', 'condition', 'language', 'price', 'quantity'])
        for line in all:
            writer.writerow(line)
    if len(error_pages) > 0:
        print("ERROR : some pages could not be scraped : ")
        for elem in error_pages :
            print("page ", str(elem))
    print("")


parser = argparse.ArgumentParser(description='Scrape the items sold by a seller on Cardmarket')
parser.add_argument('-u', '--url', type=str, required=True, help='url to a seller page containing items, such as the single page')
parser.add_argument('-o', '--output', type=str, required=True, help='path to the csv file used as output')

args = parser.parse_args()

main(args.url, args.output)
