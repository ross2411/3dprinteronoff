import os
from flask import Flask, render_template, abort, url_for, json, jsonify
import json
import meross_client
import asyncio

app = Flask(__name__,template_folder='.')

# read file
with open('file.json', 'r') as myfile:
    data = myfile.read()
@app.route("/")
def index():
    return render_template('Index.html', title="page", jsonfile=json.dumps(data))

@app.route("/on-off")
async def onOff():
    await meross_client.onOff()
    return render_template('OnOff.html')
    
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')