"""
Tk GUI app to replace the audio channel from a video using ffmpeg
"""
import functools
import os
import subprocess
import tkinter as tk
import traceback
from tkinter import ttk, filedialog, messagebox
from typing import Callable

from utils import is_pathname_valid


def replace_audio(
    video_path: str, new_audio_path: str, output_path: str
) -> subprocess.CompletedProcess:
    for arg in video_path, new_audio_path, output_path:
        if not is_pathname_valid(arg):
            raise ValueError(f"Invalid path: {arg}")
    if not os.path.isfile(video_path):
        raise ValueError(f"Nonexistent video file path: {video_path}")
    if not os.path.isfile(new_audio_path):
        raise ValueError(f"Nonexistent audio file path: {new_audio_path}")

    args = (
        f"ffmpeg -i {video_path} -i {new_audio_path} "
        f"-vcodec copy -acodec copy -map 0:0 -map 1:0 {output_path} -y"
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
        self.output_path = PathStringVar()

        path_entry_width = 32

        # video path
        self.video_path_entry_label = ttk.Label(self, text="Select video file")
        self.video_path_entry = ttk.Entry(
            self, textvariable=self.video_path, width=path_entry_width,
        )
        self.video_path_entry_browse = ttk.Button(
            self,
            text="Browse",
            command=self.video_path.make_update_command(filedialog.askopenfilename),
        )

        # audio path
        self.audio_path_entry_label = ttk.Label(self, text="Select audio file")
        self.audio_path_entry = ttk.Entry(
            self, textvariable=self.audio_path, width=path_entry_width,
        )
        self.audio_path_entry_browse = ttk.Button(
            self,
            text="Browse",
            command=self.audio_path.make_update_command(filedialog.askopenfilename),
        )

        # output path
        self.output_path_entry_label = ttk.Label(
            self, text="Select output video file location"
        )
        self.output_path_entry = ttk.Entry(
            self, textvariable=self.output_path, width=path_entry_width,
        )
        self.output_path_entry_browse = ttk.Button(
            self,
            text="Browse",
            command=self.output_path.make_update_command(
                functools.partial(
                    filedialog.asksaveasfilename,
                    defaultextension=".mp4",
                    filetypes=("video .mp4",),
                )
            ),
        )

        # run button
        self.run_button = ttk.Button(self, text="Run", command=self.run_command)

        self.configure_geometry()

    def configure_geometry(self):
        # row 1
        self.video_path_entry_label.grid(row=1, column=1, sticky=(tk.E,))
        self.video_path_entry.grid(row=1, column=2, sticky=(tk.W, tk.E,))
        self.video_path_entry_browse.grid(row=1, column=3, sticky=(tk.W,))

        # row 2
        self.audio_path_entry_label.grid(row=2, column=1, sticky=(tk.E,))
        self.audio_path_entry.grid(row=2, column=2, sticky=(tk.W, tk.E,))
        self.audio_path_entry_browse.grid(row=2, column=3, sticky=(tk.W,))

        # row 3
        self.output_path_entry_label.grid(row=3, column=1, sticky=(tk.E,))
        self.output_path_entry.grid(row=3, column=2, sticky=(tk.W, tk.E,))
        self.output_path_entry_browse.grid(row=3, column=3, sticky=(tk.W,))

        # row 4
        self.run_button.grid(row=4, column=3, sticky=(tk.E,), pady=10)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.columnconfigure(2, weight=1)

    def run_command(self):
        try:
            output_path = self.output_path.get()
            replace_audio(self.video_path.get(), self.audio_path.get(), output_path)
            os.system(f'explorer "{os.path.dirname(output_path)}"')
        except Exception as exc:
            messagebox.showerror(
                "Error", message=traceback.format_exception_only(type(exc), exc)[0]
            )
        else:
            messagebox.showinfo(
                title="Done", message="Audio replacement completed successfully"
            )
            self.quit()


class PathStringVar(tk.StringVar):
    @staticmethod
    def is_valid(value: str) -> bool:
        return is_pathname_valid(value)

    def set(self, value: str):
        if not PathStringVar.is_valid(value):
            raise ValueError(f"Invalid path: {value}")
        return super().set(os.path.normpath(value))

    def make_update_command(self, callback: Callable[[], str]) -> Callable[[], None]:
        def command():
            self.set(callback())

        return command


if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
