# Streaming-related Makefile targets
# This file contains commands for running streaming demos and production streaming

.PHONY: stream-demo stream-demo-help stream-start-prod

## Streaming Commands

# Default duration for streaming demo (can be overridden: make demo DURATION=30)
DURATION ?= 60

stream-demo:  ## Run manual streaming demo (development only, DURATION=60)
	@echo "============================================================"
	@echo "=== RTMP Streaming Demo ==="
	@echo "============================================================"
	@echo "📺 View stream with VLC:"
	@echo "   vlc rtmp://localhost:1935/live/test"
	@echo ""
	@echo "Or from another machine (replace with your host IP):"
	@echo "   vlc rtmp://YOUR_HOST_IP:1935/live/test"
	@echo ""
	@echo "Duration: $(DURATION) seconds"
	@echo ""
	@echo "Starting demo..."
	@echo ""
	docker compose exec $(SERVICE_NAME) python src/live/manual_streaming_demo.py $(DURATION)

stream-demo-help:  ## Show detailed help for streaming demo
	@echo "============================================================"
	@echo "=== Manual Streaming Demo Help ==="
	@echo "============================================================"
	@echo ""
	@echo "Prerequisites:"
	@echo "  1. Start development environment with local RTMP server:"
	@echo "     make up-dev"
	@echo ""
	@echo "  2. Open VLC media player and connect to RTMP stream:"
	@echo "     vlc rtmp://localhost:1935/live/test"
	@echo ""
	@echo "  3. Run the demo script:"
	@echo "     make demo              # Default: 60 seconds"
	@echo "     make demo DURATION=30  # Custom: 30 seconds"
	@echo ""
	@echo "What the demo does:"
	@echo "  - Streams static background image with dynamic text overlays"
	@echo "  - Updates question/answer text every 10 seconds"
	@echo "  - Runs for specified duration (default: 60 seconds)"
	@echo "  - Tests Japanese font rendering (Noto Sans CJK)"
	@echo "  - No OpenAI API usage (no cost)"
	@echo ""
	@echo "Troubleshooting:"
	@echo "  - If text appears garbled, ensure container has fonts-noto-cjk installed"
	@echo "  - If VLC can't connect, check RTMP server is running: docker compose ps"
	@echo "  - Check RTMP server logs: make logs-rtmp"
	@echo ""

stream-start-prod:  ## Start production YouTube Live streaming (not yet implemented)
	@echo "🚧 Production streaming not yet implemented"
	@echo ""
	@echo "Planned features:"
	@echo "  - Fetch latest YouTube Live video ID from channel"
	@echo "  - Start AITuberSystem with YouTube comment monitoring"
	@echo "  - Stream to YouTube Live via RTMP"
	@echo ""

## Convenience aliases
demo: stream-demo  ## Alias for stream-demo
demo-help: stream-demo-help  ## Alias for stream-demo-help
