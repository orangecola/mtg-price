from puller import *
import sys, json, urllib, boto3, os
import traceback

setParity = {
    "Judge Foil":"JDG",
	"ZvE":"DDP",
	"FtV:Transform":"V17",
	"FtV:Angels":"V15",
	"The List":"TLP"
}


def hareruya(searchTerm):
	cache = os.getenv("cache") == 'True' #Filter to enable / disable caching
	if cache: #Attempt to get from cache if caching enabled
		from cache import saveToCache, getFromCache
		output = getFromCache("cache/hareruya-" + searchTerm)
		if len(output) > 0:
			return output
	jsonoutput = []

	raw_html = simple_get('https://www.hareruyamtg.com/en/products/search?product=' + searchTerm.replace("%20%2F%2F%20", "+"))
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
			cardName = cardName.replace("+", " // ")
			setCode = alt.split('[')[1].split(']')[0]
			if 'PRE' in setCode:
				setCode = 'PRE'
			lang = alt.split('【')[1].split('】')[0]
			if lang == 'EN':
				lang = '英'
			elif lang == 'JP':
				lang = '日'
			logging.info(cardName)
			logging.info(setCode)
			logging.info(lang)
			prices = children[i].findChildren(recursive=False)[1].findChildren(recursive=False)
			#logging.info(prices)
			for j in range(1, len(prices)):
				row = prices[j]
				
				cardPrice = row.findChildren(recursive=False)[0].text.split()[1] + '円'
				cardCondition =  row.findChildren(recursive=False)[1].text.strip().split()[0][1:]
				cardCondition = '[' + lang + ':' + cardCondition + ']'
				if foil:
					cardCondition += 'Foil'
				logging.info(cardCondition)
				logging.info(cardPrice)
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
		except Exception as e:
			track = traceback.format_exc()
			logging.info(track)

	jsonoutput = sorted(jsonoutput, key=lambda k:k[0])
	for i in jsonoutput:
		if i[4] in setParity:
			i[4] = setParity[i[4]]
	if cache:
		saveToCache(jsonoutput, "cache/hareruya-" + searchTerm)
	return jsonoutput

if __name__ == '__main__':
	logging.info(hareruya(sys.argv[1]))