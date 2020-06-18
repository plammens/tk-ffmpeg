"""
Tk GUI app to replace the audio channel from a video using ffmpeg
"""

import subprocess
import tkinter as tk
from tkinter import ttk


def replace_audio(
    video_path: str, new_audio_path: str, output_path: str
) -> subprocess.CompletedProcess:
    args = (
        f"ffmpeg -i {video_path} -i {new_audio_path} "
        f"-vcodec copy -acodec copy -map 0:0 -map 1:0 {output_path}"
    )
    return subprocess.run(args, check=True)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Replace audio")

        self.main_frame = MainFrame(self).pack(side="top", fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class MainFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()

        self.video_path_entry_label = ttk.Label(text="Select video file")
        self.video_path_entry = ttk.Entry(self, textvariable=self.video_path, width=16,)
        self.audio_path_entry_label = ttk.Label(text="Select audio file")
        self.audio_path_entry = ttk.Entry(self, textvariable=self.audio_path, width=16,)

        self.configure_geometry()

    def configure_geometry(self):
        self.video_path_entry.grid(row=1, column=2, sticky=(tk.W, tk.E,))
        self.audio_path_entry.grid(row=2, column=2, sticky=(tk.W, tk.E,))

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.columnconfigure(2, weight=1)


if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
