#!/usr/bin/env python3
"""
Manual test script for StreamAdapter with local RTMP server.

This script tests the dynamic text overlay functionality by:
1. Starting a stream to local RTMP server
2. Updating question and answer text dynamically
3. Running for a short duration to verify text updates

Prerequisites:
- Local RTMP server running (make up-dev)
- Environment variables configured for local RTMP
- View stream with: vlc rtmp://localhost:1935/live/test
"""

import os
import sys
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from live.StreamAdapter import StreamAdapter


def main():
    """Run manual stream test with dynamic text updates"""
    print("[Manual Test] Starting StreamAdapter test with local RTMP server")
    print("[Manual Test] Make sure:")
    print("  1. Local RTMP server is running (make up-dev)")
    print("  2. .env is configured for local RTMP:")
    print("     YOUTUBE_RTMP_URL=rtmp://rtmp-server:1935/live")
    print("     YOUTUBE_STREAM_KEY=test")
    print("  3. View stream with: vlc rtmp://localhost:1935/live/test")
    print()

    # Check environment
    rtmp_url = os.environ.get('YOUTUBE_RTMP_URL')
    stream_key = os.environ.get('YOUTUBE_STREAM_KEY')

    print(f"[Manual Test] RTMP URL: {rtmp_url}")
    print(f"[Manual Test] Stream Key: {stream_key}")
    print()

    if 'rtmp-server' not in rtmp_url:
        print("[WARNING] RTMP URL does not point to local server!")
        print("[WARNING] This test should use local RTMP server.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("[Manual Test] Test cancelled")
            return

    # Initialize adapter
    print("[Manual Test] Initializing StreamAdapter...")
    adapter = StreamAdapter()

    # Set initial text
    print("[Manual Test] Setting initial text...")
    adapter.set_question("Initial Question: こんにちは！")
    adapter.set_answer("Initial Answer: よろしくお願いします！")

    # Start streaming
    print("[Manual Test] Starting stream...")
    adapter.start_stream()

    if not adapter.is_streaming():
        print("[ERROR] Stream failed to start!")
        return

    print("[Manual Test] Stream started successfully!")
    print("[Manual Test] Watch stream with: vlc rtmp://localhost:1935/live/test")
    print()

    # Update text dynamically
    test_duration = 30  # seconds
    update_interval = 5  # seconds

    print(f"[Manual Test] Running for {test_duration} seconds with text updates every {update_interval} seconds...")

    for i in range(test_duration // update_interval):
        time.sleep(update_interval)

        # Update text
        question = f"Question #{i+1}: 現在 {(i+1) * update_interval} 秒経過"
        answer = f"Answer #{i+1}: テキストが動的に更新されています！"

        print(f"[Manual Test] Updating text (iteration {i+1})...")
        adapter.set_question(question)
        adapter.set_answer(answer)

    print()
    print("[Manual Test] Test complete! Stopping stream...")
    adapter.stop_stream()
    print("[Manual Test] Stream stopped.")
    print()
    print("[Manual Test] Test Summary:")
    print(f"  - Duration: {test_duration} seconds")
    print(f"  - Text updates: {test_duration // update_interval}")
    print(f"  - Final question: {adapter.question_text}")
    print(f"  - Final answer: {adapter.answer_text}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Manual Test] Test interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
