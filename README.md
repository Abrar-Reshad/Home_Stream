# Local Movie Streamer

A small Windows desktop app for browsing and playing movies stored on your PC from another device on the same Wi-Fi network.

## Features

- Choose a movie folder from the desktop app.
- Start and stop a local web server with one click.
- Browse and search the library in a responsive web page.
- Stream the original movie file with HTTP range support for seeking.
- No FFmpeg installation or video conversion required.

## Use the Windows app

Download `LocalMovieStreamer.exe` from the project’s GitHub Releases page and double-click it. No Python or FFmpeg installation is needed. Select a movie folder, start the server, then use the displayed link on another device connected to the same Wi-Fi.

Windows may show a SmartScreen warning because the app is not code-signed. Only run the executable you downloaded from a release you trust.

## Requirements to run from source

- Windows 10 or 11
- Python 3.10 or newer
- A web browser on the PC and the viewing device

## Run from source

1. Download or clone this project.
2. Open a terminal in the project folder.
3. (Optional) Create and activate a virtual environment.
4. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the desktop app:

   ```powershell
   python main.py
   ```

6. Choose the folder containing your movies and click **Start Server**.
7. Connect the viewing device to the same Wi-Fi and open the address shown in the desktop app.

If Windows Firewall asks, allow Python on **Private networks** so devices on your home Wi-Fi can connect.

## Build the single-file Windows executable

On Windows, with Python installed, run this from PowerShell in the project folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build_windows.ps1
```

The build script installs the build dependencies and creates `dist\LocalMovieStreamer.exe`. Upload that executable as an asset on a GitHub Release so users can download it without installing Python. The build is Windows-specific; create it on Windows for best results.

## Playback notes

Movies are sent in their original format. The receiving browser and device must support the movie’s video and audio codecs. If a file does not play in the browser, try a browser or device that supports its format, or convert a copy to MP4 with H.264 video and AAC audio.

The server listens on port `8080`. Keep the desktop app running while watching. This project is designed for a trusted local network; it does not include accounts, passwords, or encryption. Do not expose the server directly to the public internet.

## Supported file extensions

`.mp4`, `.m4v`, `.webm`, `.mov`, `.mkv`, and `.avi`
