from flask import Flask, request
import redis
import requests
import math
import json
import os
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def get_redis0():
    redis_IP0 = os.environ.get('REDIS_IP')
    if not redis_IP0:
        raise Exception()
    reedis = redis.Redis(host=redis_IP0, port=6379, db=0, decode_responses=True)
    return reedis

def get_redis1():
    redis_IP1 = os.environ.get('REDIS_IP')
    if not redis_IP1:
        raise Exception()
    reedis1 = redis.Redis(host=redis_IP1, port=6379, db=1)
    return reedis1

def get_redis2():
    redis_IP2 = os.environ.get('REDIS_IP')
    if not redis_IP2:
        raise Exception()
    reedis2 = redis.Redis(host=redis_IP2, port=6379, db=2, decode_responses=True)
    return reedis2

def get_redis_client():
      return redis.Redis(host='127.0.0.1', port=6379, db=0)

rd0 = get_redis0()
rd1 = get_redis1()
rd2 = get_redis2()

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
        for item in rd.keys:
            data_list.append(json.loads(rd.get(item)))
        return data_list
    elif request.method == 'DELETE':
        redis.flushdb()
        return f'data deleted, there are {len(rd.keys())} keys in the db\n' 
    else:
        return 'the method you tried does not work\n'

@app.route('/genes', methods=['GET'])
def DS_HGNC():
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
def DS_SpecHGNC(hgncID:str):
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

@app.route('/image', methods = ['POST','GET', 'DELETE'])
def get_image():

    try:
        len(rd.keys()) >= 1
    except Exception:
        return ("No data in the database\n")
    years = []
    counts = []
    if request.method == 'POST':
        for item in rd.keys():
            gene = json.loads(rd.get(item))
            year = gene['date_approved_reserved'][0:4]
            years.append(year)
        yeard = dict(Counter(years))
        years = list(yeard.keys())
        counts = list(yeard.values())
        plt.figure(figsize=(28,6))
        plt.bar(years, counts, width = 0.35)
        plt.xlabel("Years")
        plt.ylabel("Number of Entries Approved")
        plt.title("Genes Approved Each Year")
        plt.savefig('approvalyears.png')
        file_bytes = open('./approvalyears.png', 'rb').read()
        rd1.set('genes_approved', file_bytes)
        return ("Image created\n")
    elif request.method == 'GET':
        path = './myapprovalyears.png'
        with open(path, 'wb') as f:
            try:
                f.write(rd1.get('genes_approved'))
            except TypeError:
                return ("No image in the database\n")
            f.write(rd1.get('genes_approved'))
        return send_file(path, mimetype='image/png', as_attachment=True)
    elif request.method == 'DELETE':
        try:
            len(rd1.keys()) >= 1
        except Exception:
            return ("No image in the database to delete")
        rd1.flushdb()
        return f'Image deleted, there are {len(rd1.keys())} keys in the db\n'
    else:
        return 'The method you tried does not work\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
