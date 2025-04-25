from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!", 200

@app.route("/info")
def get_video_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        # Виконання yt-dlp для отримання метаінформації про відео
        result = subprocess.run(
            ["yt-dlp", "-j", url],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"error": "Failed to fetch video information"}), 500

        # Парсимо результат як JSON
        data = json.loads(result.stdout)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Не використовуємо app.run(), щоб Render запускало через gunicorn
    app.run(host="0.0.0.0", port=10000)
