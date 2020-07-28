from bigweb import bigweb
from tcgplayer import tcgplayer
from hareruya import hareruya
from cardkingdom import cardkingdom
import json
import traceback

def formatOutput(output):
	return {
		"statusCode": 200,
		"headers": {
			"Access-Control-Allow-Origin": "*",
			"Access-Control-Allow-Headers": "Content-Type",
			"Access-Control-Allow-Methods": "OPTIONS,GET"
		},
		"body": json.dumps(output)
	}

def runFunction(function, event):
	print("Function started with input:", event)
	searchTerm = event['pathParameters']['querystring']
	try:
		result = function(searchTerm)
		print("Function completed with output:",result)
	except:
		print("Function halted with exception:")
		traceback.print_exc()
		result = 0
	return formatOutput(result)

def tcg_handler(event, context):
	return runFunction(tcgplayer, event)

def big_handler(event, context):
	return runFunction(bigweb, event)

def har_handler(event, context):
	return runFunction(hareruya, event)

def car_handler(event, context):
	return runFunction(cardkingdom, event)
