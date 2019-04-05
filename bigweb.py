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

def bigweb(searchTerm):
	jsonoutput = []
	f = '{0}:\t{1}'	

	#print('https://mtg.bigweb.co.jp')

	raw_html = simple_get('https://mtg.bigweb.co.jp/cards/filter?big_keyword=' + searchTerm)
	html = BeautifulSoup(raw_html, 'html.parser')
	root = html.find("div", class_="row imageview")
	children = root.findChildren(recursive=False)

	setName = ""
	for i in range(0, len(children)):
		if 'item' in children[i]['class']:
			#Display Card Name
			try:
				parsed_json = json.loads(children[i].findChildren(recursive=False)[0]['data-obj'])
				cardName = parsed_json['name']
			except:
				cardName = children[i].findChildren()[0].findChildren()[0].text
			print(cardName)
			try:
				#Display Card Prices
				pricelist = children[i].findChildren(recursive=False)[0].findChildren(recursive=False)[3].findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)
			except:
				#Sold Out
				jsonoutput.append([cardName, setName, 'Sold out', '0円'])
				print(f.format('Sold out', '0円'))
				continue
			pricelist = pricelist[:-1]
			for i in pricelist:
				condition = i.findChildren(recursive=False)[0].findChildren(recursive=False)[0].text 
				price = i.findChildren(recursive=False)[0].findChildren(recursive=False)[1].text
				print(f.format(condition, price))
				jsonoutput.append([cardName, setName, condition, price])
		else:
			#Display Set Name
			setName = children[i].findChildren()[0].findChildren()[1].findChildren()[0].text
			print (setName)

	jsonoutput = sorted(jsonoutput, key=lambda k:k[0])		
	return jsonoutput