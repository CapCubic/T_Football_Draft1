from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
app = Flask(__name__)

# Secure JWT authentication
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Enable CORS for trusted frontend sources
CORS(app, origins=["https://your-trusted-frontend.com"])

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST")
    )

@app.route("/players", methods=["GET"])
@jwt_required()  # Requires authentication token
def get_players():
    """ Fetch player stats securely using parameterized queries """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, position, goals_scored FROM players;")
    players = cur.fetchall()
    conn.close()
    return jsonify([{"name": p[0], "position": p[1], "goals_scored": p[2]} for p in players])

@app.route("/login", methods=["POST"])
def login():
    """ Generates a JWT token for authentication """
    token = create_access_token(identity="authorized_user")
    return jsonify({"token": token})

if __name__ == "__main__":
    app.run(debug=True)
