from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys, json, urllib
import json
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def hareruya(searchTerm):
	jsonoutput = []

	raw_html = simple_get('https://www.hareruyamtg.com/en/products/search?product=' + searchTerm)
	html = BeautifulSoup(raw_html, 'html.parser')
	root = html.find("ul", class_="itemListLine itemListLine--searched")
	children = root.findChildren(recursive=False)

	for i in range(0, len(children)):
		try:
			condition = ""
			price = ""
			alt = children[i].findChildren(recursive=False)[1].text
			foil = '【Foil】' in alt
			cardName = alt.split('《')[1].split('》')[0]
			setCode = alt.split('[')[1].split(']')[0]
			if 'PRE' in setCode:
				setCode = 'PRE'
			lang = alt.split('【')[1].split('】')[0]
			if lang == 'EN':
				lang = '英'
			elif lang == 'JP':
				lang = '日'
			print(cardName)
			print(setCode)
			print(lang)
			prices = children[i].findChildren(recursive=False)[2].findChildren(recursive=False)
			#print(prices)
			for j in range(1, len(prices)):
				row = prices[j]
				stock = int(row.findChildren(recursive=False)[2].text)
				if stock > 0:
					cardCondition = row.findChildren(recursive=False)[0].findChildren(recursive=False)[0].text.strip()
					cardPrice = row.findChildren(recursive=False)[1].text.split( )[0] + '円'
					cardCondition = '[' + lang + ':' + cardCondition + ']'
					if foil:
						cardCondition += 'Foil'
					print(cardCondition)
					print(cardPrice)
					condition = cardCondition if len(condition) == 0 else condition + "<br />" + cardCondition
					price = cardPrice if len(price) == 0 else price + "<br />" + cardPrice
			if len(condition) == 0:
				continue
			duplicate = False
			for k in jsonoutput:
				if cardName == k[0] and setCode == k[4]:
					duplicate = True
					k[2] += "<br />" + condition
					k[3] += "<br />" + price
					break
			if not duplicate:
				jsonoutput.append([cardName, "", condition, price, setCode])
		except:
			continue
	jsonoutput = sorted(jsonoutput, key=lambda k:k[0])
	return jsonoutput
