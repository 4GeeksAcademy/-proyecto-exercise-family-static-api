"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members =jackson_family.get_all_members()
    response_body = {

        "family": members
    }
    return jsonify(response_body);200


@app.route('/member/<int:members_id>', methods=['GET'])
def get_members(members_id):
    members = jackson_family.get_member(members_id)
    if members is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def add_members():
    new_members = request.get_get_json()
    if not new_members:
        return jsonify({"error": "invalid JSON"}), 400
    
    if "first_name" not in new_members or "age" not in new_members or "luchy_numbers" not in new_members:
        return jsonify({"error": " required member fields"}), 400
    
    added_members = jackson_family.add_member(new_members)
    return jsonify(added_members), 200

@app.route('/member/<int:members_id>', methods=['DELETE'])
def delete_members(members_id):
    result = jackson_family.delete_members(members_id)
    if result:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "not found"}), 404
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
