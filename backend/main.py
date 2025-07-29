from flask import Flask, jsonify
from flask_cors import CORS
from model import qualification
from db import add_qualification_to_db, get_qualifications

app = Flask(__name__)
CORS(app)

# endpoints: ./getQualifications ./setQualificationListToList ./createCV ./getLastCreatedCV 

@app.route('/getQualification')
def getQualifications():
    qualifications = get_qualifications()
    return jsonify(qualification)  # This will break


@app.route('/setQualificationListToList')
def setQualifications():
    pass

# This should get Job Position details paragraph as body Parameter
@app.route('/createCV')
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates data.db on first run
    app.run(debug=True)
"""