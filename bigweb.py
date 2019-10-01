from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys, json, urllib, os, boto3

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

setParity = {
    "pFNM":"FNM",
    "MPS_AKH":"MPS2",
    "MED_RNA":"MED2",
    "pJGP":"JDG",
    "pMPR":"MPRP",
    "UBT":"UMA:BT",
	"WAR_EX":"WAR"
}

def nameTransformation(setCode, setName, cardName):
	if setCode == "WAR" and "Alterrnate-ART" in setName:
		cardName = cardName + " (JP Alternate Art)"
	if setCode == "UMA:BT" and "(" in cardName:
		cardName = cardName.split("(")[0]
	return cardName

def bigweb(searchTerm):
	s3 = boto3.resource('s3').Bucket(os.environ["cache_bucket"])
	json.load_s3 = lambda f: json.load(s3.Object(key=f).get()["Body"])
	json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))
	#Check cache for result
	try:
		output = json.load_s3("cache/bigweb-" + searchTerm)
		return output
	except:
		pass

	jsonoutput = []
	f = '{0}:\t{1}'

	raw_html = simple_get('https://mtg.bigweb.co.jp/cards/filter?big_keyword=' + searchTerm)
	html = BeautifulSoup(raw_html, 'html.parser')
	root = html.find("div", class_="row imageview")
	children = root.findChildren(recursive=False)

	setName = ""
	setCode = ""
	for i in range(0, len(children)):
		if 'item' in children[i]['class']:
			condition = ""
			price = ""
			#Display Card Name
			try:
				parsed_json = json.loads(children[i].findChildren(recursive=False)[0]['data-obj'])
				cardName = parsed_json['name'].replace(u'\u00b4', '\'')
				cardName = nameTransformation(setCode, setName, cardName)
			except:
				cardName = children[i].findChildren()[0].findChildren()[0].text.replace('\\u00b4', '\'')
				cardName = nameTransformation(setCode, setName, cardName)
				continue
			print(cardName)
			try:
				#Display Card Prices
				pricelist = children[i].findChildren(recursive=False)[0].findChildren(recursive=False)[3].findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)
			except:
				#Sold Out
				jsonoutput.append([cardName, setName, 'Sold out', '0円', setCode])
				print(f.format('Sold out', '0円'))
				continue
			pricelist = pricelist[:-1]
			for i in pricelist:
				cardCondition = i.findChildren(recursive=False)[0].findChildren(recursive=False)[0].text
				cardPrice = i.findChildren(recursive=False)[0].findChildren(recursive=False)[1].text
				print(f.format(condition, price))
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
				jsonoutput.append([cardName, setName, condition, price, setCode])
		else:
			#Display Set Name
			setName = children[i].findChildren()[0].findChildren()[1].findChildren()[0].text
			setCode = children[i].findChildren()[0].findChildren()[1].text.split(':')[0]
			if setCode in setParity:
				setCode = setParity[setCode]
			print (setName)
			print (setCode)

	jsonoutput = sorted(jsonoutput, key=lambda k:k[0])
	json.dump_s3(jsonoutput, "cache/bigweb-" + searchTerm)
	return jsonoutput
