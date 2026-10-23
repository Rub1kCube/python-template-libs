SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
# =============================================================================
# Variables
# =============================================================================

.ONESHELL:
.EXPORT_ALL_VARIABLES:
.DEFAULT_GOAL:=help
MAKEFLAGS += --no-print-directory

# Colors and formatting
BLUE := $(shell printf "\033[1;34m")
GREEN := $(shell printf "\033[1;32m")
RED := $(shell printf "\033[1;31m")
YELLOW := $(shell printf "\033[1;33m")
NC := $(shell printf "\033[0m")
INFO := $(shell printf "$(BLUE)ℹ$(NC)")
OK := $(shell printf "$(GREEN)✓$(NC)")
WARN := $(shell printf "$(YELLOW)⚠$(NC)")
ERROR := $(shell printf "$(RED)✖$(NC)")


.PHONY: help
help:
# Docs: Show all available targets
	@echo ""
	@echo -e "🧭  \033[1;36mMake Targets\033[0m"
	@echo "──────────────────────────────────────────────"
	@grep -E '^[a-zA-Z0-9_.-]+:|# Docs:' $(MAKEFILE_LIST) | \
	grep -v 'grep -E' | \
	awk 'BEGIN {FS=":"; target=""} \
	/^[a-zA-Z0-9_.-]+/ {target=$$1} \
	/# Docs:/ { \
		sub(/.*# Docs:[[:space:]]*/,""); \
		if (target != "") { \
			printf "\033[1;33m• %-25s\033[0m — %s\n", target, $$0; \
			target=""; \
		} \
	}'

# =============================================================================
# Development tools
# =============================================================================
.PHONY: install
install: destroy clean
# Docs: Install the project, dependencies, and Git hooks for local development
	@echo "${INFO} Starting installation... ⬇️"
	@uv python pin 3.12 >/dev/null 2>&1
	@uv venv >/dev/null 2>&1
	@uv sync --all-groups --all-extras
	@echo "${INFO} Installing Git hooks ⬇️"
	prek install --install-hooks
	@echo "${OK} Installation complete ✨! $(shell printf "$(BLUE)Note:$(NC)") To reinstall, run $(shell printf "$(GREAN)'make install'$(NC)")"

.PHONY: upgrade
upgrade:
# Docs: Update all dependencies to their latest stable versions
	@echo "${INFO} Updating all dependencies 🔄"
	@uv lock --upgrade
	@echo "${OK} Dependencies updated 🔄"
	@uv run prek autoupdate
	@echo "${OK} prek hooks updated 🔄"

.PHONY: lock
lock:
# Docs: Update the lockfile from the declared dependencies
	@uv lock

.PHONY: destroy
destroy:
# Docs: Remove the virtual environment
	@@echo "${INFO} Destroying virtual environment... 🗑️"
	@rm -rf .venv
	@echo "${OK} Virtual environment destroyed 🗑️"

.PHONY: clean
clean:
# Docs: Remove generated tool artifacts
	@echo "${INFO} Cleaning the working directory 🧹"
	@rm -rf .pytest_cache .ruff_cache .hypothesis build/ dist/ .eggs/ .egg/ .precomcache
	@find . -name '*.egg-info' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '.ipynb_checkpoints' -exec rm -rf {} +
	@rm -rf .coverage coverage.xml coverage.json htmlcov/ .pytest_cache tests/.pytest_cache tests/**/.pytest_cache .mypy_cache
	@echo "${OK} Cleanup complete ✨"


# ============================================================================ #
# Type checking
# ============================================================================ #

.PHONY: mypy
mypy:
# Docs: Run mypy
	@echo "${INFO} Running mypy... 🔍"
	@uv run mypy . $(args)
	@echo "${OK} mypy checks complete ✨"

.PHONY: pyright
pyright:
# Docs: Run Pyright
	@echo "${INFO} Running Pyright... 🔍"
	@uv run pyright
	@echo "${OK} Pyright checks complete ✨"

.PHONY: type-check
type-check: mypy pyright
# Docs: Run all type checkers


# ============================================================================ #
# Testing
# ============================================================================ #

.PHONY: test
test:
# Docs: Run tests
	@echo "${INFO} Running tests... 🧪"
	@uv run pytest tests -q
	@echo "${OK} Tests complete ✨"


# ============================================================================ #
# Linting
# ============================================================================ #

.PHONY: lint
lint:
# Docs: Run the linter and apply fixes
	@echo "${INFO} Running Ruff with fixes... 🔧"
	@uv run ruff check . --fix
	@echo "${OK} Lint fixes applied ✨"


.PHONY: check
check:
# Docs: Run all prek checks for the project
	@echo "${INFO} Running prek... 🔎"
	PREK_HOME=".precomcache/" uv run prek run --all-files
	@echo "${OK} prek checks complete ✨"


.PHONY: check-all
check-all: test check
# Docs: Run all checks
