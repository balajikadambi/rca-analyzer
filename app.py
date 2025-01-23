from flask import Flask,request,jsonify
import os
import http.client
import json
#from flask_cors import CORS


app = Flask(__name__)
#CORS(app);

#IBM Cloud credentials
ibm_cloud__iam_url="iam.cloud.ibm.com"
ibm_watsonx_url="au-syd.ml.cloud.ibm.com"
ibm_watsonx_model_generation_api="/ml/v1-beta/generation/text?version=2023-05-29"

apikey = "7JCFLUIbWzYHn2e3X6sCKplqCA0JM6pGvnMXw5q7qzHj"
project_id = "d9565d43-92d9-4c1b-bc68-7be30fde45b8"

conn_ibm_cloud_iam = http.client.HTTPSConnection(ibm_cloud__iam_url)
payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+apikey
headers = { 'Content-Type': "application/x-www-form-urlencoded" }
conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
res = conn_ibm_cloud_iam.getresponse()
data = res.read()
decoded_json=json.loads(data.decode("utf-8"))
access_token=decoded_json["access_token"]

conn_watsonx = http.client.HTTPSConnection(ibm_watsonx_url)

context="Technical Troubleshooting"

@app.route('/')
def hello():
    return "Hello World!"
    
if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
