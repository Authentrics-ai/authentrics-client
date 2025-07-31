# Authentrics Client

A Python client for Authentrics.ai backend libraries that provides tools for model analysis, checkpoint management, and authentication.

## Features

- **Model Analysis**: Static and dynamic analysis of machine learning models
- **Checkpoint Management**: Upload, manage, and analyze model checkpoints
- **Authentication**: Secure login and session management
- **CLI Interface**: Command-line tools for easy interactive login
- **Transformers Integration**: Callback support for 🤗 Transformers training

## Installation

```bash
pip install authentrics-client
```

For CLI functionality:

```bash
pip install authentrics-client[cli]
```

For Transformers integration:

```bash
pip install authentrics-client[transformers]
```

## Quick Start

```python
from authentrics_client import AuthentricsClient

# Initialize client
client = AuthentricsClient("https://api.authentrics.ai")

# Login
client.auth.login("username", "password")

# Create a project
project = client.project.create_project("My Model Project", "Description")

# Upload a checkpoint
result = client.checkpoint.upload_checkpoint(
    project_id=project["id"],
    file_path="path/to/model.onnx",
    model_format="onnx",
)
```

## CLI Usage

```bash
# Login to Authentrics
authrx login --username=your_username --password=your_password

# View available commands
authrx --help
```

## Examples

For more detailed examples and use cases, see the [examples directory](./examples).

## Documentation

For comprehensive documentation, visit the [Authentrics.ai documentation](https://authentrics-team-lrq1a2rkieci.atlassian.net/wiki/spaces/Authentric1/overview).

## Requirements

- Python 3.9+
- requests >= 2.32.4
- pyjwt >= 2.10.1

## Contributing

For Authentrics.ai employees, please see [CONTRIBUTING.md](./CONTRIBUTING.md).
