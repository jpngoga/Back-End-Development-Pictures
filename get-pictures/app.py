
from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory picture storage
pictures = [
    {
        "id": 1,
        "title": "Live Concert 2025",
        "url": "https://example.com/concert1.jpg",
        "description": "The band performing live on stage."
    },
    {
        "id": 2,
        "title": "Summer Music Festival",
        "url": "https://example.com/concert2.jpg",
        "description": "Fans enjoying the summer festival."
    }
]


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "get-pictures"
    }), 200


# Retrieve all pictures
@app.route("/pictures", methods=["GET"])
def get_pictures():
    return jsonify(pictures), 200


# Retrieve one picture by ID
@app.route("/pictures/<int:picture_id>", methods=["GET"])
def get_picture(picture_id):
    picture = next(
        (p for p in pictures if p["id"] == picture_id),
        None
    )

    if picture is None:
        return jsonify({"error": "Picture not found"}), 404

    return jsonify(picture), 200


# Create a new picture
@app.route("/pictures", methods=["POST"])
def create_picture():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    if not data.get("title") or not data.get("url"):
        return jsonify({
            "error": "Title and URL are required"
        }), 400

    new_picture = {
        "id": max((p["id"] for p in pictures), default=0) + 1,
        "title": data["title"],
        "url": data["url"],
        "description": data.get("description", "")
    }

    pictures.append(new_picture)

    return jsonify(new_picture), 201


# Update an existing picture
@app.route("/pictures/<int:picture_id>", methods=["PUT"])
def update_picture(picture_id):
    picture = next(
        (p for p in pictures if p["id"] == picture_id),
        None
    )

    if picture is None:
        return jsonify({"error": "Picture not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    for field in ["title", "url", "description"]:
        if field in data:
            picture[field] = data[field]

    return jsonify(picture), 200


# Delete a picture
@app.route("/pictures/<int:picture_id>", methods=["DELETE"])
def delete_picture(picture_id):
    picture = next(
        (p for p in pictures if p["id"] == picture_id),
        None
    )

    if picture is None:
        return jsonify({"error": "Picture not found"}), 404

    pictures.remove(picture)

    return jsonify({
        "message": "Picture deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
