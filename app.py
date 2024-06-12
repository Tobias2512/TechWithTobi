import os
import tempfile
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from pytube import YouTube
from io import BytesIO
import re
from python_apps.qr_encoder import generate_qr_code


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/qr_encoder')
def qr_encoder():
    return render_template('qr_encoder.html')


@app.route('/youtube_downloader')
def youtube_downloader():
    return render_template('youtube_downloader.html')


@app.route('/generate_qr_directly', methods=['POST'])
def generate_qr_directly():
    data = request.json.get('data')
    image_path = request.json.get('image_path')
    module_drawer_index: int = request.json.get('module_drawer')

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        qr = generate_qr_code(data, image_path, module_drawer_index)

        # Save the QR code to a bytes buffer
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='newQR.png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def convert_youtube_url(url):
    # Backslashes are because of . & and ? are special characters
    # ([^\?]+) gets the characters after "youtu.be" untill it hits a '?', this is so we get the video_id
    mobile_pattern = r'youtu\.be/([^\?]+)'
    pc_pattern = r'youtube\.com/watch\?v=([^\&]+)'
    # Check to see which url this is pc or mobile
    mobile_match = re.search(mobile_pattern, url)
    pc_match = re.search(pc_pattern, url)
    # if pc match the link is already in right format
    if pc_match:
        return url
    # else if mobile match the link is converted to a pc link
    elif mobile_match:
        # Because we captured the video_id, it will now be in mobile_match group(1)
        video_id = mobile_match.group(1)
        url = f"https://www.youtube.com/watch?v={video_id}"
        return url
    else:
        return None


@app.route('/download_video_directly', methods=['POST'])
def download_video_directly():
    data = request.get_json()
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    try:
        # Convert video_url if necessary
        video_url = convert_youtube_url(video_url)
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
