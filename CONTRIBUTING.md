# Contributing to Authentrics Client

This guide is for Authentrics.ai employees who want to contribute to the Authentrics Client project.

## Prerequisites

- Python 3.9 or higher (preferred 3.9 for development)
- Poetry (for dependency management)
- Git

## Development Setup

### 1. Install Poetry

If you haven't installed Poetry yet:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or using pip:

```bash
pip install poetry
```

### 2. Clone the Repository

```bash
git clone https://github.com/Authentrics-ai/authentrics-client
cd authentrics-client
```

### 3. Install Dependencies

```bash
# Install all dependencies including development dependencies
poetry install

# Activate the virtual environment
$(poetry env activate)
```

## Development Workflow

### Code Style and Linting

This project uses Ruff for linting and formatting. The configuration is in `pyproject.toml`.

```bash
# Format code
ruff format

# Lint code
ruff check

# Lint and fix basic issues in one command
ruff check --fix
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests in verbose mode
pytest -v

# Run specific test file
pytest test/test_client.py
```

## Building the Package

### 1. Build Source Distribution and Wheel

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
poetry build
```

This will create:

- `dist/authentrics-client-{version}.tar.gz` (source distribution)
- `dist/authentrics_client-{version}-py3-none-any.whl` (wheel)

### 2. Verify the Build

```bash
# Check the built package
twine check dist/*
```

### 3. Publish Using Google Artifact Registry

```bash
# Configure authentication if you're not using a service account
gcloud auth login

# Upload to GAR
twine upload --repository-url https://us-central1-python.pkg.dev/authentrics/authentrics-repo/ dist/*
```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Testing

- Write tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test both success and failure cases

### Documentation

- Update docstrings when changing function signatures
- Add examples in docstrings for complex functions
- Update README.md if adding new features
- Document any breaking changes

### Git Workflow

1. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:

   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```

3. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Troubleshooting

### Common Issues

**Poetry install fails:**

```bash
# Clear Poetry cache
poetry cache clear . --all

# Reinstall dependencies
poetry install --sync
```

**Build fails:**

```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info/
poetry build
```

**Upload fails:**

```bash
# Check credentials
poetry run keyring list

# Verify package
poetry run twine check dist/*
```

### Getting Help

- Check the [Poetry documentation](https://python-poetry.org/docs/)
- Review the [Twine documentation](https://twine.readthedocs.io/)
- Ask in the team Slack channel
- Create an issue in the repository

## Release Checklist

Before releasing a new version:

- [ ] All tests pass
- [ ] Code is linted and formatted
- [ ] Documentation is updated
- [ ] Version is incremented in `pyproject.toml`
- [ ] Package builds successfully
- [ ] Package installs correctly from test repository
- [ ] Release notes are prepared
- [ ] Tag is created and pushed

## Security

- Never commit API keys or sensitive credentials
- Keep dependencies updated
- Report security issues privately to the team

---

Thank you for contributing to the Authentrics Client project!
