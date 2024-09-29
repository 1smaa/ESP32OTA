from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from include.manage import *
from include.const import *
from include.gp import *

import sys

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
    
@app.create("/create",methods=["POST"])
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
        id=create_entity()
        return jsonify({
            "response":"OK",
            "entity_id":id
        })
        
@app.create("/fetchlatest",methods=["GET"])
@endpoint_wrap
def fetch_digest() -> Response:
    '''
    Checks for entity presence inside the files
    METHOD: GET
    NECESSARY DATA: 'id' 'get' standard "inline" arguments
    '''
    id=request.args.get("id")
    if id is None: raise BadRequest
    if not check(id): raise Unauthorized
    else:
        return fetch(id)
    
@app.create("/link",methods=["POST"])
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
        if check_for_keys(data,"id","digest") or not check(data["id"]): raise Unauthorized
        link=link_entity(data["id"],data["digest"])
        return jsonify({
            "response":"OK",
            "link":link
        })
    
@app.create("/update",methods=["POST"])
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
        ######## CONTINUE
        
# Simply runs the app
if __name__=="__main__":
    app.run("0.0.0.0",34,debug=True,threaded=True)