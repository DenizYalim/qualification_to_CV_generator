from flask import Flask, jsonify, request
from flask_cors import CORS
from model import qualification
from db import add_qualification_to_db, get_qualifications
from llmCVGenerate import askForMatchingQualifications

app = Flask(__name__)
CORS(app)

# endpoints: ./getQualifications ./setQualificationListToList ./createCV ./getLastCreatedCV


@app.route("/getQualification")
def getQualifications():
    qualifications = get_qualifications()
    return jsonify(qualification)  # This will break


@app.route("/setQualificationListToList")
def setQualifications():
    body = request.get_json()
    add_qualification_to_db(body["qualifications"], body["essential"])

@app.route("/askForQualifications")
def askForQualifications():
    body = request.get_json()
    response = askForMatchingQualifications(get_qualifications(), body["jobDetails"])
    return jsonify({response})


# This should get Job Position details paragraph as body Parameter
@app.route("/createCV")
def createCV():
    pass


"""
# API Routes
@app.route('/api/products/<int:seller_id>')
def get_products(seller_id):
    
    return jsonify([{"id": p.id, "name": p.name} for p in products])

@app.route('/api/comments/<int:product_id>')
def get_comments(product_id):
    comments = Comment.query.filter_by(product_id=product_id).all()
    return jsonify([{
        "platform": c.platform,
        "user": c.user,
        "text": c.text,
        "rating": c.rating
    } for c in comments])
"""

if __name__ == "__main__":
    app.run(debug=True)
