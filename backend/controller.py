from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from db import add_qualification_to_db, getTable, set_qualification_table
from llmCVGenerate import askForMatchingQualifications, getResponse
from cvMaker import fill_cv, convertDocToPdf

app = Flask(__name__)
CORS(app)

# endpoints: ./getQualifications ./setQualificationListToList ./createCV ./getLastCreatedCV


@app.route("/getQualifications")
def getQualifications():
    qualifications = getTable(justQualifications=True)
    return jsonify(qualifications)


@app.route("/addQualification", methods=["POST"])  # this won't be used by the frontend
def addQualifications():
    body = request.get_json()
    qualification = body["qualifications"]


    add_qualification_to_db(qualification)

    # is it better to use responseBodies rather than jsonify ? # probs doesn't matter one bit
    return Response("Qualification added", status=200)


@app.route("/setQualificationListToList", methods=["PATCH"])
def setQualificationListToList():
    body = request.get_json()
    set_qualification_table(body["qualifications"])
    return Response("Qualifications set!", status=200)


# This should get Job Position details paragraph as body Parameter
@app.route("/askForSuggestions")
def askForSuggestions():
    body = request.get_json()
    response = askForMatchingQualifications(
        getTable(include_date_info=False), body["jobDetails"]
    )
    return jsonify({"response": response})


# Should get qualities chosen and template chosen from body
@app.route("/createCVDoc", methods=["POST"])
def createCVDoc():
    body = request.get_json()
    values = body["values"]
    template = body["templateName"]
    doc = fill_cv(template_file_name=template, values=values)
    return jsonify(f"CV created to {doc}", 200)


# Should get qualities chosen and template chosen from body
@app.route("/createCV", methods=["POST"])
def createCV():
    body = request.get_json()
    values = body["values"]
    template = body["templateName"]
    doc = fill_cv(template_file_name=template, values=values)
    pdf = convertDocToPdf(doc, doc)  # probably not ok
    return jsonify(f"CV pdf created to {pdf}", 200)


@app.route("/testLLM")
def testLLM():
    body = request.get_json()
    response = getResponse(body.get("prompt", "hey gpt how are you doing?"))
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
