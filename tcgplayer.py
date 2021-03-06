from puller import *
import sys, json, urllib
import json
import os
import boto3

def tcgplayer(searchTerm):
	token = ''
	cache = os.getenv("cache") == 'True' #Filter to enable / disable caching
	if cache: #Attempt to get from cache if caching enabled
		from cache import saveToCache, getFromCache
		output = getFromCache("cache/tcgplayer-" + searchTerm)
		if len(output) > 0:
			return output
	
		#Check cache for Token
		logging.info("Attempting to get TCGPlayer Key from Cache")
		token = getFromCache("tcgplayer-key")

	#If no token in cache, get API Token
	if len(token) == 0:
		parameters = {"grant_type": "client_credentials", "client_id":os.environ["client_id"], "client_secret":os.environ["client_secret"]}
		response = post("https://api.tcgplayer.com/token", data=parameters)
		token = json.loads(response.content.decode("utf-8"))
		if cache:
			saveToCache(token, "tcgplayer-key")
	
	
	authorization_header = {"Authorization": ("Bearer " + token["access_token"]), "Content-Type": "application/json"}
	
	#Get Card IDs
	searchTerm2 = urllib.parse.unquote(searchTerm)
	cardSearchData = {
    "sort": "name",
	"offset": 0,
    "filters": [
        {
            "name": "ProductName",
            "values": [
                urllib.parse.unquote(searchTerm2)
            ]
        },
        {
            "name": "Rarity",
            "values": [
                "M", "R", "U", "C", "L", "S", "P"
            ]
        }
    ]
    }
	cardIds=[]
	offset = 0
	while True:
		response = post("https://api.tcgplayer.com/v1.19.0/catalog/categories/1/search", headers=authorization_header, data=json.dumps(cardSearchData))
		searchResult = json.loads(response.content.decode("utf-8"))
		cardIds += searchResult["results"]
		totalItems = searchResult["totalItems"]
		offset += 10
		if offset > totalItems:
			break 
		cardSearchData["offset"] = offset
	cardIdsStr = ','.join(map(str, cardIds))
	#Get Set Information
	response = get("https://api.tcgplayer.com/v1.19.0/catalog/products/" + cardIdsStr, headers=authorization_header)
	cardDetails = json.loads(response.content.decode("utf-8"))
	cardDetails = cardDetails["results"]
	cardDetails = sorted(cardDetails, key=lambda k:k["name"])

	#Get Prices
	response = get("https://api.tcgplayer.com/v1.19.0/pricing/product/" + cardIdsStr, headers=authorization_header)
	prices = json.loads(response.content.decode("utf-8"))
	prices = prices["results"]

	groups=[]
	for i in cardDetails:
		groups.append(i["groupId"])

	groupIdsStr = ','.join(map(str, groups))

	#Get Group Ids
	response = get("https://api.tcgplayer.com/v1.19.0/catalog/groups/" + groupIdsStr, headers=authorization_header)
	groups = json.loads(response.content.decode("utf-8"))
	groups = groups["results"]

	output = []
	for i in cardDetails:
		name = i["name"]
		set = ""
		condition = ""
		price = ""
		for j in groups:
			if j["groupId"] == i["groupId"]:
				set = j["name"]
				setCode = j["abbreviation"]
		for j in prices:
			if j["productId"] == i["productId"]:
				if j["marketPrice"] != None:
					condition = j["subTypeName"] if len(condition) == 0 else condition + "<br />" + j["subTypeName"]
					price = str(j["marketPrice"]) if len(price) == 0 else price + "<br />" + str(j["marketPrice"])
		output.append([name, set, condition, price, setCode])
	if cache:
		saveToCache(output, "cache/tcgplayer-" + searchTerm)
	return output

if __name__ == '__main__':
	logging.info(tcgplayer(sys.argv[1]))