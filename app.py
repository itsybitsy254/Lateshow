from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance, ma

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    ma.init_app(app)

    # Home Route
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Late Show API!"})

    # Episode Schema for Serialization
    class EpisodeSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Episode

    episode_schema = EpisodeSchema()
    episodes_schema = EpisodeSchema(many=True)

    # GET all episodes
    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        episodes = Episode.query.all()
        if not episodes:
            return jsonify({"error": "No episodes found"}), 404
        return episodes_schema.jsonify(episodes), 200

    # GET a specific episode by ID
    @app.route('/episodes/<int:id>', methods=['GET'])
    def get_episode(id):
        episode = Episode.query.get(id)
        if episode is None:
            return jsonify({"error": "Episode not found"}), 404
        return episode_schema.jsonify(episode), 200

    # DELETE a specific episode by ID
    @app.route('/episodes/<int:id>', methods=['DELETE'])
    def delete_episode(id):
        episode = Episode.query.get(id)
        if episode is None:
            return jsonify({"error": "Episode not found"}), 404
        
        db.session.delete(episode)
        db.session.commit()
        return jsonify({"message": "Episode deleted successfully!"}), 204

    # Guest Schema for Serialization
    class GuestSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Guest

    guest_schema = GuestSchema()
    guests_schema = GuestSchema(many=True)

    # GET all guests
    @app.route('/guests', methods=['GET'])
    def get_guests():
        guests = Guest.query.all()
        if not guests:
            return jsonify({"error": "No guests found"}), 404
        return guests_schema.jsonify(guests), 200

    # GET a specific guest by ID
    @app.route('/guests/<int:id>', methods=['GET'])
    def get_guest(id):
        guest = Guest.query.get(id)
        if guest is None:
            return jsonify({"error": "Guest not found"}), 404
        return guest_schema.jsonify(guest), 200

    # POST a new appearance
    @app.route('/appearances', methods=['POST'])
    def create_appearance():
        data = request.json
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Validate rating
        if rating is None or not (1 <= rating <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400

        # Validate episode and guest IDs
        episode = Episode.query.get(episode_id)
        if episode is None:
            return jsonify({"error": "Invalid episode ID"}), 404

        guest = Guest.query.get(guest_id)
        if guest is None:
            return jsonify({"error": "Invalid guest ID"}), 404

        # Create new Appearance record
        try:
            appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
            db.session.add(appearance)
            db.session.commit()
            return jsonify({"message": "Appearance created successfully!"}), 201
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
