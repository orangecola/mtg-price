from bigweb import bigweb
from tcgplayer import tcgplayer
from hareruya import hareruya
from cardkingdom import cardkingdom
import json
import sys
import logging
import traceback
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
	logging.info("Function started with input:")
	logging.info(event)
	searchTerm = event['pathParameters']['querystring']
	try:
		result = function(searchTerm)
		logging.info("Function completed with output:")
		logging.info(result)
	except:
		exception_type, exception_value, exception_traceback = sys.exc_info()
		traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
		err_msg = json.dumps({
			"errorType": exception_type.__name__,
			"errorMessage": str(exception_value),
			"stackTrace": traceback_string
		})
		logging.error(err_msg)
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
