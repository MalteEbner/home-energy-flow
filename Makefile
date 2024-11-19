# Install package for local development.
.PHONY: install-dev
install-dev:
	uv pip install -e .

# run formatter
.PHONY: format
format: 
	# Format code
	ruff format src
	# Fix linting issues and sort imports
	ruff check --fix src

# run format check
.PHONY: format-check
format-check:
	# Check code formatting
	ruff check src

# run type check
.PHONY: type-check
type-check:
	mypy src

# run format and type checks
.PHONY: static-checks
static-checks: format-check type-check