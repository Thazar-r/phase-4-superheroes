from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict_with_powers())
    return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
        return jsonify({"errors": ["validation errors"]}), 400
    return jsonify({"error": "Power not found"}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_power = HeroPower(
        strength=data['strength'],
        power_id=data['power_id'],
        hero_id=data['hero_id']
    )
    db.session.add(hero_power)
    db.session.commit()
    return jsonify(hero_power.to_dict_with_hero_and_power()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates database tables
    app.run(debug=True)
