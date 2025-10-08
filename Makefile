# Main Makefile for same-vtg-AITuber project
# This file includes all sub-makefiles and provides the help command

.PHONY: help

# Default target
default: help

# Include all sub-makefiles
include makefiles/docker.mk

# Add more includes here as needed:
# include makefiles/test.mk
# include makefiles/lint.mk
# include makefiles/deploy.mk

## Help
help:  ## Show this help message
	@echo "=== Available Commands ==="
	@echo ""
	@echo "\033[1mDocker Commands:\033[0m"
	@grep -E '^docker-[a-zA-Z_-]+:.*?## .*$$' makefiles/docker.mk | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[1mConvenience Aliases:\033[0m"
	@grep -E '^(up|start|down|restart|logs|shell|build|rebuild|clean|env-setup|env-check):.*?## .*$$' makefiles/docker.mk | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[1mHelp:\033[0m"
	@echo "  \033[36mhelp                \033[0m Show this help message"
	@echo ""
	@echo "Note: Detailed help files can be added to makefiles/helps/ directory"