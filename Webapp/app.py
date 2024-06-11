import os
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
from io import BytesIO

from python_apps.qr_encoder import generate_qr_code


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Welcome :)"


@app.route('/generate_qr_directly', methods=['POST'])
def generate_qr_directly():
    data = request.json.get('data')
    image_path = request.json.get('image_path')

    if not data or not image_path:
        return jsonify({'error': "Both 'data' and 'image_path' are required."}), 400

    try:
        qr = generate_qr_code(data, image_path)

        # Save the QR code to a bytes buffer
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='newQR.png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download_video_directly', methods=['POST'])
def download_video_directly():
    data = request.get_json()
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    try:
        # Download the video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_path = temp_file.name
            video = YouTube(video_url)
            stream = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            stream.download(output_path=os.path.dirname(temp_path), filename=os.path.basename(temp_path))

            # Return the temporary file to the client
            return send_file(temp_path, as_attachment=True, download_name='YouTubeVideo.mp4', mimetype='video/mp4')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
