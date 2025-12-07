import customtkinter as ctk
import threading
import yt_dlp
import os
import winsound
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

cancel_flag = False
total_file_size = 0

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def show_progress(d):
    global total_file_size
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        percent = int(downloaded * 100 / total) if total else 0
        eta = d.get('eta', '?')
        speed = d.get('speed', 0)
        speed_str = f"{round(speed / 1024 / 1024, 2)} MB/s" if speed else "?"

        progress_bar.set(percent / 100)
        total_file_size = total
        size_mb = round(total / (1024 * 1024), 2)
        progress_label.configure(text=f"{percent}% | ETA: {eta}s | Speed: {speed_str} | Total: {size_mb} MB")

    elif d['status'] == 'finished':
        progress_bar.set(1.0)
        progress_label.configure(text="Download complete! Merging...")

def do_download():
    global cancel_flag, total_file_size
    cancel_flag = False
    total_file_size = 0

    url = url_entry.get()
    resolution = res_var.get()
    folder = folder_var.get()

    if not url or not folder:
        progress_label.configure(text="Enter URL and select folder.")
        return

    output_path = os.path.join(folder, '%(title)s.%(ext)s')

    file_format = format_var.get()

    if file_format == "mp4":
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'progress_hooks': [show_progress],
            'noplaylist': True
        }
    else:  # mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'progress_hooks': [show_progress],
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

    def cancel_check():
        if cancel_flag:
            raise Exception("Download cancelled by user.")

    class CustomLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): print(msg)

    ydl_opts['logger'] = CustomLogger()
    ydl_opts['postprocessor_hooks'] = [lambda d: cancel_check()]


    try:
        download_btn.configure(state="disabled")
        cancel_btn.configure(state="normal")
        progress_label.configure(text="Starting download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        progress_label.configure(text="✅ Download finished!")
        winsound.PlaySound("SystemNotification", winsound.SND_ALIAS)
    except Exception as e:
        if str(e) == "Download cancelled by user.":
            progress_label.configure(text="❌ Download cancelled.")
        else:
            progress_label.configure(text=f"Error: {str(e)}")
    finally:
        download_btn.configure(state="normal")
        cancel_btn.configure(state="disabled")
        progress_bar.set(0)

def start_download_thread():
    threading.Thread(target=do_download).start()

def cancel_download():
    global cancel_flag
    cancel_flag = True
    progress_label.configure(text="Cancelling...")

# GUI Setup
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("500x450")

ctk.CTkLabel(app, text="YouTube URL").pack(pady=(15, 5))
url_entry = ctk.CTkEntry(app, width=400)
url_entry.pack(pady=5)

ctk.CTkLabel(app, text="Resolution").pack(pady=(10, 5))
res_var = ctk.StringVar(value="720")
res_dropdown = ctk.CTkOptionMenu(app, values=["144", "240", "360", "480", "720", "1080"], variable=res_var)
res_dropdown.pack(pady=5)
format_var = ctk.StringVar(value="mp4")

format_label = ctk.CTkLabel(app, text="Download as:")
format_label.pack(pady=(5, 0))

format_dropdown = ctk.CTkOptionMenu(app, variable=format_var, values=["mp4", "mp3"])
format_dropdown.pack(pady=(0, 10))

ctk.CTkLabel(app, text="Download Folder").pack(pady=(10, 5))
folder_frame = ctk.CTkFrame(app, fg_color="transparent")
folder_frame.pack(pady=5)

folder_var = ctk.StringVar()
folder_entry = ctk.CTkEntry(folder_frame, width=300, textvariable=folder_var)
folder_entry.pack(side="left", padx=5)
folder_btn = ctk.CTkButton(folder_frame, text="Browse", command=choose_folder, width=70)
folder_btn.pack(side="left")

progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=15)

progress_label = ctk.CTkLabel(app, text="Waiting...", text_color="yellow")
progress_label.pack(pady=5)

button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=15)

download_btn = ctk.CTkButton(button_frame, text="Download", command=start_download_thread, width=120)
download_btn.pack(side="left", padx=10)

cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=cancel_download, fg_color="red", hover_color="#990000", width=120, state="disabled")
cancel_btn.pack(side="left", padx=10)

app.mainloop()
