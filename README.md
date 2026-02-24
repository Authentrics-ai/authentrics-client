# Authentrics Client

Python client for the Authentrics API: model analysis, checkpoint management, and authentication.

## Requirements

- **Python** 3.9+

## Installation

### Basic Installation

Install the core client:

```bash
pip install authentrics-client
```

### Installation with CLI

For command-line login and tools, install with the optional CLI dependencies:

```bash
pip install authentrics-client[cli]
```

### Installation with Transformers

For 🤗 Transformers training callback support:

```bash
pip install authentrics-client[transformers]
```

## Quick Start

### Using the Client

```python
from authentrics_client import AuthentricsClient

# Initialize client
client = AuthentricsClient("https://api.authentrics.ai")

# Login
client.auth.login(username="your_username", password="your_password")

# Create a project
project = client.project.create_project(
    name="My Model Project",
    description="Description",
    model_format="onnx",
)

# Add a checkpoint
result = client.checkpoint.add_checkpoint(
    project_id=project["id"],
    file_path="path/to/model.onnx",
    model_format="onnx",
)
```

### Using Versioned Paths

Pass `api_version="v2"` to use versioned API paths (e.g. `/api/v2/project`, `/api/v2/auth/login`). The value is normalized (e.g. `"V2"` → `"v2"`). Omit it or pass `None` for unversioned (legacy) paths.

```python
# Versioned paths
client = AuthentricsClient("https://api.authentrics.ai", api_version="v2")

# Check which version is in use (read-only)
assert client.api_version == "v2"
```

## CLI Usage

The `authrx` CLI is available when installed with `[cli]`:

```bash
# Login
authrx login https://api.authentrics.ai --username=your_username --password=your_password

# Login with versioned paths
authrx login https://api.authentrics.ai --api-version=v2 --username=... --password=...

# View available commands
authrx --help
```

## Core Functionality

### Authentication

Login with username and password (or use environment variables `AAI_USERNAME`, `AAI_PASSWORD`):

```python
client.auth.login(username="user", password="pass")
# Or: client.auth.login()  # prompts or uses env
```

Register a new user:

```python
client.auth.register(
    username="newuser",
    email="user@example.com",
    password="secret",
    first_name="New",
    last_name="User",
)
```

### Projects and Checkpoints

Create a project, add checkpoints, and fetch project details:

```python
project = client.project.create_project(
    name="My Project",
    description="Example",
    model_format="onnx",
)
project = client.project.get_project_by_id(project["id"])

client.checkpoint.add_checkpoint(
    project_id=project["id"],
    file_path="path/to/checkpoint.onnx",
    model_format="onnx",
    checkpoint_name="v1",
    tag="v1",
)
```

### Static and Dynamic Analysis

Run static analysis on a checkpoint, or use the dynamic handler for comparative, correlation, and other analyses:

```python
result = client.static.static_analysis(
    project_id=project["id"],
    checkpoint_id=checkpoint_id,
)
```

For more workflows, see the [examples directory](./examples).

## API Reference

### Client

- **`AuthentricsClient(base_url, proxy_url=None, api_version=None)`**: Main client. `api_version="v2"` uses versioned paths; `None` uses unversioned (legacy).
- **`client.api_version`**: Read-only property; current version in use (`"v2"` or `None`).

### Handlers (accessed via client)

- **`client.auth`**: Login, register, token validation
- **`client.admin`**: Admin user management (admin only)
- **`client.user`**: Current user get/update
- **`client.project`**: Projects (create, get, update, delete)
- **`client.checkpoint`**: Checkpoints (add, download, update, delete, file events)
- **`client.base_model`**: Base model upload and external base models
- **`client.result`**: Analysis results and artifacts
- **`client.membership`**: Project membership
- **`client.static`**: Static analysis, exclude, edit, metatune
- **`client.dynamic`**: Dynamic analyses (comparative, correlation, inference, sensitivity, etc.)

### File Uploads

For requests that upload files, use `authentrics_client.generate_multipart_json(file_path, **data)` as the `files` argument to the handler method.

## Troubleshooting

- **`ValueError: Pass api_version as a keyword argument`** — You passed the API version as a positional argument. Use the keyword: `AuthentricsClient(base_url, api_version="v2")`.
- **Connection or name resolution errors** — Check that `base_url` is correct and reachable (e.g. `https://api.authentrics.ai` or your deployment URL). If you use a proxy, pass it as `proxy_url=`, not as the second positional argument.
- **Authentication failures** — Verify credentials and that the base URL points to a running Authentrics API. For versioned login, use `api_version="v2"` when creating the client.

For more help, see [Support](#support) below.

## Support

For comprehensive documentation and support, visit the [Authentrics.ai documentation](https://authentrics-team-lrq1a2rkieci.atlassian.net/wiki/spaces/Authentric1/overview).

## Contributing

For Authentrics.ai employees, please see [CONTRIBUTING.md](./CONTRIBUTING.md).
