# Takes entity/relation as input and links it to DBpedia.
# Need to add additional code to rank the DBpedia results based on context and choose the best matching entity.
# Reference: https://medium.com/analytics-vidhya/entity-linking-a-primary-nlp-task-for-information-extraction-22f9d4b90aa8

import requests
import json
import time
from retry import retry

class EntityRecognitionLinking:

    class APIError(Exception):

        def __init__(self, status):
            self.status = status

        def __str__(self):
            return "APIError: status={}".format(self.status)

    @retry(Exception, backoff=100, tries=3, delay=20)
    def call_api(self, base_url, params, headers, proxies):
        res = requests.get(base_url, params=params, headers=headers, proxies=proxies)
        if res.status_code != 200:
            raise Exception("Cannot call Api")
        else:
            return res

    def entityRecogLink(self, text):

        # Base URL for Spotlight API
        base_url = "http://api.dbpedia-spotlight.org/en/annotate"
        # Parameters
        # 'text' - text to be annotated
        # 'confidence' -   confidence score for linking
        #params = {"text": "My name is Sundar. I am currently doing Master's in Artificial Intelligence at NUS. I love Natural Language Processing.", "confidence": 0.35}
        params = {"text": text, "confidence": 0.35}
        # Response content type
        #headers = {'accept': 'text/html'}
        headers = {'accept': 'application/json'}
        # GET Request
        proxies = {
            "http": "http://lum-customer-beeking-zone-shopify_zone-country-us:47aryubjyvol@zproxy.lum-superproxy.io:22225",
            "https": "https://lum-customer-beeking-zone-shopify_zone-country-us:47aryubjyvol@zproxy.lum-superproxy.io:22225"
        }
        res = requests.get(base_url, params=params, headers=headers)
        if res.status_code != 200:
            # Something went wrong
            # print("Wait Call proxies")
            # time.sleep(100)
            # print("Call proxies")
            # try:
            #     res = self.call_api(base_url, params, headers, proxies)
            # except:
            #     res = None
            #     pass
            # if not res:
            #     return {"err": "Api Error"}
            # return json.loads(res.text)
            return {}
            # raise APIError(res.status_code)
        # Display the result as HTML in Jupyter Notebook
        # display(HTML(res.text))
        # Pretty printing as json
        # print(json.dumps(json.loads(res.text), sort_keys=True, indent=4))
        return json.loads(res.text)

# import pymongo
# import pandas as pd
# client = pymongo.MongoClient(host="localhost", port=27017, username="root", password="example")
# db = client["tennis"]
# col = db["post"]
# datas = list(col.find())
# entityRecognitionLinkingObj = EntityRecognitionLinking()
# start = 83 + 68 + 19 + 122 + 697 + 557 + 423
# for idx, data in enumerate(datas[start:]):
#     print("{}/{}".format(start+idx+1, len(datas)))
#     inputText = data["title"] + " " +data["description"]
#     entityRelJson = entityRecognitionLinkingObj.entityRecogLink(inputText)
#     if "err" in entityRelJson:
#         print("Stop: ", idx)
#         break
#     entityLinkTriples = []
#     uris = []
#     for resource in entityRelJson.get("Resources", []):
#         entityLinkTriples.append(resource['@surfaceForm'])
#         uris.append(resource['@URI'])
#     df_data = pd.DataFrame({"entity": entityLinkTriples, "uri": uris})
#     if start == 0:
#         df_data.to_csv("entity_extract.csv", index=False)
#     else:
#         df_data.to_csv("entity_extract.csv", index=False, mode="a", header=None)