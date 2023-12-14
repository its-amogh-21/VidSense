from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app=app, resources={r"/foo": {"origins": "www.youtube.com"}})

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id)
    transcript = ' '.join([part_transcript['text'] for part_transcript in transcript_list])
    return transcript

def get_summary(transcript):
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summarizer(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split("=")[1]
    summary = get_summary(get_transcript(video_id=video_id))
    print(summary)
    return summary, 200


if __name__ == '__main__':
    app.run()