from bs4 import BeautifulSoup
import re
import requests


def median(xs):
    sorted_xs = sorted(xs)
    n = len(xs)
    if n % 2 == 0:
        return (sorted_xs[n/2-1] + sorted_xs[n/2])/2
    else:
        return sorted_xs[n/2]


def get_classifieds(soup):
    classifieds = []
    classifieds_soup = soup.find_all("tr", id=re.compile("adv-result-[0-9]+"))
    for classified_tag in classifieds_soup:
        price = classified_tag.find("td", "spec").find("span").text.lower().replace(",", ".")
        desc_tag = classified_tag.find("td", id=re.compile("adv-result-title_description"))
        title = desc_tag.find("a").find("strong").text.lower()
        desc = desc_tag.find("a")["title"].lower()
        if price != "prijs o.t.k." and price != "n.v.t." and price != "ruilen":
            classifieds.append((float(price.split()[-1]), title, desc))
    return classifieds


classifieds = []

base_url = "http://www.2dehands.be/computer-game-consoles/computersystemen/ipad/"
base_soup = BeautifulSoup(requests.get(base_url).text)

pages = base_soup.find_all("a", href=re.compile("start="))
last_page = max(int(p.text) for p in pages if p.text.isdigit())

classifieds.extend(get_classifieds(base_soup))

for i in xrange(1, last_page):
    print "INFO: Getting Page {0} of {1}".format(i, last_page)
    url = base_url + "?start=" + str(i*35)
    soup = BeautifulSoup(requests.get(url).text)
    classifieds.extend(get_classifieds(soup))

prices = []

for classified in classifieds:
    price, title, desc = classified
    if "ipad 1" in title and ("16 gb" in title or "16gb" in title):
        prices.append(price)

print "INFO: Min Price: ", min(prices)
print "INFO: Max Price: ", max(prices)
print "INFO: Mean Price: ", median(prices)