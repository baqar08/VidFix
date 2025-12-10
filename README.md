# VidFix
<div align="center">
  <img src="static/images/logo.svg" alt="Video Tools App Logo" width="200"/>
   


**VidFix is a versatile web application built with Flask and FFmpeg that allows users to compress, convert, trim, merge, change speed, and adjust resolution of video files.**

</div>

## Features

*   **Video Compression:**
    *   Reduce file size efficiently using **Constant Rate Factor (CRF)**.
    *   Adjustable compression levels (CRF 10-51) to balance quality and size.
*   **Audio Conversion:**
    *   Extract audio tracks from video files.
    *   Convert to popular formats: **MP3, WAV, AAC, M4A**.
*   **Video Trimming:**
    *   Cut specific segments from a video.
    *   Define precise **Start Time** and **End Time**.
*   **Video Merging:**
    *   Combine multiple video files into a single continuous video.
    *   Supports batch uploading for easy concatenation.
*   **Speed Adjustment:**
    *   Change video playback speed (e.g., 0.5x, 2.0x).
    *   **Audio Pitch Correction** ensures audio remains intelligible even at changed speeds.
*   **Resolution Changer:**
    *   Resize videos to custom dimensions (Width x Height).
    *   Essential for optimizing videos for different devices or platforms.
*   **User-Friendly Interface:**
    *   Simple, clean, and responsive web interface.
    *   Instant file processing and download generation.

## Technologies Used

*   **Backend:** Python, Flask
*   **Video Processing:** FFmpeg (via `subprocess`)
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Utilities:** UUID, Werkzeug

## Demo Video

A showcase video demonstrating the features of the Video Tools App.

🎥 [DEMO VIDEO](https://drive.google.com/file/d/1poD1TAWpRU9_zm3c3Z0zMiyjXelt7aQ-/view?usp=sharing)

## Local Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   **FFmpeg**: Must be installed and added to your system's PATH.
    *   *Mac:* `brew install ffmpeg`
    *   *Windows:* Download and add to PATH.
    *   *Linux:* `sudo apt install ffmpeg`

### 2. Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone https://github.com/baqar08/VidFix.git
cd VidFix
```

### 3. Create a Virtual Environment

It is highly recommended to create a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required Python libraries using `pip`.

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Once the setup is complete, you can start the Flask development server:

```bash
python app.py
```

Now, open your web browser and navigate to the following address:

```
http://127.0.0.1:5001/
```

You should see the **Video Tools App** running!

## How to Use

1.  Navigate to the desired tool using the navbar (Compress, Convert, Trim, Merge, etc.).
2.  **Upload** your video file(s).
3.  Configure the **settings** (e.g., select output format, set timestamps, choose resolution).
4.  Click the **Process** button (e.g., "Compress Video", "Convert").
5.  Wait for the processing to finish.
6.  Click the **Download** button to save the result to your device.

## Author

-   Name: Baqar Mustafa
-   Email: baqarmustafa84@gmail.com
-   GitHub: baqar08

