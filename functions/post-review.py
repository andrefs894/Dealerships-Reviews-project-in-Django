from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request
import atexit
import json

cloudant_username = 'b69568f1-7faa-40da-a28a-905167584d3d-bluemix'
cloudant_api_key = 'uFeWPUC_w6Qg79y295QN_8TS6Pd8WBAoj9QvIFbSPFBC'
cloudant_url = 'https://b69568f1-7faa-40da-a28a-905167584d3d-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()

db = client['reviews']

app = Flask(__name__)

@app.route('/reviews/post', methods=['POST'])
def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')
    
    # extract review data from json
    review_data = request.json

    # validate required fields
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    # validate review data as dictionary
    if not isinstance(review_data, dict):
        review_data = json.loads(review_data)
        if not isinstance(review_data, dict):
            abort(400, description='Invalid JSON data')

    # save review data in db
    new_document = db.create_document(review_data)
    if new_document.exists():
        return jsonify({'message': 'Data saved successfully'})
    else:
        return jsonify({'message': 'Failed to save data'})

if __name__ == '__main__':
    app.run(debug=True)