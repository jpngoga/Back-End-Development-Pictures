
import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where()
)

db = client[os.getenv("MONGO_DATABASE")]
songs_collection = db["songs"]

sample_songs = [
    {
        "title": "African Sunrise",
        "artist": "The Music Band",
        "lyrics": "The morning sun is rising high,\nA golden light across the sky.\nTogether we will find our way."
    },
    {
        "title": "Rhythm of Life",
        "artist": "The Music Band",
        "lyrics": "Feel the rhythm, feel the sound,\nLet the music bring us round.\nEvery heartbeat joins the song."
    },
    {
        "title": "Never Give Up",
        "artist": "The Music Band",
        "lyrics": "When the road is long and wide,\nKeep your dreams and hope inside.\nTomorrow brings another day."
    }
]

try:
    if songs_collection.count_documents({}) == 0:
        result = songs_collection.insert_many(sample_songs)
        print("Successfully inserted", len(result.inserted_ids), "songs!")
    else:
        print("Songs already exist. No duplicates inserted.")

    print("Total songs:", songs_collection.count_documents({}))

finally:
    client.close()
