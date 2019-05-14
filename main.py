from bigweb import bigweb
from tcgplayer import tcgplayer
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

def tcg_handler(event, context):

	searchTerm = event['pathParameters']['querystring']

	try:
		TCGresult = tcgplayer(searchTerm)
	except:
		traceback.print_exc()
		TCGresult = 0

	return formatOutput(TCGresult)

def big_handler(event, context):
	searchTerm = event['pathParameters']['querystring']

	try:
		BIGresult = bigweb(searchTerm)
	except:
		traceback.print_exc()
		BIGresult = 0

	return formatOutput(BIGresult)
