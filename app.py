from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

# Supported formats
video_formats = ["mp4", "webm"]
audio_formats = ["mp3"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        selected_format = request.form["format"]

        try:
            # Create a YouTube object
            yt = YouTube(url)

            if selected_format in audio_formats:
                # For MP3 format, choose the best audio stream
                stream = yt.streams.filter(only_audio=True).first()
            else:
                # For video formats, filter streams by file extension
                streams = yt.streams.filter(file_extension=selected_format)

                if not streams:
                    return "No streams available in the selected format."

                # Choose the stream with the desired resolution and file format
                stream = streams.get_highest_resolution()

            # Download the video or audio
            stream.download()
            return redirect(url_for("index"))
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template("index.html", video_formats=video_formats, audio_formats=audio_formats)

if __name__ == "__main__":
    app.run(debug=True)
