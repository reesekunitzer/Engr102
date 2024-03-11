import requests 
import time 
from bs4 import BeautifulSoup as bs 

class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

def main():
    url = "https://quotes.toscrape.com/"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    
    quotes = [] 
    while True:
        time.sleep(1)
        relative_url = get_next_url(soup)
        if relative_url is None:
            break
        next_page = url + relative_url

        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))

    return

def get_shortest_and_longest(quotes):
    longest = 0
    shortest = 1000000
    longest_quote = " "
    shortest_quote = " "

    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longest_quote = quote.text

        if len(quote.text) < shortest:
            shortest = len(quote.text)
            shortest_quote = quote.text


    return

def get_next_url(soup: bs):
    list_item = soup.find("li", {"class": "next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    url = anchor["href"]

    return url

def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})

    quotes_list = []

    for quote in quotes: 
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        print(text)

        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        print(author)

        tags = quote.find_all("a", {"class": "tag"})
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip=True))
        print(tags_text)
        print("----------------------------------")

        
        quotes_list.append(Quote(text, author, tags_text))
        
    return quotes_list


if __name__ == "__main__":
    main()