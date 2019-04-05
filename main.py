from bigweb import bigweb
from tcgplayer import tcgplayer
import json
import traceback


def main_handler(event, context):

	searchTerm = event['queryStringParameters']['querystring']
	'''
	try:
		TCGresult = tcgplayer(searchTerm)
	except: 
		traceback.print_exc()
		TCGresult = 0
	'''
	try:
		BIGresult = bigweb(searchTerm)
	except:
		traceback.print_exc()
		BIGresult = 0
	
	#final = {"tcgplayer":TCGresult, "bigweb":BIGresult}
	return {
        "statusCode": 200,
        "headers": {
		    "Access-Control-Allow-Origin": "*",
		    "Access-Control-Allow-Headers": "Content-Type",
		    "Access-Control-Allow-Methods": "OPTIONS,GET"
		  },
        "body": json.dumps(BIGresult)
    }
	