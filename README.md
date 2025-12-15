YouTube Downloader GUI
A desktop application for downloading YouTube videos and audio, built with Python, CustomTkinter, and yt-dlp.

Features
Modern GUI: Uses customtkinter for a dark-mode, modern interface.

Format Selection: download videos as MP4 or extract audio as MP3.

Resolution Control: Select video resolutions ranging from 144p to 1080p.

Directory Selection: Choose a specific output folder for downloads via a file dialog.

Real-time Statistics: Displays download progress percentage, estimated time of arrival (ETA), download speed, and total file size.

Cancellation: Ability to cancel an active download process.

Notifications: Plays a system sound notification upon completion.

Prerequisites
Operating System
Windows: This script utilizes the winsound library, which is specific to Windows. To run on macOS or Linux, the winsound line must be removed or replaced.

External Tools
FFmpeg: This is required for yt-dlp to merge video/audio streams and convert files to MP3. Ensure FFmpeg is installed and added to your system's PATH.

Python Libraries
You need to install the following dependencies:

Bash

pip install customtkinter yt-dlp
Note: threading, os, winsound, and tkinter are standard Python libraries and do not need to be installed separately.

Installation & Usage
Clone or Download the repository containing test2.py.

Install the requirements mentioned above.

Run the script:

Bash
python test2.py
How to use:

Paste a YouTube URL into the top entry field.

Select your desired Resolution (e.g., 720, 1080).

Choose the Format (MP4 for video, MP3 for audio).

Click Browse to select the destination folder.

Click Download to begin.

Technical Details
Threading: Downloads run on a separate thread to keep the GUI responsive during the download process.

Audio Post-processing: When MP3 is selected, the script uses FFmpegExtractAudio to convert the stream to MP3 at 192kbps quality.

Progress Hooks: The application uses a custom hook to calculate and update the UI with speed and size metrics.
