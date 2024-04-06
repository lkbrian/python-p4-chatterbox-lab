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

@app.route('/messages',methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        return make_response(messages,200)
    
    elif request.method == 'POST':
        new_message = Message(
            body=request.form.get("body"),
            username = request.form.get('username')            
        )
        db.session.add(new_message)
        db.session.commit()
        message = new_message.to_dict()
        return make_response(message,201)

@app.route('/messages/<int:id>',methods=['GET','PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        response= message.to_dict()
        return make_response(response,200)
    if request.method == 'PATCH':
        for attr in request.form:
            setattr(message,attr,request.form.get(attr))
        db.session.add(message)
        db.session.commit()
        updated_message = message.to_dict()
        return make_response(updated_message,200)
    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = {' succesfull': True,'message':'Message deleted succesfully'}
        return make_response(response,200)




if __name__ == '__main__':
    app.run(port=4000)
