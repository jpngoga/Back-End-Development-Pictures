
import os
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

db = client[MONGO_DATABASE]
songs_collection = db["songs"]


# Convert MongoDB documents into JSON-safe dictionaries
def serialize_song(song):
    return {
        "id": str(song["_id"]),
        "title": song.get("title", ""),
        "artist": song.get("artist", ""),
        "lyrics": song.get("lyrics", "")
    }


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    try:
        client.admin.command("ping")
        return jsonify({
            "service": "get-songs",
            "status": "healthy",
            "database": "connected"
        }), 200
    except PyMongoError:
        return jsonify({
            "service": "get-songs",
            "status": "unhealthy",
            "database": "disconnected"
        }), 503


# Get all songs
@app.route("/songs", methods=["GET"])
def get_songs():
    try:
        songs = songs_collection.find()
        return jsonify([serialize_song(song) for song in songs]), 200
    except PyMongoError:
        return jsonify({"error": "Unable to retrieve songs"}), 500


# Get one song by ID
@app.route("/songs/<song_id>", methods=["GET"])
def get_song(song_id):
    try:
        if not ObjectId.is_valid(song_id):
            return jsonify({"error": "Invalid song ID"}), 400

        song = songs_collection.find_one({"_id": ObjectId(song_id)})

        if song is None:
            return jsonify({"error": "Song not found"}), 404

        return jsonify(serialize_song(song)), 200

    except PyMongoError:
        return jsonify({"error": "Unable to retrieve song"}), 500


# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
