"""
Tk GUI app to replace the audio channel from a video using ffmpeg
"""

import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable


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

        self.main_frame = MainFrame(self, padding=(5, 10, 5, 10))
        self.configure_geometry()

    def configure_geometry(self):
        self.main_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class MainFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.video_path = PathStringVar()
        self.audio_path = PathStringVar()

        path_entry_width = 32
        self.video_path_entry_label = ttk.Label(self, text="Select video file")
        self.video_path_entry = ttk.Entry(
            self, textvariable=self.video_path, width=path_entry_width,
        )
        self.video_path_entry_browse = ttk.Button(
            self,
            text="Browse",
            command=self.video_path.make_update_command(filedialog.askopenfilename),
        )
        self.audio_path_entry_label = ttk.Label(self, text="Select audio file")
        self.audio_path_entry = ttk.Entry(
            self, textvariable=self.audio_path, width=path_entry_width,
        )
        self.audio_path_entry_browse = ttk.Button(
            self,
            text="Browse",
            command=self.audio_path.make_update_command(filedialog.askopenfilename),
        )

        self.configure_geometry()

    def configure_geometry(self):
        # row 1
        self.video_path_entry_label.grid(row=1, column=1)
        self.video_path_entry.grid(row=1, column=2, sticky=(tk.W, tk.E,))
        self.video_path_entry_browse.grid(row=1, column=3, sticky=(tk.W,))

        # row 2
        self.audio_path_entry_label.grid(row=2, column=1)
        self.audio_path_entry.grid(row=2, column=2, sticky=(tk.W, tk.E,))
        self.audio_path_entry_browse.grid(row=2, column=3, sticky=(tk.W,))

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.columnconfigure(2, weight=1)


class PathStringVar(tk.StringVar):
    def make_update_command(self, callback: Callable[[], str]) -> Callable[[], None]:
        def command():
            self.set(callback())

        return command


if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
