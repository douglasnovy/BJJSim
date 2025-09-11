# Contributing to BJJSim

Thank you for helping build an open, rigorous BJJ self-play simulation.

## Development standards

- Python 3.12 only
- Type hints required everywhere (public and private). CI enforces `mypy --strict`.
- Style: `ruff` (lint and format). Pre-commit hooks must pass.
- Tests: `pytest`. Add tests for new behavior. Prefer small, focused tests.
- Documentation: Update relevant docs under `docs/` with each change.

### Code Formatting Requirements

This project enforces strict formatting standards to prevent CI failures:

- **Line endings**: Unix LF only (configured via `.gitattributes`)
- **File endings**: All files must end with a newline
- **Whitespace**: No trailing whitespace allowed
- **Character encoding**: UTF-8 only
- **Indentation**: 4 spaces for Python, 2 spaces for YAML/JSON

### Editor Configuration

The project includes `.editorconfig` for automatic editor compliance. Most editors will automatically:
- Use LF line endings
- Insert final newlines
- Trim trailing whitespace
- Use correct indentation

**Recommended VS Code settings** (add to your settings.json):
```json
{
    "files.eol": "\n",
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "editor.formatOnSave": true
}
```

## Workflow

1. Create an issue describing the change.
2. Create a branch: `feature/<short-description>`.
3. **Required setup**: Run `pre-commit install --install-hooks` once to prevent formatting issues.
4. Make changes and commit frequently.
5. **Before pushing**: Run `pre-commit run --all-files` to catch any formatting issues.
6. Ensure `ruff`, `mypy`, and `pytest` are green locally.
7. Open a PR linking the issue and updating docs.

### Preventing Common Formatting Issues

Run these commands locally to avoid CI failures:

```bash
# Install and setup pre-commit (required once)
pre-commit install --install-hooks

# Check all files for formatting issues
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Run specific checks
ruff check .
ruff format --check .
mypy src/
```

**Note**: The `attached_assets/` directory is ignored by git and pre-commit to prevent ephemeral file formatting issues.

## Code organization

- `src/bjjsim/` for package code
- `tests/` for tests mirroring module structure
- `scripts/` for developer utilities (no library imports from here)
- `docs/` for requirements, architecture, planning

## Type hints

- Prefer `typing` and `collections.abc` over `typing_extensions` (Python 3.12).
- Use `TypedDict`/`Protocol` for structured dicts and interfaces.
- Avoid `Any`; when unavoidable, encapsulate and document the boundary.

## Commits and PRs

- Conventional commits recommended: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Keep PRs small and focused. Include a short motivation and design notes.
