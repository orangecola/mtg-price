import json, boto3, botocore, os
import traceback
s3 = boto3.resource('s3').Bucket(os.environ["cache_bucket"])
json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))

def saveToCache(jsonOutput, key):
    json.dump_s3(jsonOutput, key)

def getFromCache(key):
    try:
        response = s3.Object(key).get()["Body"].read().decode("utf-8")
        print("Cache Hit")
        output = json.loads(response)
        return output
    except:
        print("Cache Miss")
        return ''