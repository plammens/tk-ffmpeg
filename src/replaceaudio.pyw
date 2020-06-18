"""
Tk GUI app to replace the audio channel from a video using ffmpeg
"""

import subprocess


def replace_audio(
    video_path: str, new_audio_path: str, output_path: str
) -> subprocess.CompletedProcess:
    args = (
        f"ffmpeg -i {video_path} -i {new_audio_path} "
        f"-vcodec copy -acodec copy -map 0:0 -map 1:0 {output_path}"
    )
    return subprocess.run(args, check=True)
