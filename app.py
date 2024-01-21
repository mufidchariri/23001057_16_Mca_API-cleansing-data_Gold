import pandas as pd 
import re

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

class CustomFlaskAppwithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppwithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: "API For Cleansing Data, By Mufid"),
        'version' : LazyString(lambda: "1.0.0"),
        'description' : LazyString(lambda: "API untuk Cleansing Data, oleh Mufid"),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static", # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs./"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)

@swag_from("docs/text_processing_file.yml", methods = ['POST'])
@app.route('/text-processing-file',methods = ['POST'])
def text_processing_file():

    file = request.files.getlist('file')[0]

    df = pd.read_csv(file, encoding="ISO-8859-1")

    text = df.Tweet.to_list()
    
    cleaned_text = []
    for text in text:
        cleaned_text.append(re.sub(r'[^a-zA-Z0-9]', '', text))

    json_response = {
        'status_code' : 200,
        'description' : "Text yang telah diproses",
        'data' : cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing.yml",methods =['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    text_clean = re.sub(r'[^a-zA-Z0-9]', '', text)

    #conn = sqlite3.connect('data/binar_data_science.db')
    #print("Opened Database Succesfully")
    #conn.execute(f"INSERT INTO users (raw_text, result_text) VALUES ({text}, {text_clean})")
    #conn.commit()
    #print("Records Has Been Created")
    #conn.close()

    json_response = {
        'status_code': 200,
        'description': "Text yang sudah diproses",
        'data_raw': text,
        'data_clean': text_clean
    }
    return json_response

if __name__== '__main__':
    app.run()