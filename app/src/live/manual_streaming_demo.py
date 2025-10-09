#!/usr/bin/env python3
"""
Manual streaming demo script for testing RTMP streaming with VLC.

This script demonstrates:
- RTMP streaming to local server
- Dynamic text overlay updates
- Background image display

Usage:
1. Start local RTMP server: make up-dev
2. Open VLC: vlc rtmp://localhost:1935/live/test
3. Run this script:
   docker compose exec same-vtg-aituber python src/live/manual_streaming_demo.py [duration]

   Or use make:
   make demo              # 60 seconds (default)
   make demo DURATION=30  # 30 seconds
"""

import time
import sys
import os
import argparse

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from live.StreamAdapter import StreamAdapter


def main(duration: int = 60):
    print("=" * 60)
    print("[Demo] RTMP Streaming Demo - StreamAdapter Test")
    print("=" * 60)
    print()

    print("[Demo] Initializing StreamAdapter...")
    adapter = StreamAdapter()

    print(f"[Demo] RTMP URL: {adapter.rtmp_url}")
    print(f"[Demo] Stream Key: {adapter.stream_key}")
    print(f"[Demo] Background: {adapter.background_image}")
    print()

    # Set initial overlay text
    print("[Demo] Setting overlay text...")
    adapter.set_question("テスト質問: RTMPストリーミングは動作していますか？")
    adapter.set_answer("テスト回答: はい、正常に動作しています！")
    print()

    # Start streaming
    print("[Demo] Starting RTMP stream...")
    adapter.start_stream()

    if adapter.is_streaming():
        print("[Demo] ✅ Stream started successfully!")
        print()
        print("=" * 60)
        print("📺 View the stream with VLC:")
        print("   vlc rtmp://localhost:1935/live/test")
        print("=" * 60)
        print()
        print(f"[Demo] Streaming for {duration} seconds...")
        print("[Demo] Text will update every 10 seconds to test dynamic overlay...")
        print()

        # Update text during stream to demonstrate dynamic overlay
        update_interval = 10
        num_updates = duration // update_interval
        remaining_time = duration % update_interval

        for i in range(num_updates):
            time.sleep(update_interval)
            elapsed = (i + 1) * update_interval
            adapter.set_answer(f"テスト回答: {elapsed}秒経過しました。動的更新テスト中...")
            print(f"[Demo] ⏱️  {elapsed}s - Text overlay updated")

        # Sleep for any remaining time
        if remaining_time > 0:
            time.sleep(remaining_time)

        print()
        print("[Demo] Stopping stream...")
        adapter.stop_stream()
        print("[Demo] ✅ Stream stopped")
        print()
        print("[Demo] Demo completed successfully!")
        print()
        print("Expected results in VLC:")
        print("  ✅ Background image displayed")
        print("  ✅ Question text (white, top)")
        print("  ✅ Answer text (yellow, below question)")
        print("  ✅ Text updated every 10 seconds")
        print("  ⚠️  No audio (silent stream)")
    else:
        print("[Demo] ❌ Failed to start stream")
        print("[Demo] Check FFmpeg errors above")
        print()
        print("Troubleshooting:")
        print("  1. Make sure RTMP server is running: docker ps | grep rtmp")
        print("  2. Check .env configuration")
        print("  3. Verify background image exists")
        return 1

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RTMP Streaming Demo")
    parser.add_argument(
        "duration",
        type=int,
        nargs="?",
        default=60,
        help="Streaming duration in seconds (default: 60)"
    )
    args = parser.parse_args()

    try:
        exit_code = main(duration=args.duration)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[Demo] Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[Demo] ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
