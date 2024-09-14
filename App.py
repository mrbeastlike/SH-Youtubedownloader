from flask import Flask, render_template, request, redirect, url_for
import os
import yt_dlp

app = Flask(__name__)
app.config["DOWNLOAD_FOLDER"] = "./downloads"

# Crear la carpeta de descargas si no existe
if not os.path.exists(app.config["DOWNLOAD_FOLDER"]):
    os.makedirs(app.config["DOWNLOAD_FOLDER"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    if not video_url:
        return "No URL provided", 400

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Descargar el mejor video con audio
            'merge_output_format': 'mp4',  # Combinar ambos en MP4
            'outtmpl': os.path.join(app.config["DOWNLOAD_FOLDER"], '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = ydl.prepare_filename(info_dict)

        return redirect(url_for('download_complete', filename=os.path.basename(video_title)))

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/download_complete/<filename>')
def download_complete(filename):
    return f"Descarga completada: {filename}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
