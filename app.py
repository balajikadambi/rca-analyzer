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
    
@app.route("/watsonx_ai_service")
def queryWatsonx():
    query_arg=request.args['query']
    print("query : ",query_arg)
    try:
        str_payload=create_payload(context, query_arg)
        out_json=watsonx_generate(str_payload)

        answer=out_json["results"]
        json_output=""
        for count, ele in enumerate(answer):
            print (f"Answer {count} = {answer[count]['generated_text']}")
            json_output+=f"Answer {count} = {answer[count]['generated_text']}"
        return jsonify(json_output)
    except:
        return jsonify("An error occurred while fetching the response from watsonx.ai service!!!")

#function to genereate the paylod to invoke watson.ai service
def watsonx_generate(payload):

    headers = {
        'Authorization': "Bearer "+access_token,
        'Content-Type': "application/json",
        'Accept': "application/json"
        }

    conn_watsonx.request("POST", ibm_watsonx_model_generation_api, payload, headers)

    res = conn_watsonx.getresponse()
    data = res.read()
    decoded_json=json.loads(data.decode("utf-8"))
    return (decoded_json)

def create_payload(context, question):
    payload_json_flan_ul2 = { "model_id": "ibm/granite-3-8b-instruct",
  "input": context + "Input: " + question + "  Output:",
  "parameters": {
    "decoding_method": "greedy",
    "max_new_tokens": 200,
    "min_new_tokens": 0,
    "stop_sequences": [],
    "repetition_penalty": 1
      },
     "project_id": project_id
    }

    str_payload=json.dumps(payload_json_flan_ul2)
    return str_payload

#function to capture & return the generated results
def getTopAnswer(context, question):
    str_payload=create_payload(context, question)
    out_json=watsonx_generate(str_payload)

    return (out_json["results"][0]['generated_text'])

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
