# RAGStudyBot justfile

# Run the development server
server:
    uv run uvicorn app.main:app --reload

# Run tests
test:
    uv run pytest

# Run linter
lint:
    uv run ruff check .

# Format code
fmt:
    uv run ruff format .

# Check formatting without modifying
fmt-check:
    uv run ruff format --check .

# Run lint + format fix
fix:
    uv run ruff check --fix .
    uv run ruff format .

# Install pre-commit hooks
hooks:
    pre-commit install
