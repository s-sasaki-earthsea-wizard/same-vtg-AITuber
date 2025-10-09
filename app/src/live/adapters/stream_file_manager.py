"""
File management utilities for streaming text overlays.

This module handles atomic file operations for FFmpeg text overlay updates.
"""

import os
import tempfile


class StreamFileManager:
    """
    Manages file I/O operations for streaming text overlays.

    Uses atomic file write operations (temp file + rename) to prevent
    FFmpeg from reading partially written files.
    """

    @staticmethod
    def write_text_file(filepath: str, text: str) -> None:
        """
        Write text to file atomically to avoid partial reads by FFmpeg.

        Uses temp file + rename pattern for atomic file updates.

        Args:
            filepath: Target file path
            text: Text content to write

        Raises:
            Exception: If file write fails
        """
        # Write to temporary file first
        temp_fd, temp_path = tempfile.mkstemp(dir='/tmp', text=True)
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                f.write(text)
            # Atomic rename (POSIX guarantees atomicity)
            os.rename(temp_path, filepath)
        except Exception as e:
            # Clean up temp file if rename fails
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise Exception(f"Failed to write text file {filepath}: {e}")

    @staticmethod
    def initialize_text_files(question_file: str, answer_file: str) -> None:
        """
        Initialize text files with empty content.

        Args:
            question_file: Path to question text file
            answer_file: Path to answer text file

        Raises:
            Exception: If file initialization fails
        """
        StreamFileManager.write_text_file(question_file, "")
        StreamFileManager.write_text_file(answer_file, "")
