from flask import Flask, request
import redis
import requests
import math

app = Flask(__name__)

def get_redis_client():
      return redis.Redis(host='127.0.0.1', port=6379, db=0)

rd = get_redis_client()

@app.route('/data', methods=['POST','GET','DELETE'])
def DataSet():
    global response

    if request.method == 'POST':
        response = requests.get(url='https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            rd.set(item.get('hgnc_id'), json.dumps(item))
            return f'data loaded\n'
    elif request.method == 'GET':
        data_list = []
        for item in rd.keys:
            data_list.append(json.loads(rd.get(item)))
        return data_list
    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted, there are {len(rd.keys())} keys in the db\n' 
    else:
        return 'the method you tried does not work\n'

@app.route('/genes', methods=['GET'])
def DS_hgnc():
    try:
        rd.keys()
    except keyError:
        return("No data is posted.\n")
    
    hgncID_list = []
    for item in response.json()['response']['docs']:
        hgncID_list.append(item['hgnc_id'])
    return hgnsID_list

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
