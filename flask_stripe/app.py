from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import environ
from flask_cors import CORS
import os
import stripe

stripe.api_key = environ.get('STRIPE_SECRET')
endpoint_secret = 'whsec_jq57EvUi7OeG4I3Tz6oPkklm6sl3yjFy'

# Init app
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.username
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username','email','amount')

user_schema = UserSchema(many=True)

@app.route('/',methods=['GET'])
def test():
    return 'welcome to flask server'

@app.route('/api/user',methods=['GET'])
def get_users():
    users = User.query.all()
    result = user_schema.dump(users)
    return jsonify(result)

@app.route('/api/user',methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    amount = 0
 
    new_user = User(username=username,email=email,amount=amount)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/api/user/<id>',methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.amount = request.json['amount']
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/api/create-payment-intent',methods=['POST'])
def payment():
    try:
        email = request.json['email']
        amount = int(request.json['amount'])
        
        intent = stripe.PaymentIntent.create(
            amount = amount*100,
            currency='usd',
            receipt_email=email
        )

        return jsonify({
                'clientSecret': intent['client_secret']
            })
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 403


@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        amount = int(payment_intent.amount)/100
        client_secret = payment_intent.client_secret
        email = payment_intent.receipt_email

        user = User.query.filter_by(email= email).first()
        user.amount = amount
        db.session.commit()

        print(f'user {email} has paid {amount} with client {client_secret}')

    # ... handle other event types or update database.
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

# Run server
if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)