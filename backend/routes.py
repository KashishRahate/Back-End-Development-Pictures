from . import app
import os
import json
from flask import jsonify, request, abort, make_response

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

# Additional required imports, if any

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """Return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by ID"""
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry"""
    if not request.is_json:
        return {"message": "Request must be JSON"}, 400

    picture = request.get_json()

    # Check if ID is present and unique
    if "id" not in picture or any(p["id"] == picture["id"] for p in data):
        # If duplicate, return 302 with duplicate message
        return {"Message": f"picture with id {picture['id']} already present"}, 302

    # Add new picture to data list
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture by ID"""
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    updates = request.get_json()
    picture.update(updates)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID"""
    picture = next((p for p in data if p["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    data.remove(picture)
    # Return 204 No Content status code on successful deletion
    return "", 204
