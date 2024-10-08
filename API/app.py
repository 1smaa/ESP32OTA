from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from include.manage import *
from include.const import *
from include.gp import *

import sqlite3

#
#   MAIN FILE
#

app=Flask(__name__)
CORS(app)

@app.route("/test",methods=["GET"])
@endpoint_wrap
def test() -> Response:
    '''
    Test endpoint to verify if the API is running correctly.
    '''
    return jsonify({
        "status":"running"
    })
    
@app.route("/create",methods=["POST"])
@endpoint_wrap
def register_entity() -> Response:
    '''
    Registers a new entity inside the files
    METHOD: POST
    NECESSARY DATA: Json with a 'key' key
    '''
    if not request.is_json:
        raise BadRequest
    else:
        data=request.get_json()
        if ("key" not in data.keys() or data["key"]!=KEY): raise Unauthorized
        id=Storage.create_entity()
        return jsonify({
            "response":"OK",
            "entity_id":id
        })
        
@app.route("/fetchlatest",methods=["GET"])
@endpoint_wrap
def fetch_digest() -> Response:
    '''
    Checks for entity presence inside the files
    METHOD: GET
    NECESSARY DATA: 'id' 'get' standard "inline" arguments
    '''
    id=request.args.get("id")
    if id is None: raise BadRequest
    if not Storage.check(id): raise Unauthorized
    else:
        return Storage.fetch(id)
    
@app.route("/link",methods=["POST"])
@endpoint_wrap
def link() -> Response:
    '''
    Returns the link from which to download the update
    METHOD: POST
    NECESSARY DATA: 'id' and 'digest' of the download
    '''
    if not request.is_json: raise BadRequest
    else:
        data=request.get_json()
        if check_for_keys(data,"id","timestamp") or not Storage.check(data["id"]): raise Unauthorized
        link=Storage.link_entity(data["id"],data["timestamp"])
        return jsonify({
            "response":"OK",
            "link":link
        })
        
@app.route("/timestamps",methods=["GET"])
@endpoint_wrap
def timestamps() -> Response:
    '''
    Returns the list of available updates timestamps
    METHOD: GET
    NECESSARY DATA: 'id' and 'last', a boolean value to specify if only the latest timestamp is needed
    '''
    id=request.args.get("id")
    last=request.args.get("last")
    if not id or not Storage.check(id): raise Unauthorized
    timestamps=Storage.get_timestamps()
    if len(timestamps):
        if last:
            return jsonify({
                "response":"OK",
                "timestamp":max(timestamps)
            })
        else:
            return jsonify({
                "response":"OK",
                "timestamps":timestamps
            })
    else:
        return jsonify({
            "response":"Empty",
            "timestamps":[]
        })
        
    
    
@app.route("/update",methods=["POST"])
@endpoint_wrap
def update() -> Response:
    '''
    Uploads a new update to the files
    METHOD: POST
    NECESSARY DATA: 'id','digest','timestamp','link'
    '''
    if not request.is_json: raise BadRequest
    else:
        data=request.get_json()
        if not check_for_keys(data,"id","digest","timestamp","link"): raise Unauthorized
        if Storage.create(data):
            return jsonify({
                "response":"OK"
            })
        else: raise Exception
        
        
# Simply runs the app
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=False,threaded=True)