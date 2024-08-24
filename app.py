from flask import Flask, send_from_directory
from flask_cors import CORS
from youtube_search import YoutubeSearch
from pytubefix import YouTube
import json
from helper import *

# Titles = {}

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/search/<path:q>")
def search(q):
    data = YoutubeSearch(q, max_results=5).to_dict()

    results = []
    for video in data:
        with open("./music/title", "a", encoding="utf-8") as file:
            file.write(f"{video['id']}|{video['title']}\n")

        results.append({
            "title": video["title"],
            "thumbnail": video["thumbnails"][0],
            "id": video["id"]
        })

    return results


@app.route("/api/options/<path:id>")
def options(id):
    try:
        video = YouTube(f"https://www.youtube.com/watch?v={id}")
    except:
        return {"message": "Invalid video ID"}, 404

    streams = video.streams

    audio = streams.get_audio_only()
    data = streams.filter(adaptive=True, type="video", file_extension="mp4")

    results = []
    results.append({
        "itag": audio.itag,
        "res": "MP3",
        "size": audio.filesize_mb
    })

    for row in data:
        if row.resolution:
            results.append({
                "itag": row.itag,
                "res": row.resolution,
                "size": row.filesize_mb + audio.filesize_mb,
            })

    return results


@app.route("/api/prepare/<path:id>/<path:itag>")
def prepare(id, itag):
    try:
        stream = YouTube(f"https://www.youtube.com/watch?v={id}")
        video = stream.streams.get_by_itag(itag)
        audio = stream.streams.get_audio_only()

        titles_dict = load_title_dict()
        if id in titles_dict:
            title = escape(titles_dict[id])
        else:
            return {"message": "Invalid video ID"}, 404

        res = 0 if video.includes_audio_track else video.resolution
    except:
        return {"message": "Invalid video ID"}, 404

    filename = get_file_name(id, title, res)
    if not path.isfile(f"music/{filename}"):
        file_download(id, title, audio, video, res)

    results = {"filename": filename}

    return results


@app.route("/download/<path:id>/<path:filename>")
def download(id, filename):
    if not path.isfile(f"music/{id}/{filename}"):
        return {"message": "File not exist"}, 404
    return send_from_directory(directory=f'music/{id}', path=filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
