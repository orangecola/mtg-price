from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys, json, urllib
import json
import os


def tcgplayer(searchTerm):

	#Get API Token
	parameters = {"grant_type": "client_credentials", "client_id":os.environ["client_id"], "client_secret":os.environ["client_secret"]}
	response = get("https://api.tcgplayer.com/token", data=parameters)
	token = json.loads(response.content)
	authorization_header = {"Authorization": ("Bearer " + token["access_token"]), "Content-Type": "application/json"}

	#Get Card IDs
	searchTerm = urllib.parse.unquote(searchTerm)
	cardSearchData = {
    "sort": "name",
    "filters": [
        {
            "name": "ProductName",
            "values": [
                urllib.parse.unquote(searchTerm)
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

	response = post("http://api.tcgplayer.com/v1.19.0/catalog/categories/1/search", headers=authorization_header, data=json.dumps(cardSearchData))
	searchResult = json.loads(response.content)

	cardIds = searchResult["results"]
	cardIdsStr = ','.join(map(str, cardIds))

	#Get Set Information
	response = get("http://api.tcgplayer.com/v1.19.0/catalog/products/" + cardIdsStr, headers=authorization_header)
	cardDetails = json.loads(response.content)
	cardDetails = cardDetails["results"]
	cardDetails = sorted(cardDetails, key=lambda k:k["name"])

	#Get Prices
	response = get("http://api.tcgplayer.com/v1.19.0/pricing/product/" + cardIdsStr, headers=authorization_header)
	prices = json.loads(response.content)
	prices = prices["results"]

	groups=[]
	for i in cardDetails:
		groups.append(i["groupId"])

	groupIdsStr = ','.join(map(str, groups))

	#Get Group Ids
	response = get("http://api.tcgplayer.com/v1.19.0/catalog/groups/" + groupIdsStr, headers=authorization_header)
	groups = json.loads(response.content)
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
	return output
