from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False

# Init DB
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Products Class/Model
class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20),unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', foreign_keys=[category_id], backref='products')

    def __init__(self,name,description,category_id,price,qty):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.price = price
        self.qty = qty
    

class Category(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20),unique = True)
    code = db.Column(db.Integer,unique = True)
    
# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty', 'category_id', 'category')
    category = ma.Nested('CategorySchema', many=False)

# Product Schema
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id','name','code')

# Init schema
product_schema = ProductSchema()
category_schema = CategorySchema()
products_schema = ProductSchema(many=True)
categorys_schema = CategorySchema(many=True)

# Create a Product
@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    category_id = request.json['category_id']
    category = Category.query.get(category_id)
    if(category):
        new_product = Product(name=name,description=description,category_id=category_id,price=price,qty=qty)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product)
    return {"result":"category not found"}

# Create a Cateogry
@app.route('/category',methods=['POST'])
def add_category():
    name = request.json['name']
    code = request.json['code']
    category = Category(name=name,code=code)
    db.session.add(category)
    db.session.commit()
    return category_schema.jsonify(category)

# Get all products
@app.route('/product',methods=['GET'])
def get_products():
    products = Product.query.all()
    result = products_schema.dump(products)
    return jsonify(result)
    # return products_schema.jsonify(products)

# Get all categorys
@app.route('/category',methods=['GET'])
def get_categorys():
    categorys = Category.query.all()
    result = categorys_schema.dump(categorys)
    return jsonify(result)

# Get Single Product
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Get Single category
@app.route('/category/<id>',methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    return category_schema.jsonify(category)

# Update a product
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']
    db.session.commit()
    return product_schema.jsonify(product)

# Get Single Product
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


# Run server
if __name__ == '__main__':
    app.run(debug=True)