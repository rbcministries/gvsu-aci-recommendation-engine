from time import sleep
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import csv
import re
import os

output_file = os.path.join(os.path.dirname(__file__), 'odb_pages_text.csv')
# sites = ["https://odbu.org/", "https://whereyafrom.org/", "https://discoveryseries.org/"]
sites = ["https://odb.org/", "https://odbu.org/", "https://whereyafrom.org/", "https://discoveryseries.org/"]
headers = ['url', 'text']
book_count_threshold = 1
books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth,' 
    '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 
    'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 
    'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 
    'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 
    'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 
    'Titus', 'Philemon', 'Hebrew', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

processed_urls = set()
internal_urls = set()

total_urls_visited = 0

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawl(url, webdriver: webdriver, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"[*] Crawling: {url}")
    links = get_all_website_links(url, webdriver)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, webdriver, max_urls=max_urls)

def get_all_website_links(url, webdriver: webdriver):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    try:
        webdriver.get(url)
        # Just sleep a few seconds to wait for page to load. 
        # Speed isn't super important right now
        sleep(3)
        reached_page_end = False
        last_height = webdriver.execute_script("return document.body.scrollHeight")

        while not reached_page_end:
            driver.find_element_by_xpath('//body').send_keys(Keys.END)   
            sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                reached_page_end = True
            else:
                last_height = new_height

        html = webdriver.page_source
        processed_urls.add(url)
    except:
        return urls

    text = webdriver.find_element_by_tag_name('body').text
    text = text.replace('\n', ' ')
    text = re.sub(r'[^a-zA-Z0-9:–\' ]', '', text).lower()
    
    # booksCounts = {}
    # for book in books:
    #     count = text.count(book)
    #     if count >= book_count_threshold:
    #         booksCounts[book] = count
    
    # if len(booksCounts) > 0:
    with open(output_file, 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([url, text])
        # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not href.endswith('/'):
            href = href + '/'
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if f'://{domain_name}/' not in href:
            # external link
            continue
        if 'login' in href:
            # don't care about login stuff
            continue
        if href.split('\\')[-1] == url.split("\\")[-1]:
            continue
        print(f"[*] Internal link: {href}")

        urls.add(href)
        internal_urls.add(href)
    return urls


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

with open(output_file, 'w+', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(headers)

for url in sites:
    crawl(url, driver, 3000)

print("[+] Total Internal links:", len(internal_urls))
# print("[+] Total External links:", len(external_urls))
# print("[+] Total URLs:", len(external_urls) + len(internal_urls))
print("[+] Total crawled URLs:", total_urls_visited)
