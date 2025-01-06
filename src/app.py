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



jackson_family.add_member({
    'name':'John',
    'age': 55,
    'lucky_numbers': [1,2,3]
})

jackson_family.add_member(
{
    'name':'Jane',
    'age':35,
    'lucky_number':[10, 14, 3]
})

jackson_family.add_member({
    'name':'Jimmy',
    'age':5,
    'lucky_number':[1]

})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
   
    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200

@app.route('/members', methods =['POST'])
def add_member():
    data = request.json
    print("added", data)
    jackson_family.add_member(data)
    if data is not None:
        return "member created", 200
    
@app.route('/member/<int:id>', methods = ['DELETE'])
def delete_single_member(id):
    member = jackson_family.get_member(id)

    if member: 
        jackson_family.delete_member(id)
        return jsonify({"message": f"Member deleted succesfully : {member} "}), 200
   
    else: 
        return jsonify({"error" : "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
