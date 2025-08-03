from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from db import add_qualification_to_db, get_qualifications, set_qualification_table
from llmCVGenerate import askForMatchingQualifications, getResponse

app = Flask(__name__)
CORS(app)

# endpoints: ./getQualifications ./setQualificationListToList ./createCV ./getLastCreatedCV


@app.route("/getQualifications")
def getQualifications():
    qualifications = get_qualifications(justQualifications=True)
    return jsonify(qualifications)


@app.route("/addQualification", methods=["POST"])  # this won't be used by the frontend
def addQualifications():
    body = request.get_json()
    qualification = body["qualifications"]

    essentiality = body.get("essential", False)

    add_qualification_to_db(qualification, essentiality)

    # is it better to use responseBodies rather than jsonify ? # probs doesn't matter one bit
    return Response("Qualification added", status=200)


@app.route("/setQualificationListToList", methods=["PATCH"])
def setQualificationListToList():
    body = request.get_json()
    set_qualification_table(body["qualifications"])
    return Response("Qualifications set!", status=200)


@app.route("/askForSuggestions")
def askForSuggestions():
    body = request.get_json()
    response = askForMatchingQualifications(
        get_qualifications(include_date_info=False), body["jobDetails"]
    )
    return jsonify({"response": response})


# This should get Job Position details paragraph as body Parameter
@app.route("/createCV")
def createCV():
    pass


@app.route("/testLLM")
def testLLM():
    body = request.get_json()
    response = getResponse(body.get("prompt", "hey gpt how are you doing?"))
    return jsonify({"response": response})


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
