"""
Unit tests for StreamAdapter FFmpeg RTMP streaming functionality.

These tests verify the StreamAdapter without actually starting RTMP streams:
- FFmpeg command construction
- Text overlay configuration
- Background image path handling
- RTMP URL and Stream Key configuration

Note: These are unit tests that do NOT make actual RTMP connections.
No streaming to YouTube Live occurs during testing.
"""

import os
import pytest
from pathlib import Path
from live.StreamAdapter import StreamAdapter


class TestStreamAdapter:
    """Test suite for StreamAdapter class"""

    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Setup mock environment variables for testing"""
        monkeypatch.setenv('YOUTUBE_RTMP_URL', 'rtmp://test.example.com/live')
        monkeypatch.setenv('YOUTUBE_STREAM_KEY', 'test-stream-key-12345')
        monkeypatch.setenv('STREAM_BACKGROUND_IMAGE', '/app/assets/images/background.png')

    def test_stream_adapter_initialization(self, mock_env):
        """Test StreamAdapter initializes with correct configuration"""
        adapter = StreamAdapter()

        assert adapter.rtmp_url == 'rtmp://test.example.com/live'
        assert adapter.stream_key == 'test-stream-key-12345'
        assert adapter.background_image == '/app/assets/images/background.png'
        assert adapter.question_text == ""
        assert adapter.answer_text == ""
        assert adapter.ffmpeg_process is None

        # Verify text file paths are initialized
        assert adapter.question_textfile == '/tmp/stream_question.txt'
        assert adapter.answer_textfile == '/tmp/stream_answer.txt'

        # Verify text files are created and empty
        assert os.path.exists(adapter.question_textfile)
        assert os.path.exists(adapter.answer_textfile)
        with open(adapter.question_textfile, 'r') as f:
            assert f.read() == ""
        with open(adapter.answer_textfile, 'r') as f:
            assert f.read() == ""

    def test_stream_adapter_missing_credentials(self, monkeypatch):
        """Test StreamAdapter raises exception when credentials are missing"""
        monkeypatch.delenv('YOUTUBE_RTMP_URL', raising=False)
        monkeypatch.delenv('YOUTUBE_STREAM_KEY', raising=False)

        with pytest.raises(Exception, match="YouTube RTMP credentials not configured"):
            StreamAdapter()

    def test_set_question_updates_text(self, mock_env, capsys):
        """Test set_question() updates question text and text file"""
        adapter = StreamAdapter()
        adapter.set_question("テスト質問ですか？")

        assert adapter.question_text == "テスト質問ですか？"

        # Verify text file was updated
        with open(adapter.question_textfile, 'r', encoding='utf-8') as f:
            assert f.read() == "テスト質問ですか？"

        # Check overlay update was called (via print output)
        captured = capsys.readouterr()
        assert "テスト質問ですか？" in captured.out

    def test_set_answer_updates_text(self, mock_env, capsys):
        """Test set_answer() updates answer text and text file"""
        adapter = StreamAdapter()
        adapter.set_answer("テスト回答です。")

        assert adapter.answer_text == "テスト回答です。"

        # Verify text file was updated
        with open(adapter.answer_textfile, 'r', encoding='utf-8') as f:
            assert f.read() == "テスト回答です。"

        # Check overlay update was called (via print output)
        captured = capsys.readouterr()
        assert "テスト回答です。" in captured.out

    def test_build_ffmpeg_command_structure(self, mock_env):
        """Test _build_ffmpeg_command() returns valid FFmpeg command"""
        adapter = StreamAdapter()
        adapter.set_question("質問テキスト")
        adapter.set_answer("回答テキスト")

        cmd = adapter._build_ffmpeg_command()

        # Verify command starts with ffmpeg
        assert cmd[0] == 'ffmpeg'

        # Verify essential FFmpeg arguments are present
        assert '-re' in cmd  # Real-time encoding
        assert '-loop' in cmd  # Loop background
        assert '-i' in cmd  # Input file
        assert '-vf' in cmd  # Video filter
        assert '-c:v' in cmd  # Video codec
        assert '-f' in cmd  # Output format

    def test_ffmpeg_command_includes_background_image(self, mock_env):
        """Test FFmpeg command includes background image path"""
        adapter = StreamAdapter()
        cmd = adapter._build_ffmpeg_command()

        # Background image should be in command
        assert '/app/assets/images/background.png' in cmd

    def test_ffmpeg_command_includes_rtmp_destination(self, mock_env):
        """Test FFmpeg command includes correct RTMP destination"""
        adapter = StreamAdapter()
        cmd = adapter._build_ffmpeg_command()

        # RTMP destination should be at the end
        expected_destination = 'rtmp://test.example.com/live/test-stream-key-12345'
        assert cmd[-1] == expected_destination

    def test_ffmpeg_command_includes_text_overlay(self, mock_env):
        """Test FFmpeg command includes textfile-based text overlay with reload"""
        adapter = StreamAdapter()
        adapter.set_question("Q: What is AI?")
        adapter.set_answer("A: Artificial Intelligence")

        cmd = adapter._build_ffmpeg_command()

        # Find the -vf (video filter) argument
        vf_index = cmd.index('-vf')
        vf_value = cmd[vf_index + 1]

        # Verify drawtext filters use textfile and reload
        assert 'drawtext' in vf_value
        assert 'textfile=/tmp/stream_question.txt' in vf_value
        assert 'textfile=/tmp/stream_answer.txt' in vf_value
        assert 'reload=1' in vf_value

    def test_ffmpeg_command_video_settings(self, mock_env):
        """Test FFmpeg command has correct video encoding settings"""
        adapter = StreamAdapter()
        cmd = adapter._build_ffmpeg_command()

        # Verify video codec settings
        assert 'libx264' in cmd  # H.264 codec
        assert 'veryfast' in cmd  # Encoding preset
        assert 'yuv420p' in cmd  # Pixel format
        assert 'flv' in cmd  # FLV format for RTMP

    def test_ffmpeg_command_bitrate_settings(self, mock_env):
        """Test FFmpeg command has correct bitrate settings"""
        adapter = StreamAdapter()
        cmd = adapter._build_ffmpeg_command()

        # Verify bitrate arguments
        assert '3000k' in cmd  # Max video bitrate
        assert '6000k' in cmd  # Buffer size
        assert '128k' in cmd  # Audio bitrate

    def test_is_streaming_initially_false(self, mock_env):
        """Test is_streaming() returns False when not streaming"""
        adapter = StreamAdapter()
        assert adapter.is_streaming() is False

    def test_background_image_default_path(self, monkeypatch):
        """Test default background image path when env var not set"""
        monkeypatch.setenv('YOUTUBE_RTMP_URL', 'rtmp://test.example.com/live')
        monkeypatch.setenv('YOUTUBE_STREAM_KEY', 'test-key')
        monkeypatch.delenv('STREAM_BACKGROUND_IMAGE', raising=False)

        adapter = StreamAdapter()

        assert adapter.background_image == '/app/assets/images/background.png'

    def test_question_and_answer_empty_by_default(self, mock_env):
        """Test question and answer text are empty strings by default"""
        adapter = StreamAdapter()

        assert adapter.question_text == ""
        assert adapter.answer_text == ""

    def test_multiple_text_updates(self, mock_env):
        """Test multiple consecutive text updates work correctly"""
        adapter = StreamAdapter()

        adapter.set_question("First question")
        assert adapter.question_text == "First question"

        adapter.set_question("Second question")
        assert adapter.question_text == "Second question"

        adapter.set_answer("First answer")
        assert adapter.answer_text == "First answer"

        adapter.set_answer("Second answer")
        assert adapter.answer_text == "Second answer"

    def test_text_file_atomic_write(self, mock_env):
        """Test text files are written atomically to avoid partial reads"""
        adapter = StreamAdapter()

        # Write a long text to verify atomic write
        long_text = "あ" * 1000  # 1000 Japanese characters

        adapter.set_question(long_text)

        # Verify the full text is written correctly
        with open(adapter.question_textfile, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == long_text
            assert len(content) == 1000

    def test_text_file_utf8_encoding(self, mock_env):
        """Test text files support UTF-8 encoding for Japanese text"""
        adapter = StreamAdapter()

        # Test with various Japanese text
        japanese_question = "こんにちは、これは質問ですか？"
        japanese_answer = "はい、これは回答です。日本語テスト。"

        adapter.set_question(japanese_question)
        adapter.set_answer(japanese_answer)

        # Verify UTF-8 encoding
        with open(adapter.question_textfile, 'r', encoding='utf-8') as f:
            assert f.read() == japanese_question

        with open(adapter.answer_textfile, 'r', encoding='utf-8') as f:
            assert f.read() == japanese_answer

    def test_text_file_overwrite_on_update(self, mock_env):
        """Test text files are overwritten (not appended) on update"""
        adapter = StreamAdapter()

        # Set initial text
        adapter.set_question("First")
        with open(adapter.question_textfile, 'r') as f:
            content1 = f.read()

        # Update with new text
        adapter.set_question("Second")
        with open(adapter.question_textfile, 'r') as f:
            content2 = f.read()

        # Verify content was replaced, not appended
        assert content2 == "Second"
        assert "First" not in content2


if __name__ == "__main__":
    # Allow running tests directly with: python test_stream_adapter.py
    pytest.main([__file__, "-v", "-s"])
