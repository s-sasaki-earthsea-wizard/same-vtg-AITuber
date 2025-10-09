# FFmpeg-based RTMP streaming adapter for YouTube Live
# Replaces OBS with headless streaming solution

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from .adapters.stream_file_manager import StreamFileManager
from .adapters.ffmpeg_command_builder import FFmpegCommandBuilder, StreamConfig


class StreamAdapter:
    """
    Headless streaming adapter using FFmpeg to broadcast to YouTube Live via RTMP.

    Displays question and answer text overlays on a static background image.
    Text overlays are dynamically updated using FFmpeg's textfile + reload mechanism.
    Audio can be provided via set_audio_file() for synchronized A/V streaming.
    """

    def __init__(self) -> None:
        load_dotenv()

        # Get RTMP credentials from environment
        self.rtmp_url = os.environ.get('STREAM_RTMP_URL')
        self.stream_key = os.environ.get('STREAM_KEY')

        if not self.rtmp_url or not self.stream_key:
            raise Exception("RTMP streaming credentials not configured. Set STREAM_RTMP_URL and STREAM_KEY in .env")

        # Text overlay state
        self.question_text = ""
        self.answer_text = ""

        # Text file paths for dynamic overlay updates
        self.question_textfile = '/tmp/stream_question.txt'
        self.answer_textfile = '/tmp/stream_answer.txt'

        # Initialize text files using StreamFileManager
        StreamFileManager.initialize_text_files(
            self.question_textfile,
            self.answer_textfile
        )

        # Audio file path for streaming
        self.audio_file = None

        # FFmpeg process (will be started when streaming begins)
        self.ffmpeg_process = None

        # Background image path (can be customized via environment variable)
        self.background_image = os.environ.get('STREAM_BACKGROUND_IMAGE', '/app/assets/images/background.png')

    def set_question(self, text: str):
        """
        Set the question text to display on stream.

        Updates the text file atomically so FFmpeg can reload it in real-time.
        """
        self.question_text = text
        StreamFileManager.write_text_file(self.question_textfile, text)
        print(f"[Stream Overlay] Question: {text}")

    def set_answer(self, text: str):
        """
        Set the answer text to display on stream.

        Updates the text file atomically so FFmpeg can reload it in real-time.
        """
        self.answer_text = text
        StreamFileManager.write_text_file(self.answer_textfile, text)
        print(f"[Stream Overlay] Answer: {text}")

    def set_audio_file(self, filepath: str):
        """
        Set the audio file path for streaming.

        Args:
            filepath: Path to WAV audio file to stream

        Note: Audio will be included in the next stream start.
        For real-time audio updates during streaming, the stream must be restarted.
        """
        if not os.path.exists(filepath):
            print(f"[StreamAdapter] Warning: Audio file not found: {filepath}")

        self.audio_file = filepath
        print(f"[StreamAdapter] Audio file set: {filepath}")

    def _build_ffmpeg_command(self) -> list[str]:
        """
        Build FFmpeg command for RTMP streaming with dynamic text overlays and audio.

        Returns:
            list[str]: FFmpeg command arguments

        Note: This method is extracted for testability. It constructs the command
        but does not execute it.

        Delegates to FFmpegCommandBuilder for command construction.
        """
        config = StreamConfig(
            rtmp_url=self.rtmp_url,
            stream_key=self.stream_key,
            background_image=self.background_image,
            question_textfile=self.question_textfile,
            answer_textfile=self.answer_textfile,
            audio_file=self.audio_file
        )

        return FFmpegCommandBuilder.build_rtmp_command(config)

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
