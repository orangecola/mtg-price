from puller import *
from cache import *
import sys, json, urllib, boto3, os
import traceback

def getArray(url):
	jsonoutput = []
	foil = "mtg_foil" in url
	raw_html = simple_get(url)
	raw_html2 = raw_html.replace(str.encode('\n</li>\n</li>\n</li>\n</li>'), str.encode(''))
	html = BeautifulSoup(raw_html2, 'html.parser')
	root = html.find("div", class_="col-sm-9 mainListing")
	children = root.findChildren(recursive=False)[1:]
	jsonoutput = []
	for child in children:
		title = child.find("span", class_="productDetailTitle").findChildren()[0].text
		cardSet = child.find("div", class_="productDetailSet").findChildren()[0].text.split("(")[0][:-1]
		prices = child.findAll("li", class_="itemAddToCart")
		print(title, cardSet)
		conditionsResult = ""
		priceResult = ""
		for price in prices:
			condition = price.find("input", class_="style")['value']
			stock = price.find("span", class_="styleQty").text
			stylePrice = price.find("span", class_="stylePrice").text.rstrip()
			if foil:
				condition += " Foil"		
			if int(stock) > 0 :
				print(condition, stylePrice)
				conditionsResult = condition if len(conditionsResult) == 0 else conditionsResult + "<br />" + condition
				priceResult = stylePrice if len(priceResult) == 0 else priceResult + "<br />" + stylePrice
			
		if len(conditionsResult) == 0:
			conditionsResult = "Sold Out"
			priceResult = "Sold Out"
		jsonoutput.append([title, cardSet, conditionsResult, priceResult, ""])
	return jsonoutput

def cardkingdom(searchTerm):
	cache = os.getenv("cache") == 'True'
	if cache: #Attempt to get from cache if caching enabled
		output = getFromCache("cache/cardkingdom-" + searchTerm)
		if len(output) > 0:
			return output
	searchTerm = searchTerm.replace("%20%2F%2F%20", "+")
	url = 'https://www.cardkingdom.com/catalog/search?filter%5Bipp%5D=60&filter%5Bsort%5D=name&filter%5Bname%5D='
	nonFoil = getArray(url + searchTerm)
	foil = getArray(url + searchTerm + '&filter[tab]=mtg_foil') 
	print("nonFoil")
	print(nonFoil)
	print("Foil")
	print(foil)
	combined = nonFoil
	for item in foil:
		if 'Sold Out' == item[2]:
			continue
		copy = list(filter(lambda x: x[1] == item[1], combined))
		if len(copy) == 0:
			combined.append(item)
			continue
		index = combined.index(copy[0])
		if "Sold Out" in combined[index][2]:
			combined[index][2] = item[2]
			combined[index][3] = item[3]
		else:
			combined[index][2] = combined[index][2] + "<br />" + item[2]
			combined[index][3] = combined[index][3] + "<br />" + item[3]
	if cache:
		saveToCache(combined, "cache/cardkingdom-" + searchTerm)
	return combined
	
if __name__ == '__main__':
	print(cardkingdom(sys.argv[1]))