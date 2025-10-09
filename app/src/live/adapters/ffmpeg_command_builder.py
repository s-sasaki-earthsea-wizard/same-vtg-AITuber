"""
FFmpeg command construction for RTMP streaming.

This module builds FFmpeg command lines for YouTube Live streaming
with dynamic text overlays and audio support.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class StreamConfig:
    """
    Configuration for FFmpeg streaming.

    Attributes:
        rtmp_url: RTMP server URL (e.g., rtmp://a.rtmp.youtube.com/live2)
        stream_key: Stream key for authentication
        background_image: Path to background image file
        question_textfile: Path to question text file for overlay
        answer_textfile: Path to answer text file for overlay
        audio_file: Optional path to audio file (WAV format)
    """
    rtmp_url: str
    stream_key: str
    background_image: str
    question_textfile: str
    answer_textfile: str
    audio_file: Optional[str] = None


class FFmpegCommandBuilder:
    """
    Builds FFmpeg command lines for RTMP streaming.

    Constructs commands for streaming with:
    - Dynamic text overlays (textfile + reload=1)
    - Audio input (WAV file or silent audio)
    - Video encoding (H.264)
    - Audio encoding (AAC)
    """

    @staticmethod
    def build_rtmp_command(config: StreamConfig) -> list[str]:
        """
        Build FFmpeg command for RTMP streaming with dynamic text overlays and audio.

        Args:
            config: Stream configuration

        Returns:
            list[str]: FFmpeg command arguments

        Note: Text overlays are dynamically updated using textfile + reload=1 mechanism.
        FFmpeg reads the text files every frame, enabling real-time text updates.

        Audio can be provided via config.audio_file. If no audio file is set,
        silent audio will be used (anullsrc).
        """
        rtmp_destination = f"{config.rtmp_url}/{config.stream_key}"

        # Base FFmpeg command
        ffmpeg_cmd = ['ffmpeg', '-re']  # Read input at native frame rate

        # Add audio input if available
        if config.audio_file and os.path.exists(config.audio_file):
            ffmpeg_cmd.extend(['-i', config.audio_file])  # Audio input
        else:
            # Use silent audio source if no audio file provided
            ffmpeg_cmd.extend([
                '-f', 'lavfi',
                '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100'
            ])

        # Add video input
        ffmpeg_cmd.extend([
            '-loop', '1',  # Loop the background image
            '-i', config.background_image,  # Input: background image
        ])

        # Video filter for text overlays
        ffmpeg_cmd.extend([
            '-vf', (
                f"drawtext=textfile={config.question_textfile}:reload=1:"
                f"fontsize=24:fontcolor=white:x=50:y=50,"
                f"drawtext=textfile={config.answer_textfile}:reload=1:"
                f"fontsize=32:fontcolor=yellow:x=50:y=100"
            ),
        ])

        # Video encoding settings
        ffmpeg_cmd.extend([
            '-c:v', 'libx264',  # Video codec
            '-preset', 'veryfast',  # Encoding preset for low latency
            '-maxrate', '3000k',  # Max bitrate
            '-bufsize', '6000k',  # Buffer size
            '-pix_fmt', 'yuv420p',  # Pixel format
            '-g', '50',  # GOP size
        ])

        # Audio encoding settings
        ffmpeg_cmd.extend([
            '-c:a', 'aac',  # Audio codec
            '-b:a', '128k',  # Audio bitrate
            '-ar', '44100',  # Audio sample rate
        ])

        # Output format and destination
        ffmpeg_cmd.extend([
            '-shortest',  # Stop when shortest input ends (for audio sync)
            '-f', 'flv',  # Output format (RTMP uses FLV)
            rtmp_destination
        ])

        return ffmpeg_cmd
