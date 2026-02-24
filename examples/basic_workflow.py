"""
Basic workflow example for the Authentrics client.

Demonstrates: login, creating a project, adding checkpoints, fetching project
details, and running static analysis. Use real file paths and credentials when
running; the versioned client is optional.
"""
import authentrics_client as authrx

# Initialize the client (optionally with API version for versioned paths).
# Omit api_version for unversioned (legacy) paths.
client = authrx.AuthentricsClient(
    "https://api.authentrics.ai",
    api_version="v2",  # optional: use versioned paths; remove or set None for legacy
)

# Login with your credentials.
client.auth.login(
    username="your_username",
    password="your_password",
)

# Create a project.
project = client.project.create_project(
    name="My Project",
    description="Example project for static analysis",
    model_format="onnx",
)

# Add checkpoints (use real file paths on your machine).
checkpoint_paths = [
    "path/to/checkpoint1.onnx",
    "path/to/checkpoint2.onnx",
    "path/to/checkpoint3.onnx",
]
for path in checkpoint_paths:
    client.checkpoint.add_checkpoint(
        project_id=project["id"],
        file_path=path,
        model_format="onnx",
    )

# Refresh project to get file list with checkpoint IDs.
project = client.project.get_project_by_id(project["id"])
checkpoint_ids = [f["id"] for f in project.get("fileList", [])]

# Run static analysis on each checkpoint (except the first, which has no previous).
results = []
for checkpoint_id in checkpoint_ids[1:]:
    result = client.static.static_analysis(
        project_id=project["id"],
        checkpoint_id=checkpoint_id,
    )
    results.append(result)

print("Static analysis results:", results)
