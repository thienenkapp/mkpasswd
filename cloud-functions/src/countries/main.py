#!/usr/bin/python3
import functions_framework
from google.cloud import firestore
import json

countries_a=[]
countries_r=[]

def Readcountries(sCollection):
    db = firestore.Client()

    users_ref = db.collection(u'mkpasswd-wordlists')
    docs = users_ref.stream()

    #print("Read docs:")
    for doc in docs:
        data=doc.to_dict()
        #print(data)

        if ("country" in data):
            if (data["country"] not in countries_a):
                countries_a.append(data["country"])
                countries_r.append(dict(name = data["country"]))
                #print(countries_a)


def main_get_countries(request):
    Readcountries('mkpasswd-wordlists')
    jsonString = json.dumps(countries_r) #, indent=4)
    #print(jsonString)
    return jsonString

#
# CORS was needed because local Swagger development was able to connect
# It could be solved in LoadBalancer, in Backend (StackDriver) or NEG.
# It must be done in the function itself
# https://cloud.google.com/functions/docs/samples/functions-http-cors
#

@functions_framework.http
def main(request):
    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }


    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    return (main_get_countries(request), 200, headers)
