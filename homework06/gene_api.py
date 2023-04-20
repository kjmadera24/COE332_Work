from flask import Flask, request
import redis
import requests
import math
import json

app = Flask(__name__)

def get_redis_client():
      return redis.Redis(host='redis-db', port=6379, db=0, decode_responses=True)

rd = get_redis_client()

def getData():
    response = requests.get(url='https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
    dataset = response.json
    data = dataset()['response']['docs']
    return data

@app.route('/data', methods=['POST','GET','DELETE'])
def DataSet():
    """
    This app route has 3 different functions; a Post, Get, and Delete.
    Each function manipulates the entire data set.

    Returns:
        Post: Returns a string letting the user know that the data set
        has been uploaded to the redis server.
        Get: Returns a list of every hgnc_id and information from the
        data set.
        Delete: Returns a string letting the user know that the data
        in the redis server has been deleted and the amount of keys
        in the server to prove it.
    """
    if request.method == 'POST':
        data = getData()
        for item in data:
            key = f'{item["hgnc_id"]}'
            rd.set(item.get('hgnc_id'), json.dumps(item))
        return f'data loaded\n'
    elif request.method == 'GET':
        try: 
            rd.keys()
        except keyError:
            return("Please post data!!")
        data_list = []
        for item in rd.keys():
            data_list.append(json.loads(rd.get(item)))
        return data_list
    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted, there are {len(rd.keys())} keys in the db\n' 
    else:
        return 'the method you tried does not work\n'

@app.route('/genes', methods=['GET'])
def DS_HGNC() -> list:
    """
    This function gets the specific each key for every hgnc_id and places
    them into a list.

    Returns:
        hgncID_list (list): a list with only the hgnc_ids from the data set.
    """
    try:
        rd.keys()
    except keyError:
        return("No data is posted.\n")
    
    return rd.keys()

@app.route('/genes/<string:hgncID>', methods=['GET'])
def DS_SpecHGNC(hgncID: str) -> dict:
    """
    This function gets the specific hgnc_id the user wants and returns
    the information for that id only.

    Args:
        hgncID (str): This should be the string inoutted into the curl
        for the specific id dictionary wanted.

    Returns:
        ID_Output (dict): The dictionary for the corresponding ID
        provided from the user.
    """
    try:
        rd.keys()
    except keyError:
        return("No data is posted.\n")
    
    specHGNC = json.loads(rd.get(hgncID))
    return specHGNC

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
