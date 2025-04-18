from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

# Utility function to get the transcript from YouTube
def fetch_transcript(url):
    video_id = url.split('=')[1].split('&')[0]

    try:
        # Step 1: Try to fetch English transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        print("✅ English transcript found:")
    except NoTranscriptFound:
        try:
            # Step 2: If English not found, try Hindi (auto-generated)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
            print("⚠️ English not found. Fetched Hindi transcript instead:")
        except NoTranscriptFound:
            print("❌ No transcript available in English or Hindi.")
            transcript = None

    # Format the transcript
    context_transcript = ''
    if transcript:
        for line in transcript:
            context_transcript += f" {line['text']}"

    return context_transcript


@app.route('/generate-transcript', methods=['POST'])
def generate_transcript():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "Missing url"}), 400
    
    url = data['url']
    transcript = fetch_transcript(url)
    
    if not transcript:
        return jsonify({"error": "No transcript available"}), 404
    
    return jsonify({
        "transcript": transcript,
    }), 200


if __name__ == "__main__":
    app.run(debug=False)
