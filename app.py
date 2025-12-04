import os
import uuid
import subprocess
from pathlib import Path
from flask import (
    Flask, render_template, request, redirect, url_for,
    send_from_directory, flash, abort
)
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
PROCESSED_DIR = BASE_DIR / "processed"
ALLOWED_EXT = {"mp4", "mov", "mkv", "avi", "webm", "flv"}

for p in (UPLOAD_DIR, PROCESSED_DIR):
    p.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["UPLOAD_DIR"] = str(UPLOAD_DIR)
app.config["PROCESSED_DIR"] = str(PROCESSED_DIR)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1GB
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def unique_filename(filename: str) -> str:
    name = secure_filename(filename)
    uid = uuid.uuid4().hex[:10]
    return f"{uid}_{name}"

def run_ffmpeg(cmd: list):
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return proc.stdout, proc.stderr
    except subprocess.CalledProcessError as e:
        stderr = e.stderr or e.stdout or str(e)
        raise RuntimeError(stderr.strip())

def save_upload(file_storage) -> str:
    filename = unique_filename(file_storage.filename)
    path = Path(app.config["UPLOAD_DIR"]) / filename
    file_storage.save(str(path))
    return str(path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "GET":
        return render_template("compress.html")
    file = request.files.get("video")
    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    crf = request.form.get("crf", "28")
    try:
        crf_val = int(crf)
        if not (10 <= crf_val <= 51):
            raise ValueError()
    except ValueError:
        flash("CRF must be an integer between 10 and 51.")
        return redirect(request.url)

    in_path = save_upload(file)
    out_name = f"{uuid.uuid4().hex[:8]}_compressed.mp4"
    out_path = Path(app.config["PROCESSED_DIR"]) / out_name

    cmd = ["ffmpeg", "-y", "-i", in_path, "-vcodec", "libx264", "-crf", str(crf_val), "-preset", "medium", str(out_path)]
    try:
        run_ffmpeg(cmd)
    except RuntimeError as e:
        flash(f"Compression failed: {e}")
        return redirect(request.url)

    return redirect(url_for("download_file", filename=out_name))

@app.route("/convert", methods=["GET", "POST"])
def convert():
    if request.method == "GET":
        return render_template("convert.html")
    file = request.files.get("video")
    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    audio_format = request.form.get("format", "mp3").lower()
    codec_map = {"mp3":"libmp3lame", "wav":"pcm_s16le", "aac":"aac", "m4a":"aac"}
    if audio_format not in codec_map:
        flash("Unsupported audio format.")
        return redirect(request.url)

    in_path = save_upload(file)
    out_name = f"{uuid.uuid4().hex[:8]}.{audio_format}"
    out_path = Path(app.config["PROCESSED_DIR"]) / out_name

    cmd = ["ffmpeg", "-y", "-i", in_path, "-vn", "-acodec", codec_map[audio_format], str(out_path)]
    try:
        run_ffmpeg(cmd)
    except RuntimeError as e:
        flash(f"Conversion failed: {e}")
        return redirect(request.url)

    return redirect(url_for("download_file", filename=out_name))

@app.route("/trim", methods=["GET", "POST"])
def trim():
    if request.method == "GET":
        return render_template("trim.html")
    file = request.files.get("video")
    start = request.form.get("start", "0").strip()
    end = request.form.get("end", "").strip()
    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    in_path = save_upload(file)
    out_name = f"{uuid.uuid4().hex[:8]}_trim.mp4"
    out_path = Path(app.config["PROCESSED_DIR"]) / out_name

    cmd = ["ffmpeg", "-y", "-i", in_path, "-ss", start]
    if end:
        cmd += ["-to", end]
    cmd += ["-c", "copy", str(out_path)]

    try:
        run_ffmpeg(cmd)
    except RuntimeError as e:
        flash(f"Trim failed: {e}")
        return redirect(request.url)

    return redirect(url_for("download_file", filename=out_name))

@app.route("/merge", methods=["GET", "POST"])
def merge():
    if request.method == "GET":
        return render_template("merge.html")
    files = request.files.getlist("videos")
    if not files or len(files) == 0:
        flash("No files selected.")
        return redirect(request.url)

    saved = []
    uid = uuid.uuid4().hex[:8]
    for f in files:
        if f and f.filename and allowed_file(f.filename):
            saved.append(save_upload(f))

    if not saved:
        flash("No valid files uploaded.")
        return redirect(request.url)

    list_file = Path(app.config["UPLOAD_DIR"]) / f"{uid}_list.txt"
    with list_file.open("w", encoding="utf-8") as fh:
        for p in saved:
            fh.write(f"file '{p}'\n")

    out_name = f"{uid}_merged.mp4"
    out_path = Path(app.config["PROCESSED_DIR"]) / out_name
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(out_path)]
    try:
        run_ffmpeg(cmd)
    except RuntimeError as e:
        flash(f"Merge failed: {e}")
        return redirect(request.url)
    finally:
        try:
            list_file.unlink()
        except Exception:
            pass

    return redirect(url_for("download_file", filename=out_name))

@app.route("/speed", methods=["GET", "POST"])
def speed():
    if request.method == "GET":
        return render_template("speed.html")
    file = request.files.get("video")
    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    try:
        factor = float(request.form.get("factor", "1.0"))
        if factor <= 0:
            raise ValueError()
    except ValueError:
        flash("Speed factor must be a positive number.")
        return redirect(request.url)

    in_path = save_upload(file)
    out_name = f"{uuid.uuid4().hex[:8]}_speed_{str(factor).replace('.', '_')}.mp4"
    out_path = Path(app.config["PROCESSED_DIR"]) / out_name

    v_filter = f"setpts={1.0/factor}*PTS"
    audio_filters = []
    audio_factor = 1.0 / factor
    if 0.5 <= audio_factor <= 2.0:
        audio_filters = [f"atempo={audio_factor}"]
    else:
        remain = audio_factor
        chain = []
        while remain > 2.0:
            chain.append("2.0")
            remain /= 2.0
        while remain < 0.5:
            chain.append("0.5")
            remain /= 0.5
        chain.append(str(round(remain, 3)))
        audio_filters = [",".join([f"atempo={c}" for c in chain])]

    cmd = ["ffmpeg", "-y", "-i", in_path, "-filter:v", v_filter]
    if audio_filters:
        cmd += ["-filter:a", ",".join(audio_filters)]
    cmd += [str(out_path)]

    try:
        run_ffmpeg(cmd)
    except RuntimeError as e:
        flash(f"Speed change failed: {e}")
        return redirect(request.url)

    return redirect(url_for("download_file", filename=out_name))

@app.route("/resolution", methods=["GET", "POST"])
def resolution():
    if request.method == "GET":
        return render_template("resolution.html")
    file = request.files.get("video")
    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    res = request.form.get("resolution", "1280x720").strip()
    if "x" not in res:
        flash("Resolution must be in WIDTHxHEIGHT format.")
        return redirect(request.url)
    w,h = res.split("x",1)
    if not (w.isdigit() and h.isdigit()):
        flash("Width and height must be numbers.")
        return redirect(request.url)

    in_path = save_upload(file)
    out_name = f"{uuid.uuid4().hex[:8]}_{w}x{h}.mp4"
    out_path = Path(app.config["PROCESSED_DIR"]) / out_name

    cmd = ["ffmpeg", "-y", "-i", in_path, "-vf", f"scale={w}:{h}", str(out_path)]
    try:
        run_ffmpeg(cmd)
    except RuntimeError as e:
        flash(f"Resolution change failed: {e}")
        return redirect(request.url)

    return redirect(url_for("download_file", filename=out_name))

@app.route("/processed/<path:filename>")
def download_file(filename):
    p = Path(app.config["PROCESSED_DIR"]) / filename
    try:
        p.resolve().relative_to(Path(app.config["PROCESSED_DIR"]).resolve())
    except Exception:
        abort(404)
    if not p.exists():
        abort(404)
    return send_from_directory(app.config["PROCESSED_DIR"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
