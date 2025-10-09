# FFmpeg-based RTMP streaming adapter for YouTube Live
# Replaces OBS with headless streaming solution

import os
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv


class StreamAdapter:
    """
    Headless streaming adapter using FFmpeg to broadcast to YouTube Live via RTMP.

    Displays question and answer text overlays on a static background image.
    """

    def __init__(self) -> None:
        load_dotenv()

        # Get RTMP credentials from environment
        self.rtmp_url = os.environ.get('YOUTUBE_RTMP_URL')
        self.stream_key = os.environ.get('YOUTUBE_STREAM_KEY')

        if not self.rtmp_url or not self.stream_key:
            raise Exception("YouTube RTMP credentials not configured. Set YOUTUBE_RTMP_URL and YOUTUBE_STREAM_KEY in .env")

        # Text overlay state
        self.question_text = ""
        self.answer_text = ""

        # FFmpeg process (will be started when streaming begins)
        self.ffmpeg_process = None

        # Background image path (can be customized via environment variable)
        self.background_image = os.environ.get('STREAM_BACKGROUND_IMAGE', '/app/assets/images/background.png')

    def set_question(self, text: str):
        """Set the question text to display on stream"""
        self.question_text = text
        self._update_overlay()

    def set_answer(self, text: str):
        """Set the answer text to display on stream"""
        self.answer_text = text
        self._update_overlay()

    def _update_overlay(self):
        """
        Update the text overlay on the stream.

        In a production implementation, this would dynamically update the FFmpeg
        drawtext filter. For now, this is a placeholder for the overlay logic.

        TODO: Implement dynamic text overlay update mechanism
        """
        # For initial implementation, we'll log the text changes
        # Full implementation would require either:
        # 1. Regenerating overlay images and updating FFmpeg input
        # 2. Using FFmpeg's zmq filter for dynamic text updates
        # 3. Using a separate overlay rendering service

        print(f"[Stream Overlay] Question: {self.question_text}")
        print(f"[Stream Overlay] Answer: {self.answer_text}")

    def _build_ffmpeg_command(self) -> list[str]:
        """
        Build FFmpeg command for RTMP streaming.

        Returns:
            list[str]: FFmpeg command arguments

        Note: This method is extracted for testability. It constructs the command
        but does not execute it.
        """
        rtmp_destination = f"{self.rtmp_url}/{self.stream_key}"

        # FFmpeg command for streaming
        # Note: This is a basic implementation. Text overlay updates require
        # more advanced techniques (see _update_overlay TODO)
        ffmpeg_cmd = [
            'ffmpeg',
            '-re',  # Read input at native frame rate
            '-loop', '1',  # Loop the background image
            '-i', self.background_image,  # Input: background image
            '-vf', f"drawtext=text='{self.question_text}':fontsize=24:fontcolor=white:x=50:y=50,"
                   f"drawtext=text='{self.answer_text}':fontsize=32:fontcolor=yellow:x=50:y=100",
            '-c:v', 'libx264',  # Video codec
            '-preset', 'veryfast',  # Encoding preset for low latency
            '-maxrate', '3000k',  # Max bitrate
            '-bufsize', '6000k',  # Buffer size
            '-pix_fmt', 'yuv420p',  # Pixel format
            '-g', '50',  # GOP size
            '-c:a', 'aac',  # Audio codec (currently no audio input)
            '-b:a', '128k',  # Audio bitrate
            '-f', 'flv',  # Output format (RTMP uses FLV)
            rtmp_destination
        ]

        return ffmpeg_cmd

    def start_stream(self):
        """
        Start FFmpeg RTMP streaming to YouTube Live.

        Uses a static background with text overlays for question/answer display.
        """
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            print("[StreamAdapter] Stream already running")
            return

        ffmpeg_cmd = self._build_ffmpeg_command()

        try:
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"[StreamAdapter] FFmpeg streaming started to {self.rtmp_url}")
        except FileNotFoundError:
            raise Exception("FFmpeg not found. Please install FFmpeg in the Docker container")
        except Exception as e:
            raise Exception(f"Failed to start FFmpeg stream: {e}")

    def stop_stream(self):
        """Stop the FFmpeg streaming process"""
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait(timeout=5)
            print("[StreamAdapter] Stream stopped")

    def is_streaming(self) -> bool:
        """Check if stream is currently active"""
        return self.ffmpeg_process is not None and self.ffmpeg_process.poll() is None


if __name__ == '__main__':
    # Test the adapter
    import random

    adapter = StreamAdapter()

    question_text = "Question number is " + str(random.randint(0, 100))
    adapter.set_question(question_text)

    answer_text = "Answer number is " + str(random.randint(0, 100))
    adapter.set_answer(answer_text)

    print("\nNote: To actually start streaming, call adapter.start_stream()")
    print("This requires valid RTMP credentials and FFmpeg installed")
