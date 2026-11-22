import socket
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

from server import MediaServer


class MovieStreamerApp:
    BG = "#f3f6fb"
    INK = "#17243b"
    MUTED = "#68778f"
    BLUE = "#2563eb"

    def __init__(self, root):
        self.root = root
        self.root.title("Local Movie Streamer")
        self.root.geometry("760x700")
        self.root.minsize(620, 650)
        self.root.configure(bg=self.BG)

        self.server = MediaServer()
        self.movie_folder = tk.StringVar()
        self.address = ""
        self.server_running = False

        self._configure_styles()
        self._build_window()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def _configure_styles(self):
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        else:
            style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.INK, font=("Segoe UI", 10))
        style.configure("Heading.TLabel", font=("Segoe UI", 19, "bold"), foreground=self.INK)
        style.configure("Muted.TLabel", foreground=self.MUTED)
        style.configure("Card.TLabelframe", background="white", bordercolor="#dce4ef", relief="solid")
        style.configure("Card.TLabelframe.Label", background=self.BG, foreground=self.INK, font=("Segoe UI", 11, "bold"))
        style.configure("TEntry", padding=(10, 9), font=("Segoe UI", 10))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 10))
        style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=(13, 9))
        style.configure("Address.TLabel", font=("Segoe UI", 15, "bold"), foreground=self.BLUE)

    def _build_window(self):
        header = tk.Frame(self.root, bg="#111c33", padx=32, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="LOCAL MOVIE STREAMER", bg="#111c33", fg="#94b4ff",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(header, text="Your movies, on your Wi-Fi", bg="#111c33", fg="white",
                 font=("Segoe UI", 21, "bold")).pack(anchor="w", pady=(6, 3))
        tk.Label(header, text="Choose a folder, start the server, then open the link on another device.",
                 bg="#111c33", fg="#c0cbe0", font=("Segoe UI", 10)).pack(anchor="w")

        content = ttk.Frame(self.root, padding=(30, 18, 30, 16))
        content.pack(fill="both", expand=True)

        folder_card = ttk.LabelFrame(content, text="  1  Choose your movie folder  ", style="Card.TLabelframe", padding=15)
        folder_card.pack(fill="x", pady=(0, 16))
        ttk.Label(folder_card, text="The selected folder and its subfolders will appear in your library.",
                  style="Muted.TLabel", wraplength=650).pack(anchor="w", pady=(0, 12))
        folder_row = ttk.Frame(folder_card)
        folder_row.pack(fill="x")
        self.folder_entry = ttk.Entry(folder_row, textvariable=self.movie_folder, state="readonly")
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.browse_button = ttk.Button(folder_row, text="Browse…", style="Secondary.TButton", command=self.select_folder)
        self.browse_button.pack(side="right")

        server_card = ttk.LabelFrame(content, text="  2  Start your local server  ", style="Card.TLabelframe", padding=15)
        server_card.pack(fill="x", pady=(0, 16))
        ttk.Label(server_card, text="Original files are streamed directly. Keep this app open while watching.",
                  style="Muted.TLabel", wraplength=650).pack(anchor="w", pady=(0, 14))
        action_row = ttk.Frame(server_card)
        action_row.pack(fill="x")
        self.start_button = ttk.Button(action_row, text="Start Server", style="Primary.TButton", command=self.start_server)
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(action_row, text="Stop Server", style="Secondary.TButton", command=self.stop_server, state="disabled")
        self.stop_button.pack(side="left", padx=(10, 0))
        self.status_var = tk.StringVar(value="Server is stopped")
        self.status_label = ttk.Label(action_row, textvariable=self.status_var, style="Muted.TLabel")
        self.status_label.pack(side="right", padx=(10, 0))

        share_card = ttk.LabelFrame(content, text="  3  Open the library on your device  ", style="Card.TLabelframe", padding=15)
        share_card.pack(fill="x", pady=(0, 15))
        ttk.Label(share_card, text="Connect your device to the same Wi-Fi, then visit:",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        self.address_var = tk.StringVar(value="Start the server to get your address")
        share_row = ttk.Frame(share_card)
        share_row.pack(fill="x", pady=(0, 9))
        self.address_entry = ttk.Entry(share_row, textvariable=self.address_var, state="readonly", font=("Segoe UI", 13, "bold"))
        self.address_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.copy_button = tk.Button(
            share_row,
            text="Copy share link",
            command=self.copy_address,
            state="disabled",
            bg=self.BLUE,
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            disabledforeground="#e2e8f0",
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.copy_button.pack(side="right")
        self.open_button = ttk.Button(share_card, text="Open library on this PC", style="Secondary.TButton", command=self.open_library, state="disabled")
        self.open_button.pack(anchor="w")

        ttk.Label(content, text="Tip: Original playback depends on the receiving device supporting the movie’s video and audio formats.",
                  style="Muted.TLabel", wraplength=680).pack(anchor="w", pady=(2, 0))

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select your movie folder", mustexist=True)
        if folder:
            self.movie_folder.set(folder)

    @staticmethod
    def get_local_ip():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
        except OSError:
            return "127.0.0.1"
        finally:
            sock.close()

    def start_server(self):
        folder = self.movie_folder.get()
        if not folder:
            messagebox.showinfo("Choose a folder", "Select the folder containing your movies first.", parent=self.root)
            return
        try:
            self.server.start(folder)
        except OSError as error:
            messagebox.showerror("Could not start server", str(error), parent=self.root)
            return

        self.server_running = True
        self.address = f"http://{self.get_local_ip()}:8080"
        self.address_var.set(self.address)
        self.status_var.set("Server is running")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.browse_button.configure(state="disabled")
        self.copy_button.configure(state="normal")
        self.open_button.configure(state="normal")

    def stop_server(self):
        self.server.stop()
        self.server_running = False
        self.address = ""
        self.address_var.set("Start the server to get your address")
        self.status_var.set("Server is stopped")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.browse_button.configure(state="normal")
        self.copy_button.configure(state="disabled")
        self.open_button.configure(state="disabled")

    def copy_address(self):
        if self.address:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.address)
            self.status_var.set("Address copied to clipboard")

    def open_library(self):
        if self.address:
            webbrowser.open(self.address)

    def close_app(self):
        self.server.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    MovieStreamerApp(root)
    root.mainloop()
