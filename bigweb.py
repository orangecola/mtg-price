from puller import *

import sys, json, urllib, os

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
	cache = os.getenv("cache") == 'True' #Filter to enable / disable caching
	if cache: #Attempt to get from cache if caching enabled
		from cache import saveToCache, getFromCache
		output = getFromCache("cache/bigweb-" + searchTerm)
		if len(output) > 0:
			return output

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
				pricelist = children[i].find("div", class_="card-img-box-caption-up ").findChildren(recursive=False)[0]
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
	if cache:
		saveToCache(jsonoutput, "cache/bigweb-" + searchTerm)
	return jsonoutput

if __name__ == '__main__':
	print(bigweb(sys.argv[1]))