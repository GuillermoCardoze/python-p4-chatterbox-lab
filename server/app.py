from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        return make_response(jsonify(messages), 200)
    elif request.method == "POST":
        data = request.get_json()
        new_message = Message (
            body = data.get("body"),
            username = data.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(jsonify(new_message.to_dict()), 200)
    else:
        return make_response({"message": "message not found."})
    


        
    

@app.route('/messages/<int:id>', methods = ["PATCH", "DELETE"])
def messages_by_id(id):
    messages_id = Message.query.filter_by(id=id).first()
    if request.method == "PATCH":
        data = request.get_json()
        messages_id.body = data.get("body", messages_id.body)
        db.session.commit()

        return make_response((messages_id).to_dict(), 200)
    


    if request.method == "DELETE":
        db.session.delete(messages_id)
        db.session.commit()
        return ({},204)
   

if __name__ == '__main__':
    app.run(port=5555)
