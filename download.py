# ==================== YOUR YOUTUBE LINKS (EDIT HERE) ====================
youtube_links = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]

# ==================== DOWNLOAD SETTINGS (EDIT IF NEEDED) ====================
download_folder = r"."  # Change to your preferred folder

audio_only = False

max_height = None  # Set to 720, 1080, etc. if you want to limit quality (no ffmpeg needed)


# ==================== NO NEED TO EDIT BELOW THIS LINE ====================
import yt_dlp
import os

# Define progress_hook OUTSIDE so it's accessible
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        eta = d.get('_eta_str', 'N/A').strip()
        filename = os.path.basename(d.get('filename', 'Unknown'))
        print(f"[{filename}] {percent} at {speed} (ETA: {eta})", end='\r')
    elif d['status'] == 'finished':
        filename = os.path.basename(d.get('filename', 'Unknown'))
        print(f"\nDone: {filename}")

def download_videos(url_list, output_path='.'):
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],  # Now this works!
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        if max_height:
            ydl_opts['format'] = f'best[height<={max_height}]/best'
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in url_list:
            if not url.strip():
                continue
            print(f"\nStarting: {url}")
            try:
                ydl.download([url])
            except Exception as e:
                print(f"\nFailed to download {url}: {e}")

if __name__ == "__main__":
    if not youtube_links:
        print("No links provided. Please add URLs to the 'youtube_links' list at the top.")
    else:
        download_videos(youtube_links, output_path=download_folder)
        print("\nAll downloads completed!")
